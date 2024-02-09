-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dc_dev_db;
CREATE USER IF NOT EXISTS 'dc_dev'@'localhost' IDENTIFIED BY 'dc_dev_pwd';
GRANT ALL PRIVILEGES ON `dc_dev_db`.* TO 'dc_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dc_dev'@'localhost';
FLUSH PRIVILEGES;
