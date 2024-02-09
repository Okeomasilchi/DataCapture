-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: localhost    Database: dc_dev_db
-- ------------------------------------------------------
-- Server version	8.0.35-0ubuntu0.23.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

-- Database creation and user management
DROP DATABASE IF EXISTS dc_dev_db;
CREATE DATABASE IF NOT EXISTS dc_dev_db;
CREATE USER IF NOT EXISTS 'dc_dev'@'localhost' IDENTIFIED BY 'dc_dev_pwd';
GRANT ALL PRIVILEGES ON `dc_dev_db`.* TO 'dc_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dc_dev'@'localhost';
FLUSH PRIVILEGES;

-- Table structure and data insertion
USE dc_dev_db;

-- Table structure for table `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `first_name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_user_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `customcategory`
DROP TABLE IF EXISTS `customcategory`;
CREATE TABLE `customcategory` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `idx_category_id` (`id`),
  CONSTRAINT `customcategory_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `surveys`
DROP TABLE IF EXISTS `surveys`;
CREATE TABLE `surveys` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `user_id` varchar(60) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `expiry_date` date DEFAULT NULL,
  `visibility` tinyint(1) NOT NULL,
  `randomize` tinyint(1) NOT NULL,
  `question_type` varchar(120) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `idx_survey_id` (`id`),
  CONSTRAINT `surveys_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `questions`
