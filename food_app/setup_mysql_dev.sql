-- Prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS `food_mania_db`;
CREATE USER IF NOT EXISTS 'food_mania'@'localhost' IDENTIFIED BY 'food_mania_pwd';
GRANT ALL PRIVILEGES ON `food_mania_db`.* TO 'food_mania'@'localhost';
GRANT SELECT ON performance_schema.* TO 'food_mania'@'localhost';