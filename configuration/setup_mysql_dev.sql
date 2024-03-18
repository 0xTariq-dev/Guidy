-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS guidy_dev_db;
CREATE USER IF NOT EXISTS 'guidy_dev'@'localhost' IDENTIFIED BY 'Pa$$w0rddev';
GRANT ALL PRIVILEGES ON `guidy_dev_db`.* TO 'guidy_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'guidy_dev'@'localhost';
FLUSH PRIVILEGES;
