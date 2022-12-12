-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2022-12-12 05:03:19
-- 服务器版本： 10.4.21-MariaDB
-- PHP 版本： 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `air_ticket`
--

-- --------------------------------------------------------

--
-- 表的结构 `airline`
--

CREATE TABLE `airline` (
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Cathey Pacific'),
('China Eastern');

-- --------------------------------------------------------

--
-- 表的结构 `airline_staff`
--

CREATE TABLE `airline_staff` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `date_of_birth` date NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `permission` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`, `permission`) VALUES
('ha', '101a6ec9f938885df0a44f20458d2eb4', 'ha', 'ha', '2000-01-01', 'China Eastern', 'admin'),
('he', 'ffe553694f5096471590343432359e02', 'he', 'he', '1999-01-01', 'China Eastern', 'staff'),
('hi', 'c4bb408471eb7727e59e11385b0a8c19', 'hi', 'hi', '1999-01-01', 'Cathey Pacific', 'admin'),
('hihi', 'c4bb408471eb7727e59e11385b0a8c19', 'hi', 'hi', '1996-03-09', 'China Eastern', 'operator'),
('ho', '8b0dc2e34844337434b8475108a490ab', 'ho', 'ho', '1999-01-01', 'Cathey Pacific', 'operator'),
('hu', 'a334ed15e6c4bc3cff677821df4a8960', 'hu', 'hu', '1980-08-08', 'China Eastern', 'admin'),
('o', '9982b2a7fceaaee2c8444b5086aee008', 'o', 'o', '1990-01-01', 'Cathey Pacific', 'admin');

-- --------------------------------------------------------

--
-- 表的结构 `airplane`
--

CREATE TABLE `airplane` (
  `airline_name` varchar(50) NOT NULL,
  `airplane_id` varchar(10) NOT NULL,
  `seats` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('Cathey Pacific', 'A666', 500),
('Cathey Pacific', 'C000', 400),
('Cathey Pacific', 'D100', 500),
('Cathey Pacific', 'E555', 600),
('Cathey Pacific', 'F111', 300),
('China Eastern', 'A888', 300),
('China Eastern', 'B888', 300),
('China Eastern', 'C888', 200),
('China Eastern', 'F666', 300);

-- --------------------------------------------------------

--
-- 表的结构 `airport`
--

CREATE TABLE `airport` (
  `airport_name` varchar(50) NOT NULL,
  `airport_city` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('FOC', 'Fuzhou'),
('HKG', 'Hong Kong'),
('JFK', 'NYC'),
('PEK', 'Beijing'),
('PVG', 'Shanghai'),
('SHA', 'Shanghai'),
('WUX', 'Wuxi');

-- --------------------------------------------------------

--
-- 表的结构 `booking_agent`
--

CREATE TABLE `booking_agent` (
  `email` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `booking_agent_id` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('a@gmail.com', '0b4e7a0e5fe84ad35fb5f95b9ceeac79', '2222'),
('agent@163.com', '65d4c7c8c5119ebec464ad55c08acac0', '1111'),
('b@gmail.com', '875f26fdb1cecf20ceb4ca028263dec6', '3333'),
('c@gmail.com', 'c1f68ec06b490b3ecb4066b1b13a9ee9', '4444');

-- --------------------------------------------------------

--
-- 表的结构 `customer`
--

CREATE TABLE `customer` (
  `email` varchar(50) NOT NULL,
  `name` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL,
  `building_number` varchar(50) NOT NULL,
  `street` varchar(50) NOT NULL,
  `city` varchar(50) NOT NULL,
  `state` varchar(50) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `passport_number` varchar(20) NOT NULL,
  `passport_expiration` date NOT NULL,
  `passport_country` varchar(20) NOT NULL,
  `date_of_birth` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('bb@163.com', 'bb', '875f26fdb1cecf20ceb4ca028263dec6', 'bb', 'bb', 'bb', 'bb', '122-2333-2333', '1234ABB', '2026-10-07', 'China', '2009-01-07'),
('he@163.com', 'he', 'ffe553694f5096471590343432359e02', 'his building', 'his street', 'his city', 'his state', '111-1111-1111', 'I22222222', '2040-04-04', 'his country', '2000-01-01'),
('hh@163.com', 'hh', 'f14029217ff5e7a50cdc7e70f686cf29', 'hh', 'hh', 'hh', 'hh', '123-2333-2332', '1234HHH', '2023-10-09', 'China', '2022-12-24'),
('me@gmail.com', 'me', '46756b989b1050a317258e6d5e8e9891', 'my building', 'my street', 'my city', 'my state', '222-2222-2222', 'I22222222', '2040-04-04', 'my country', '2000-02-02'),
('qt3462@nyu.edu', 'Qianyue Tang', '7fa8282ad93047a4d6fe6111c93b308a', '11111', '140 E 14th Street', 'New York City', 'New York', '646-1639-7954', '111111', '1111-11-11', '111', '1111-11-11'),
('qt346@nyu.edu', 'Qianyue', '123456', 'AB', 'Century Avenue', 'Shanghai', 'Shanghai', '18906161088', 'A1234567', '2030-01-01', 'China', '2001-12-12');

-- --------------------------------------------------------

--
-- 表的结构 `flight`
--

CREATE TABLE `flight` (
  `airline_name` varchar(50) NOT NULL,
  `flight_number` varchar(10) NOT NULL,
  `departure_time` datetime NOT NULL,
  `arrival_time` datetime NOT NULL,
  `price` decimal(10,0) NOT NULL,
  `status` varchar(50) NOT NULL,
  `airplane_id` varchar(10) NOT NULL,
  `departure_airport` varchar(50) NOT NULL,
  `arrival_airport` varchar(50) NOT NULL,
  `departure_city` varchar(20) NOT NULL,
  `arrival_city` varchar(20) NOT NULL,
  `remaining_tickets` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `departure_time`, `arrival_time`, `price`, `status`, `airplane_id`, `departure_airport`, `arrival_airport`, `departure_city`, `arrival_city`, `remaining_tickets`) VALUES
('Cathey Pacific', 'CX338', '2022-12-04 16:56:00', '2022-12-05 16:57:00', '2000', 'upcoming', 'A666', 'PVG', 'JFK', 'Shanghai', 'NYC', 198),
('Cathey Pacific', 'CX367', '2021-08-28 13:25:00', '2021-08-28 16:15:00', '300', 'upcoming', 'C000', 'PVG', 'HKG', 'Shanghai', 'Hong Kong', 199),
('Cathey Pacific', 'CX844', '2021-08-29 02:05:00', '2021-08-29 06:00:00', '1700', 'in-progress', 'A666', 'HKG', 'JFK', 'Hong Kong', 'NYC', 299),
('China Eastern', 'CA338', '2022-12-17 19:10:00', '2022-12-18 19:11:00', '8000', 'upcoming', 'A888', 'JFK', 'FOC', 'NYC', 'Fuzhou', 246),
('China Eastern', 'CA389', '2022-12-09 14:08:00', '2022-12-10 14:09:00', '500', 'upcoming', 'B888', 'JFK', 'FOC', 'NYC', 'Fuzhou', 200),
('China Eastern', 'MU111', '2020-01-01 10:10:00', '2020-01-01 00:22:00', '200', 'upcoming', 'F666', 'PEK', 'SHA', 'Beijing', 'Shanghai', 199),
('China Eastern', 'MU288', '2021-02-01 15:00:00', '2021-02-01 17:00:00', '200', 'upcoming', 'B888', 'WUX', 'PEK', 'Wuxi', 'Beijing', 187),
('China Eastern', 'MU500', '2023-01-01 13:01:00', '2023-01-01 15:01:00', '250', 'upcoming', 'F666', 'PEK', 'PVG', 'Beijing', 'Shanghai', 0),
('China Eastern', 'MU588', '2022-05-23 16:25:00', '2021-05-24 20:20:00', '1900', 'upcoming', 'B888', 'JFK', 'FOC', 'NYC', 'Fuzhou', 189);

-- --------------------------------------------------------

--
-- 表的结构 `purchase`
--

CREATE TABLE `purchase` (
  `ticket_id` varchar(10) NOT NULL,
  `customer_email` varchar(50) NOT NULL,
  `booking_agent_id` varchar(10) DEFAULT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `purchase`
--

INSERT INTO `purchase` (`ticket_id`, `customer_email`, `booking_agent_id`, `date`) VALUES
('011212', 'qt346@nyu.edu', NULL, '2021-06-01'),
('666889', 'he@163.com', NULL, '2022-12-04'),
('666890', 'he@163.com', '1111', '2022-12-04'),
('666891', 'he@163.com', '1111', '2022-12-05'),
('666892', 'he@163.com', NULL, '2022-12-05'),
('666893', 'he@163.com', '2222', '2020-12-06'),
('666894', 'me@gmail.com', '1111', '2022-12-06'),
('666895', 'me@gmail.com', NULL, '2022-12-06'),
('666899', 'bb@163.com', '2222', '2022-12-08'),
('666900', 'bb@163.com', NULL, '2022-12-08'),
('666901', 'bb@163.com', NULL, '2022-12-08'),
('666904', 'bb@163.com', NULL, '2022-12-08'),
('666905', 'me@gmail.com', '2222', '2022-12-08'),
('666906', 'bb@163.com', NULL, '2022-12-08'),
('666907', 'hh@163.com', NULL, '2022-12-09'),
('666908', 'me@gmail.com', '2222', '2022-12-09'),
('666909', 'me@gmail.com', '3333', '2022-12-09'),
('666910', 'bb@163.com', NULL, '2022-12-09'),
('666911', 'me@gmail.com', '1111', '2022-12-09'),
('666912', 'hh@163.com', '1111', '2022-12-09'),
('666913', 'hh@163.com', '3333', '2022-12-09');

-- --------------------------------------------------------

--
-- 表的结构 `ticket`
--

CREATE TABLE `ticket` (
  `ticket_id` varchar(10) NOT NULL,
  `airline_name` varchar(50) NOT NULL,
  `flight_number` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_number`) VALUES
