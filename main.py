from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List
from PIL import Image, ExifTags
import io
import os
import uvicorn
import torch
import torch.nn as nn
from torchvision import transforms, models
import mysql.connector
from datetime import datetime, timedelta
import random
from passlib.context import CryptContext
from jose import jwt

app = FastAPI(title="Road AI Backend API dengan JWT Auth")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Konfigurasi JWT Keamanan
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pydantic Model untuk request Auth (TanPA ROLE)
class UserRegister(BaseModel):
    fullname: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# =======================================================
# FUNGSI DATABASE & KEAMANAN
# =======================================================
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", 3306),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASS", ""),
        database=os.environ.get("DB_NAME", "defaultdb")
    )

def simpan_ke_database(filename, kelas_kerusakan, akurasi, lat, lon):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        sql_query = "INSERT INTO riwayat_deteksi (nama_file, kelas_kerusakan, akurasi, waktu_inspeksi, latitude, longitude) VALUES (%s, %s, %s, %s, %s, %s)"
        waktu_sekarang = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = (filename, kelas_kerusakan, akurasi, waktu_sekarang, lat, lon)
        cursor.execute(sql_query, values)
        db.commit()
        cursor.close()
        db.close()
    except Exception as e:
        print(f"Error Database Log: {e}")

# =======================================================
# ENDPOINT AUTHENTICATION (REGISTER & LOGIN)
# =======================================================
@app.post("/api/auth/register")
def register_user(user: UserRegister):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        
        # Cek apakah email sudah terdaftar
        cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            raise HTTPException(status_code=400, detail="Email sudah terdaftar!")
        
        # Hash password sebelum disimpan
        hashed_password = pwd_context.hash(user.password)
        
        sql = "INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (user.fullname, user.email, hashed_password))
        db.commit()
        
        cursor.close()
        db.close()
        return {"status": "success", "pesan": "Akun berhasil dibuat!"}
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/login")
def login_user(user: UserLogin):
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        db_user = cursor.fetchone()
        
        cursor.close()
        db.close()
        
        if not db_user or not pwd_context.verify(user.password, db_user["password"]):
            raise HTTPException(status_code=400, detail="Email atau password salah!")
        
        # Buat JWT Token
        waktu_kadaluarsa = datetime.utcnow() + timedelta(minutes=120)
        payload = {
            "sub": db_user["email"],
            "fullname": db_user["fullname"],
            "exp": waktu_kadaluarsa
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        return {
            "status": "success",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "fullname": db_user["fullname"]
            }
        }
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

# =======================================================
# LOGIKA OPREK EKSTRAKSI GPS FOTO & MODEL AI ROAD
# =======================================================
def get_decimal_from_dms(dms, ref):
    decimal = float(dms[0]) + float(dms[1])/60 + float(dms[2])/3600
    if ref in ['S', 'W']: decimal = -decimal
    return decimal

def get_image_coordinates(image):
    try:
        exif = image._getexif()
        if not exif: raise ValueError()
        geotagging = {}
        for (idx, tag) in ExifTags.TAGS.items():
            if tag == 'GPSInfo':
                for (key, val) in ExifTags.GPSTAGS.items():
                    if key in exif[idx]: geotagging[val] = exif[idx][key]
        lat = get_decimal_from_dms(geotagging['GPSLatitude'], geotagging['GPSLatitudeRef'])
        lon = get_decimal_from_dms(geotagging['GPSLongitude'], geotagging['GPSLongitudeRef'])
        return lat, lon
    except Exception:
        base_lat, base_lon = -7.7113, 110.6010 # Default Klaten
        return base_lat + random.uniform(-0.04, 0.04), base_lon + random.uniform(-0.04, 0.04)

