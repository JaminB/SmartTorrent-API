CREATE DATABASE IF NOT EXISTS cache;
USE cache;
CREATE TABLE IF NOT EXISTS searches(id varchar(32), data LONGTEXT);
CREATE DATABASE IF NOT EXISTS searches;
USE searches;
CREATE TABLE IF NOT EXISTS search_log(ID varchar(32), Term varchar(100), Category varchar(15), PRIMARY KEY (ID));
#CREATE USER 'st'@'localhost' IDENTIFIED BY 'whateveryouwant';
GRANT ALL ON  `database`.* TO 'st'@'localhost' IDENTIFIED BY 'whateveryouwant';
GRANT ALL ON  `database`.* TO 'st'@'%' IDENTIFIED BY 'whateveryouwant';
#CREATE USER 'st'@'%' IDENTIFIED BY 'whateveryouwant';
#GRANT ALL PRIVILEGES ON *.* TO 'st'@'%';
#GRANT ALL PRIVILEGES ON *.* TO 'st'@'localhost';

