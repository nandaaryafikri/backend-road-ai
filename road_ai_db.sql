-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 24 Bulan Mei 2026 pada 16.53
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `road_ai_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `riwayat_deteksi`
--

CREATE TABLE `riwayat_deteksi` (
  `id` int(11) NOT NULL,
  `nama_file` varchar(255) NOT NULL,
  `kelas_kerusakan` varchar(100) NOT NULL,
  `akurasi` float NOT NULL,
  `waktu_inspeksi` datetime NOT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `riwayat_deteksi`
--

INSERT INTO `riwayat_deteksi` (`id`, `nama_file`, `kelas_kerusakan`, `akurasi`, `waktu_inspeksi`, `latitude`, `longitude`) VALUES
(15, 'POTHOLES_ONLINE (23).jpg', 'Potholes (Lubang)', 99.31, '2026-05-24 12:24:12', NULL, NULL),
(16, 'POTHOLES_ONLINE (38).jpg', 'Potholes (Lubang)', 99.35, '2026-05-24 12:24:25', NULL, NULL),
(17, 'IMG_20260425_134130_955.jpg', 'Corrugation (Keriting)', 98.49, '2026-05-24 16:01:40', -7.6851, 110.384),
(18, 'IMG_20260425_131242_474.jpg', 'Potholes (Lubang)', 97.71, '2026-05-24 16:07:53', -7.68287, 110.419),
(19, 'IMG_20260425_132509_401.jpg', 'Potholes (Lubang)', 98.97, '2026-05-24 16:08:40', -7.67456, 110.43),
(20, 'IMG_20260425_150223_370.jpg', 'Potholes (Lubang)', 95.31, '2026-05-24 16:09:13', -7.6698, 110.368),
(21, 'IMG_20260425_131117_728.jpg', 'Potholes (Lubang)', 99.23, '2026-05-24 16:10:01', -7.70522, 110.365),
(22, 'IMG_20260425_131119_171.jpg', 'Potholes (Lubang)', 97.82, '2026-05-24 16:10:01', -7.69189, 110.375),
(23, 'IMG_20260425_131242_474.jpg', 'Potholes (Lubang)', 97.71, '2026-05-24 16:10:02', -7.6682, 110.369),
(24, 'IMG_20260425_131245_063.jpg', 'Potholes (Lubang)', 97.34, '2026-05-24 16:10:02', -7.69097, 110.401),
(25, 'IMG_20260425_131301_771.jpg', 'Potholes (Lubang)', 98.45, '2026-05-24 16:10:03', -7.71279, 110.374),
(26, 'IMG_20260425_131303_880.jpg', 'Potholes (Lubang)', 97.86, '2026-05-24 16:10:03', -7.73551, 110.433),
(27, 'IMG_20260425_131527_066.jpg', 'Potholes (Lubang)', 98.31, '2026-05-24 16:10:04', -7.73196, 110.414),
(28, 'IMG_20260425_131530_890.jpg', 'Potholes (Lubang)', 97.8, '2026-05-24 16:10:04', -7.67197, 110.369),
(29, 'IMG_20260425_131553_708.jpg', 'Potholes (Lubang)', 98.1, '2026-05-24 16:10:05', -7.72078, 110.365),
(30, 'IMG_20260425_131558_918.jpg', 'Potholes (Lubang)', 98.86, '2026-05-24 16:10:05', -7.69784, 110.422),
(31, 'IMG_20260425_131618_467.jpg', 'Potholes (Lubang)', 98.52, '2026-05-24 16:10:06', -7.65424, 110.43),
(32, 'IMG_20260425_131620_737.jpg', 'Potholes (Lubang)', 98.44, '2026-05-24 16:10:06', -7.65983, 110.386),
(33, 'IMG_20260425_131627_894.jpg', 'Potholes (Lubang)', 98.59, '2026-05-24 16:10:07', -7.64087, 110.374),
(34, 'IMG_20260425_131630_926.jpg', 'Potholes (Lubang)', 98.39, '2026-05-24 16:10:07', -7.66493, 110.381),
(35, 'POTHOLES_ONLINE (3).jpg', 'Potholes (Lubang)', 99.3, '2026-05-24 18:15:50', -7.72776, 110.597),
(36, 'POTHOLES_ONLINE (5).jpg', 'Potholes (Lubang)', 99.37, '2026-05-24 18:42:41', -7.67441, 110.393),
(37, 'POTHOLES_ONLINE (5).jpg', 'Potholes (Lubang)', 99.37, '2026-05-24 18:42:44', -7.6589, 110.372),
(38, 'POTHOLES_ONLINE (5).jpg', 'Potholes (Lubang)', 99.37, '2026-05-24 18:42:46', -7.67331, 110.453),
(39, 'POTHOLES_ONLINE (11).jpg', 'Potholes (Lubang)', 99.29, '2026-05-24 18:44:24', -7.7283, 110.619),
(40, 'POTHOLES_ONLINE (3).jpg', 'Potholes (Lubang)', 99.3, '2026-05-24 18:45:13', -7.68487, 110.636),
(41, 'POTHOLES_ONLINE (5).jpg', 'Potholes (Lubang)', 99.37, '2026-05-24 18:45:51', -7.69927, 110.587),
(42, 'POTHOLES_ONLINE (9).jpg', 'Potholes (Lubang)', 99.32, '2026-05-24 18:46:14', -7.67469, 110.563),
(43, 'POTHOLES_ONLINE (10).jpg', 'Potholes (Lubang)', 99.14, '2026-05-24 18:46:14', -7.68471, 110.607),
(44, 'POTHOLES_ONLINE (11).jpg', 'Potholes (Lubang)', 99.29, '2026-05-24 18:46:15', -7.72825, 110.602),
(45, 'CFD_001_jpg.rf.d70ON6x4R4D14gOGyLcD.jpg', 'Corrugation (Keriting)', 98.54, '2026-05-24 18:48:02', -7.67641, 110.57),
(46, 'CFD_003_jpg.rf.3Bn1Nqx26Ym0yTMIPQU7.jpg', 'Corrugation (Keriting)', 98.66, '2026-05-24 18:48:03', -7.69762, 110.629),
(47, 'CFD_004_jpg.rf.lyxyVL5gGNQlsDjYDr1I.jpg', 'Corrugation (Keriting)', 98.17, '2026-05-24 18:48:03', -7.74028, 110.603),
(48, 'ALLIGATOR_PRIMER (18).jpg', 'Alligator Cracking', 99.47, '2026-05-24 18:48:20', -7.70328, 110.617),
(49, 'ALLIGATOR_PRIMER (19).jpg', 'Alligator Cracking', 99.48, '2026-05-24 18:48:20', -7.74471, 110.584),
(50, 'ALLIGATOR_PRIMER (20).jpg', 'Alligator Cracking', 99.51, '2026-05-24 18:48:21', -7.75044, 110.639),
(51, 'ALLIGATOR_PRIMER (21).jpg', 'Alligator Cracking', 99.53, '2026-05-24 18:48:21', -7.71005, 110.594);

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `fullname`, `email`, `password`) VALUES
(1, 'Nanda Arya Fikri', 'nandaaryafikri15@gmail.com', '$2b$12$QXuI0KF6404z6.mL2qfKReAnlWwB7hnopasIzeWk3s/E5woJ.vnmC');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `riwayat_deteksi`
--
ALTER TABLE `riwayat_deteksi`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `riwayat_deteksi`
--
ALTER TABLE `riwayat_deteksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
