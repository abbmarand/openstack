CREATE DATABASE IF NOT EXISTS wp;
CREATE USER IF NOT EXISTS 'wp'@'%' IDENTIFIED BY 'secret'; 
GRANT ALL PRIVILEGES ON wp.* TO 'wp'@'%';