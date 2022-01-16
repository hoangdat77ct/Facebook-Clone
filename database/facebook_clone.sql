-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 16, 2022 at 02:48 PM
-- Server version: 8.0.27-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `facebook_clone`
--

-- --------------------------------------------------------

--
-- Table structure for table `article`
--

CREATE TABLE `article` (
  `article_id` int NOT NULL,
  `user_id` int NOT NULL,
  `content` varchar(800) DEFAULT NULL,
  `static_file` varchar(500) DEFAULT NULL,
  `publish_time` datetime NOT NULL,
  `status` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `article`
--

INSERT INTO `article` (`article_id`, `user_id`, `content`, `static_file`, `publish_time`, `status`) VALUES
(4, 13, 'Bài viết số 1', 'img/hinhanh.png', '2022-01-13 16:51:03', 1),
(5, 13, 'Bài viết số 2', 'img/hinhanh.png', '2022-01-13 16:51:23', 0),
(6, 16, 'Hiệp thi đấu đầu tiên ngoài món quà từ thủ môn Martinez dành cho Bruno thì chúng ta hãy dành tràn số 36 để hoan nghênh Anthony Elanga nhé. Màn trình diễn rất hay của cầu thủ trẻ này.', 'img/hinhanh.png', '2022-01-16 13:31:42', 1),
(7, 16, 'Hiệp thi đấu đầu tiên ngoài món quà từ thủ môn Martinez dành cho Bruno thì chúng ta hãy dành tràn', 'img/hinhanh2.png', '2022-01-16 13:36:25', 0);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int NOT NULL,
  `public_name` varchar(50) NOT NULL,
  `avatar` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1',
  `cover_img` varchar(500) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '1',
  `phone` char(100) DEFAULT NULL,
  `email` char(100) NOT NULL,
  `user_name` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `public_status` tinyint(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `public_name`, `avatar`, `cover_img`, `phone`, `email`, `user_name`, `password`, `public_status`) VALUES
(13, 'admin', '1', '1', '0123456789', 'admin@gmail.com', 'admin', 'sha256$ymvvWQ3FUpOJiL2y$0886cd1965c08dbcc356af2d942637ee64485104ca707fcb94afd92327718f46', 1),
(14, 'admin1', '1', '1', '0123456789', 'admin1@gmail.com', 'admin1', 'sha256$8dO8oyEeUCVqEuFY$827870df1286a59df647fcc397e50c2e181b378125b0a1a4b399bab12c02e6f2', 1),
(15, 'admin2', '1', '1', '0123456789', 'admin2@gmail.com', 'admin2', 'sha256$r30pOIUaRLioyYXS$c7f06782ad5c914c3ac4967cfd590b5b60b40b76b838c0816860acef0ea26887', 0),
(16, 'Hoàng Minh', 'img/avatar-1-cover.png', 'img/update-coverimg-1.png', '0113456789', 'hoangdat777ct@gmail.com', 'hoangminh', 'sha256$plAwYR1fQS8KzG2K$f84a95c58529a06fae340a9b829958123f406156433cdddb09740a07e0d7454b', 0),
(17, 'Hoàng Đạt', '1', '1', '0123456', 'hoangdat77ct@gmail.com', 'test', 'sha256$ycd4m5gzthZ05LjU$fea2d0ba42d0e168fc62bc3f3d5feece5bb460b67674d26067b156899699dbe3', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `article`
--
ALTER TABLE `article`
  ADD PRIMARY KEY (`article_id`),
  ADD KEY `FK1` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`) USING BTREE,
  ADD UNIQUE KEY `user_name` (`user_name`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `article`
--
ALTER TABLE `article`
  MODIFY `article_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `article`
--
ALTER TABLE `article`
  ADD CONSTRAINT `FK1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
