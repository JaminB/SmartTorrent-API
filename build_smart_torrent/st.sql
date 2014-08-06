DROP DATABASE cache;
CREATE DATABASE cache;
USE cache;
CREATE TABLE searches(id varchar(32), data LONGTEXT);
CREATE USER 'st'@'localhost' IDENTIFIED BY 'tech0nsite!';
CREATE USER 'st'@'%' IDENTIFIED BY 'tech0nsite!';
GRANT ALL PRIVILEGES ON *.* TO 'st'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'st'@'localhost';