('666891', 'Cathey Pacific', 'CX338'),
('666900', 'Cathey Pacific', 'CX338'),
('666902', 'Cathey Pacific', 'CX338'),
('666903', 'Cathey Pacific', 'CX338'),
('123456', 'Cathey Pacific', 'CX367'),
('666889', 'Cathey Pacific', 'CX367'),
('666909', 'Cathey Pacific', 'CX367'),
('011212', 'Cathey Pacific', 'CX844'),
('666906', 'Cathey Pacific', 'CX844'),
('666897', 'China Eastern', 'CA338'),
('666899', 'China Eastern', 'CA338'),
('666901', 'China Eastern', 'CA338'),
('666904', 'China Eastern', 'CA338'),
('666905', 'China Eastern', 'CA338'),
('666908', 'China Eastern', 'CA338'),
('666912', 'China Eastern', 'MU111'),
('666894', 'China Eastern', 'MU288'),
('666910', 'China Eastern', 'MU288'),
('666911', 'China Eastern', 'MU288'),
('666913', 'China Eastern', 'MU288'),
('666895', 'China Eastern', 'MU500'),
('666888', 'China Eastern', 'MU588'),
('666890', 'China Eastern', 'MU588'),
('666892', 'China Eastern', 'MU588'),
('666893', 'China Eastern', 'MU588'),
('666896', 'China Eastern', 'MU588'),
('666907', 'China Eastern', 'MU588');

