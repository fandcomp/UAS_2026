-- ============================================================
-- setup_badcrud.sql
-- Script setup database untuk aplikasi DamnCRUD
-- Database: badcrud (sesuai functions.php)
-- ============================================================

-- Buat database badcrud jika belum ada
CREATE DATABASE IF NOT EXISTS `badcrud`
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_general_ci;

USE `badcrud`;

-- ── Tabel contacts ─────────────────────────────────────────
DROP TABLE IF EXISTS `contacts`;
CREATE TABLE `contacts` (
  `id`      int(11)      NOT NULL AUTO_INCREMENT,
  `name`    varchar(255) NOT NULL,
  `email`   varchar(255) NOT NULL,
  `phone`   varchar(255) NOT NULL,
  `title`   varchar(255) NOT NULL,
  `created` datetime     NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16
  DEFAULT CHARSET=utf8
  COLLATE=utf8_general_ci;

-- ── Data kontak (13 baris) ─────────────────────────────────
INSERT INTO `contacts` (`id`, `name`, `email`, `phone`, `title`, `created`) VALUES
  (1,  'John Does',      'johndoe@example.com',       '2026550143', 'Judge',      '2019-05-08 17:32:00'),
  (2,  'David Deacon',   'daviddeacon@example.com',   '2025550121', 'Security',   '2019-05-08 17:28:44'),
  (3,  'Sam White',      'samwhite@example.com',      '2004550121', 'Employee',   '2019-05-08 17:29:27'),
  (4,  'Colin Chaplin',  'colinchaplin@example.com',  '2022550178', 'Supervisor', '2019-05-08 17:29:27'),
  (5,  'Ricky Waltz',    'rickywaltz@example.com',    '7862342390', 'Employee',   '2019-05-09 19:16:00'),
  (6,  'Arnold Hall',    'arnoldhall@example.com',    '5089573579', 'Manager',    '2019-05-09 19:17:00'),
  (7,  'Toni Adams',     'alvah1981@example.com',     '2603668738', 'Employee',   '2019-05-09 19:19:00'),
  (8,  'Donald Perry',   'donald1983@example.com',    '7019007916', 'Employee',   '2019-05-09 19:20:00'),
  (9,  'Joe McKinney',   'nadia.doole0@example.com',  '6153353674', 'Employee',   '2019-05-09 19:20:00'),
  (10, 'Angela Horst',   'angela1977@example.com',    '3094234980', 'Assistant',  '2019-05-09 19:21:00'),
  (11, 'James Jameson',  'james1965@example.com',     '4002349823', 'Assistant',  '2019-05-09 19:32:00'),
  (12, 'Daniel Deacon',  'danieldeacon@example.com',  '5003423549', 'Manager',    '2019-05-09 19:33:00'),
  (13, 'Ikram',          'ikram@suhu.co',              '0092988122', 'Director',   '2019-12-20 10:06:09');

-- ── Tabel users ────────────────────────────────────────────
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id_user`  int(2)       NOT NULL AUTO_INCREMENT,
  `username` varchar(50)  DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_user`)
) ENGINE=InnoDB AUTO_INCREMENT=2
  DEFAULT CHARSET=utf8mb4
  COLLATE=utf8mb4_general_ci;

-- ── Data user admin ────────────────────────────────────────
-- username : admin
-- password : nimda666!  (hash SHA256 + salt XDrBmrW9g2fb)
INSERT INTO `users` (`id_user`, `username`, `password`) VALUES
  (1, 'admin', '9feac9a05349e4ccc78fb9d9b4ab61b33f868c7f8b8acd56dc7303c1af0cb7ca');

-- ── Verifikasi ─────────────────────────────────────────────
SELECT 'Database badcrud berhasil dibuat!'  AS status;
SELECT CONCAT('Jumlah kontak : ', COUNT(*)) AS info FROM contacts;
SELECT CONCAT('Jumlah user   : ', COUNT(*)) AS info FROM users;