def load_road_model():
    model = models.convnext_tiny(weights=None)
    in_features = 768
    model.classifier = nn.Sequential(
        nn.Flatten(start_dim=1, end_dim=-1),
        nn.LayerNorm((768,), eps=1e-06, elementwise_affine=True),
        nn.Sequential(
            nn.Dropout(p=0.5), nn.Linear(in_features, 256), nn.ReLU(), nn.Dropout(p=0.3), nn.Linear(256, 3)
        )
    )
    try: model.load_state_dict(torch.load("convnext_tiny_MODEL1_final.pth", map_location=device), strict=False)
    except Exception: pass
    model.to(device).eval()
    return model

model = load_road_model()
transform_pipeline = transforms.Compose([
    transforms.Resize((224, 224)), transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

CLASS_MAPPING = {
    0: {"nama": "Alligator Cracking", "hex": "#ef4444"},
    1: {"nama": "Corrugation (Keriting)", "hex": "#3b82f6"},
    2: {"nama": "Potholes (Lubang)", "hex": "#f59e0b"}
}

@app.get("/api/riwayat")
def get_riwayat():
    try:
        db = get_db_connection(); cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM riwayat_deteksi ORDER BY id DESC LIMIT 5")
        records = cursor.fetchall(); cursor.close(); db.close()
        for r in records:
            if isinstance(r['waktu_inspeksi'], datetime): r['waktu_inspeksi'] = r['waktu_inspeksi'].strftime('%d %b %Y %H:%M')
        return {"status": "success", "data": records}
    except Exception as e: return {"status": "error", "pesan": str(e)}

@app.get("/api/peta")
def get_data_peta():
    try:
        db = get_db_connection(); cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM riwayat_deteksi WHERE latitude IS NOT NULL ORDER BY id DESC")
        records = cursor.fetchall(); cursor.close(); db.close()
        for r in records:
            if isinstance(r['waktu_inspeksi'], datetime): r['waktu_inspeksi'] = r['waktu_inspeksi'].strftime('%d %b %Y %H:%M')
        return {"status": "success", "data": records}
    except Exception as e: return {"status": "error", "pesan": str(e)}

@app.post("/api/deteksi")
async def deteksi_kerusakan(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        lat, lon = get_image_coordinates(image)
        tensor_img = transform_pipeline(image).unsqueeze(0).to(device)
        with torch.no_grad():
            outputs = model(tensor_img)
            _, predicted_idx = torch.max(torch.nn.functional.softmax(outputs[0], dim=0), 0)
            idx = predicted_idx.item()
            conf_score = round(torch.max(torch.nn.functional.softmax(outputs[0], dim=0), 0)[0].item() * 100, 2)
        hasil = CLASS_MAPPING.get(idx, {"nama": "Tidak Dikenali", "hex": "#ffffff"})
        simpan_ke_database(file.filename, hasil["nama"], conf_score, lat, lon)
        return {"status": "success", "prediksi": hasil["nama"], "persentase": conf_score, "warna_hex": hasil["hex"]}
    except Exception as e: return {"status": "error", "pesan": str(e)}

@app.post("/api/deteksi/batch")
async def deteksi_kerusakan_batch(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        try:
            image_bytes = await file.read()
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            lat, lon = get_image_coordinates(image)
            tensor_img = transform_pipeline(image).unsqueeze(0).to(device)
            with torch.no_grad():
                outputs = model(tensor_img)
                idx = torch.max(torch.nn.functional.softmax(outputs[0], dim=0), 0)[1].item()
                conf_score = round(torch.max(torch.nn.functional.softmax(outputs[0], dim=0), 0)[0].item() * 100, 2)
            hasil = CLASS_MAPPING.get(idx, {"nama": "Tidak Dikenali", "hex": "#ffffff"})
            simpan_ke_database(file.filename, hasil["nama"], conf_score, lat, lon)
            results.append({"filename": file.filename, "status": "success", "prediksi": hasil["nama"], "persentase": conf_score, "warna_hex": hasil["hex"]})
        except Exception as e: results.append({"filename": file.filename, "status": "error", "pesan": str(e)})
    return {"status": "success", "results": results}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)