USE users_db;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN` (`username`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