DROP TABLE IF EXISTS `questions`;
CREATE TABLE `questions` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `question` text NOT NULL,
  `options` json NOT NULL,
  `survey_id` varchar(60) NOT NULL,
  `random` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `survey_id` (`survey_id`),
  CONSTRAINT `questions_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `surveys` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `responses`
DROP TABLE IF EXISTS `responses`;
CREATE TABLE `responses` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `bio` json DEFAULT NULL,
  `timestamp` datetime NOT NULL,
  `answers` json NOT NULL,
  `survey_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `survey_id` (`survey_id`),
  CONSTRAINT `responses_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `surveys` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Table structure for table `surveycategory`
DROP TABLE IF EXISTS `surveycategory`;
CREATE TABLE `surveycategory` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `survey_id` varchar(60) NOT NULL,
  `category_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `survey_id` (`survey_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `surveycategory_ibfk_1` FOREIGN KEY (`survey_id`) REFERENCES `surveys` (`id`),
  CONSTRAINT `surveycategory_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `customcategory` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Data insertion for 'users' table
INSERT INTO users (id, first_name, email, password, last_name, created_at, updated_at)
VALUES
('user1_id', 'John', 'john@example.com', 'password123', 'Doe', NOW(), NOW()),
('user2_id', 'Jane', 'jane@example.com', 'password456', 'Doe', NOW(), NOW()),
('user3_id', 'Alice', 'alice@example.com', 'password789', 'Smith', NOW(), NOW()),
('user4_id', 'Bob', 'bob@example.com', 'passwordabc', 'Johnson', NOW(), NOW()),
('user5_id', 'Eva', 'eva@example.com', 'passworddef', 'Miller', NOW(), NOW()),
('user6_id', 'David', 'david@example.com', 'passwordghi', 'Wilson', NOW(), NOW()),
('user7_id', 'Sophia', 'sophia@example.com', 'passwordjkl', 'Anderson', NOW(), NOW()),
('user8_id', 'Michael', 'michael@example.com', 'passwordmno', 'Brown', NOW(), NOW()),
('user9_id', 'Olivia', 'olivia@example.com', 'passwordpqr', 'Martin', NOW(), NOW()),
('user10_id', 'William', 'william@example.com', 'passwordstu', 'Taylor', NOW(), NOW());

-- Data insertion for 'customcategory' table
INSERT INTO customcategory (id, name, user_id, created_at, updated_at)
VALUES
('category1_id', 'Category 1', 'user1_id', NOW(), NOW()),
('category2_id', 'Category 2', 'user2_id', NOW(), NOW()),
('category3_id', 'Category 3', 'user3_id', NOW(), NOW()),
('category4_id', 'Category 4', 'user4_id', NOW(), NOW()),
('category5_id', 'Category 5', 'user5_id', NOW(), NOW()),
('category6_id', 'Category 6', 'user6_id', NOW(), NOW()),
('category7_id', 'Category 7', 'user7_id', NOW(), NOW()),
('category8_id', 'Category 8', 'user8_id', NOW(), NOW()),
('category9_id', 'Category 9', 'user9_id', NOW(), NOW()),
('category10_id', 'Category 10', 'user10_id', NOW(), NOW());

-- Data insertion for 'surveys' table
INSERT INTO surveys (id, user_id, title, description, expiry_date, visibility, randomize, question_type, created_at, updated_at)
VALUES
('survey1_id', 'user1_id', 'Survey 1', 'Description for Survey 1', '2024-12-31', 1, 1, 'Type A', NOW(), NOW()),
('survey2_id', 'user2_id', 'Survey 2', 'Description for Survey 2', '2024-12-31', 1, 1, 'Type B', NOW(), NOW()),
('survey3_id', 'user3_id', 'Survey 3', 'Description for Survey 3', '2024-12-31', 1, 1, 'Type C', NOW(), NOW()),
('survey4_id', 'user4_id', 'Survey 4', 'Description for Survey 4', '2024-12-31', 1, 1, 'Type A', NOW(), NOW()),
('survey5_id', 'user5_id', 'Survey 5', 'Description for Survey 5', '2024-12-31', 1, 1, 'Type B', NOW(), NOW()),
('survey6_id', 'user6_id', 'Survey 6', 'Description for Survey 6', '2024-12-31', 1, 1, 'Type C', NOW(), NOW()),
('survey7_id', 'user7_id', 'Survey 7', 'Description for Survey 7', '2024-12-31', 1, 1, 'Type A', NOW(), NOW()),
('survey8_id', 'user8_id', 'Survey 8', 'Description for Survey 8', '2024-12-31', 1, 1, 'Type B', NOW(), NOW()),
('survey9_id', 'user9_id', 'Survey 9', 'Description for Survey 9', '2024-12-31', 1, 1, 'Type C', NOW(), NOW()),
('survey10_id', 'user10_id', 'Survey 10', 'Description for Survey 10', '2024-12-31', 1, 1, 'Type A', NOW(), NOW());

-- Data insertion for 'questions' table
INSERT INTO questions (id, question, options, survey_id, random, created_at, updated_at)
VALUES
('question1_id', 'What is your favorite color?', '["Red", "Blue", "Green"]', 'survey1_id', 1, NOW(), NOW()),
('question2_id', 'How often do you exercise?', '["Never", "Rarely", "Regularly"]', 'survey2_id', 1, NOW(), NOW()),
('question3_id', 'What is your favorite movie genre?', '["Action", "Comedy", "Drama"]', 'survey3_id', 1, NOW(), NOW()),
('question4_id', 'Do you prefer tea or coffee?', '["Tea", "Coffee"]', 'survey4_id', 1, NOW(), NOW()),
('question5_id', 'How many hours of sleep do you get?', '["Less than 6", "6-8", "More than 8"]', 'survey5_id', 1, NOW(), NOW()),
('question6_id', 'What is your preferred mode of transportation?', '["Car", "Bus", "Walk"]', 'survey6_id', 1, NOW(), NOW()),
('question7_id', 'Are you a morning person or a night owl?', '["Morning Person", "Night Owl"]', 'survey7_id', 1, NOW(), NOW()),
('question8_id', 'Do you enjoy cooking?', '["Yes", "No"]', 'survey8_id', 1, NOW(), NOW()),
('question9_id', 'What type of books do you like?', '["Fiction", "Non-Fiction", "Sci-Fi"]', 'survey9_id', 1, NOW(), NOW()),
('question10_id', 'What is your favorite holiday destination?', '["Beach", "Mountain", "City"]', 'survey10_id', 1, NOW(), NOW());

-- Data insertion for 'responses' table
INSERT INTO responses (id, bio, timestamp, answers, survey_id, created_at, updated_at)
VALUES
('response1_id', '{"age": 25, "gender": "Male"}', NOW(), '{"question1_id": "Red"}', 'survey1_id', NOW(), NOW()),
('response2_id', '{"age": 30, "gender": "Female"}', NOW(), '{"question2_id": "Regularly"}', 'survey2_id', NOW(), NOW()),
('response3_id', '{"age": 35, "gender": "Non-Binary"}', NOW(), '{"question3_id": "Action"}', 'survey3_id', NOW(), NOW()),
('response4_id', '{"age": 40, "gender": "Male"}', NOW(), '{"question4_id": "Coffee"}', 'survey4_id', NOW(), NOW()),
('response5_id', '{"age": 28, "gender": "Female"}', NOW(), '{"question5_id": "6-8"}', 'survey5_id', NOW(), NOW()),
('response6_id', '{"age": 32, "gender": "Male"}', NOW(), '{"question6_id": "Car"}', 'survey6_id', NOW(), NOW()),
('response7_id', '{"age": 27, "gender": "Female"}', NOW(), '{"question7_id": "Morning Person"}', 'survey7_id', NOW(), NOW()),
('response8_id', '{"age": 45, "gender": "Male"}', NOW(), '{"question8_id": "Yes"}', 'survey8_id', NOW(), NOW()),
('response9_id', '{"age": 30, "gender": "Female"}', NOW(), '{"question9_id": "Fiction"}', 'survey9_id', NOW(), NOW()),
('response10_id', '{"age": 35, "gender": "Male"}', NOW(), '{"question10_id": "Beach"}', 'survey10_id', NOW(), NOW());

-- Data insertion for 'surveycategory' table
INSERT INTO surveycategory (survey_id, category_id, created_at, updated_at)
VALUES
('survey1_id', 'category1_id', NOW(), NOW()),
('survey2_id', 'category2_id', NOW(), NOW()),
('survey3_id', 'category3_id', NOW(), NOW()),
('survey4_id', 'category4_id', NOW(), NOW()),
('survey5_id', 'category5_id', NOW(), NOW()),
('survey6_id', 'category6_id', NOW(), NOW()),
('survey7_id', 'category7_id', NOW(), NOW()),
('survey8_id', 'category8_id', NOW(), NOW()),
('survey9_id', 'category9_id', NOW(), NOW()),
('survey10_id', 'category10_id', NOW(), NOW());

/*!40101 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
