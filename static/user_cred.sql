-- CREATE DATABASE user_management;
-- CREATE TABLE users (
--     id INT AUTO_INCREMENT PRIMARY KEY,
--     name VARCHAR(255) NOT NULL,
--     email VARCHAR(255) UNIQUE NOT NULL,
--     password VARCHAR(255) NOT NULL,
--     age INT DEFAULT NULL,
--     user_type ENUM('patient', 'staff') NOT NULL,
--     hospital_name VARCHAR(255) DEFAULT NULL 
--     
-- );
-- drop table users;
show tables;
desc users;
USE user_management;
select * from users;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM users WHERE name= 'ranjeet aaa';
SET SQL_SAFE_UPDATES = 1;