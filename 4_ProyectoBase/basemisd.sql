-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 15, 2026 at 02:56 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `basemisd`
--

-- --------------------------------------------------------

--
-- Table structure for table `registros_litros`
--

CREATE TABLE `registros_litros` (
  `id` int(11) NOT NULL,
  `litros` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `resultados_conversion`
--

CREATE TABLE `resultados_conversion` (
  `id` int(11) NOT NULL,
  `registro_id` int(11) NOT NULL,
  `mililitros` double NOT NULL,
  `centilitros` double NOT NULL,
  `metros_cubicos` double NOT NULL,
  `tiempo_microsegundos` double NOT NULL,
  `fecha_procesamiento` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `registros_litros`
--
ALTER TABLE `registros_litros`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `resultados_conversion`
--
ALTER TABLE `resultados_conversion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_registros_litros` (`registro_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `resultados_conversion`
--
ALTER TABLE `resultados_conversion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `resultados_conversion`
--
ALTER TABLE `resultados_conversion`
  ADD CONSTRAINT `fk_registros_litros` FOREIGN KEY (`registro_id`) REFERENCES `registros_litros` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
