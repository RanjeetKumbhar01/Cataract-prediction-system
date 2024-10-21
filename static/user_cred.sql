CREATE DATABASE user_management;

USE user_management;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    age INT DEFAULT NULL,
    user_type ENUM('patient', 'staff') NOT NULL,
    hospital_name VARCHAR(255) DEFAULT NULL 
    
);
show tables;
desc users;
-- drop table users;
select * from users;

SET SQL_SAFE_UPDATES = 0;
DELETE FROM users WHERE name = '@434';
SET SQL_SAFE_UPDATES = 1;