-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS guidy_test_db;
CREATE USER IF NOT EXISTS 'guidy_test'@'localhost' IDENTIFIED BY 'Pa$$w0rdtest';
GRANT ALL PRIVILEGES ON `guidy_test_db`.* TO 'guidy_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'guidy_test'@'localhost';
FLUSH PRIVILEGES;