-- --------------------------------------------------------

--
-- 表的结构 `works_for`
--

CREATE TABLE `works_for` (
  `email` varchar(50) NOT NULL,
  `airline_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `works_for`
--

INSERT INTO `works_for` (`email`, `airline_name`) VALUES
('a@gmail.com', 'Cathey Pacific'),
('a@gmail.com', 'China Eastern'),
('agent@163.com', 'Cathey Pacific'),
('agent@163.com', 'China Eastern'),
('b@gmail.com', 'Cathey Pacific'),
('b@gmail.com', 'China Eastern'),
('c@gmail.com', 'China Eastern');

--
-- 转储表的索引
--

--
-- 表的索引 `airline`
--
ALTER TABLE `airline`
  ADD PRIMARY KEY (`airline_name`);

--
-- 表的索引 `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD PRIMARY KEY (`username`),
  ADD KEY `airline_name` (`airline_name`);

--
-- 表的索引 `airplane`
--
ALTER TABLE `airplane`
  ADD PRIMARY KEY (`airline_name`,`airplane_id`);

--
-- 表的索引 `airport`
--
ALTER TABLE `airport`
  ADD PRIMARY KEY (`airport_name`);

--
-- 表的索引 `booking_agent`
--
ALTER TABLE `booking_agent`
  ADD PRIMARY KEY (`email`);

--
-- 表的索引 `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`email`);

--
-- 表的索引 `flight`
--
ALTER TABLE `flight`
  ADD PRIMARY KEY (`airline_name`,`flight_number`),
  ADD KEY `airline_name` (`airline_name`,`airplane_id`),
  ADD KEY `departure_airport` (`departure_airport`),
  ADD KEY `arrival_airport` (`arrival_airport`),
  ADD KEY `departure_city` (`departure_city`);

--
-- 表的索引 `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`ticket_id`,`customer_email`),
  ADD KEY `customer_email` (`customer_email`);

