-- Drop database if exists
DROP DATABASE IF EXISTS rest_api_ims_db;

-- Delete user if exists
-- DROP USER IF EXISTS 'ims_db_dev'@'localhost';

-- Create database and user if not exists
CREATE DATABASE IF NOT EXISTS rest_api_ims_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'rest_api_ims_db_user'@'localhost' IDENTIFIED BY 'rest_api_ims_db_pwd';
GRANT ALL ON rest_api_ims_db.* TO 'rest_api_ims_db_user'@'localhost';
GRANT SELECT ON performance_schema.* TO 'rest_api_ims_db_user'@'localhost';
FLUSH PRIVILEGES;

-- Switch to the newly created database
USE rest_api_ims_db;

-- Table structure for `users`
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` varchar(150) NOT NULL,
  `name` varchar(150) NOT NULL,
  `email` varchar(150) NOT NULL UNIQUE,
  `password` varchar(250) NOT NULL,
  `user_role` TINYINT DEFAULT 0 COMMENT '0 -> Employee, 1 -> Super Admin, 2 -> Admin, 3 -> Manager, 4 -> Sales Employee, 5 -> Finance',
  `active` TINYINT DEFAULT 1 COMMENT '0 -> False, 1 -> True',
  `deleted` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table structure for `settings`
DROP TABLE IF EXISTS `settings`;
CREATE TABLE `settings` (
  `id` int AUTO_INCREMENT NOT NULL,
  `user_id` varchar(150) NOT NULL,
  `create_store` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `view_store` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `edit_store` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `approve_store` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `create_product` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `view_product` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `edit_product` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `approve_product` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `create_user` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `view_user` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `edit_user` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `approve_user` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `create_setting` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `view_setting` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `edit_setting` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `approve_setting` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `create_sales_record` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `view_sales_record` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `edit_sales_record` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `approve_sales_record` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `create_account` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `view_account` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `edit_account` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `approve_account` TINYINT DEFAULT 0 COMMENT '0 -> False, 1 -> True',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_users_user_id` (`user_id`),
  CONSTRAINT `fk_users_user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- INSERT INTO `users`(id, name, email, password) 
-- VALUES('f35cdf6d-9dbf-4ad1-b201-654d9c4b0cdd', 'Admin user', 'admin@test.com', '81dc9bdb52d04dc20036dbd8313ed055', 2);

-- To view table's comments
-- SELECT COLUMN_NAME, COLUMN_COMMENT FROM information_schema.columns WHERE table_schema='databse_name' AND TABLE_NAME='table_name';