--
-- 表的索引 `ticket`
--
ALTER TABLE `ticket`
  ADD PRIMARY KEY (`ticket_id`),
  ADD KEY `airline_name` (`airline_name`,`flight_number`);

--
-- 表的索引 `works_for`
--
ALTER TABLE `works_for`
  ADD PRIMARY KEY (`email`,`airline_name`),
  ADD KEY `airline_name` (`airline_name`);

--
-- 限制导出的表
--

--
-- 限制表 `airline_staff`
--
ALTER TABLE `airline_staff`
  ADD CONSTRAINT `airline_staff_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- 限制表 `airplane`
--
ALTER TABLE `airplane`
  ADD CONSTRAINT `airplane_ibfk_1` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`);

--
-- 限制表 `flight`
--
ALTER TABLE `flight`
  ADD CONSTRAINT `flight_ibfk_1` FOREIGN KEY (`airline_name`,`airplane_id`) REFERENCES `airplane` (`airline_name`, `airplane_id`),
  ADD CONSTRAINT `flight_ibfk_2` FOREIGN KEY (`departure_airport`) REFERENCES `airport` (`airport_name`),
  ADD CONSTRAINT `flight_ibfk_3` FOREIGN KEY (`arrival_airport`) REFERENCES `airport` (`airport_name`);

--
-- 限制表 `purchase`
--
ALTER TABLE `purchase`
  ADD CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`ticket_id`) REFERENCES `ticket` (`ticket_id`),
  ADD CONSTRAINT `purchase_ibfk_2` FOREIGN KEY (`customer_email`) REFERENCES `customer` (`email`) ON UPDATE CASCADE;

--
-- 限制表 `ticket`
--
ALTER TABLE `ticket`
  ADD CONSTRAINT `ticket_ibfk_1` FOREIGN KEY (`airline_name`,`flight_number`) REFERENCES `flight` (`airline_name`, `flight_number`);

--
-- 限制表 `works_for`
--
ALTER TABLE `works_for`
  ADD CONSTRAINT `works_for_ibfk_1` FOREIGN KEY (`email`) REFERENCES `booking_agent` (`email`),
  ADD CONSTRAINT `works_for_ibfk_2` FOREIGN KEY (`airline_name`) REFERENCES `airline` (`airline_name`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
