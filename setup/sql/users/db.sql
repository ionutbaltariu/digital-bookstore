USE users_db;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN` (`username`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE `user_profiles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `firstname` varchar(128),
  `lastname` varchar(128),
  `email` varchar(128),
  `address` varchar(128),
  `birthday` date,
  `userid` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_email` (`email`),
  UNIQUE KEY `unique_user_id` (`userid`),
  FOREIGN KEY (id) REFERENCES users(id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

LOCK TABLES `users` WRITE, `user_profiles` WRITE;

INSERT INTO
  `users`
VALUES
    (1, 'xenojohn','$2y$10$S1a59TKiFxK80XZLp07sHeTRIbx8IdAk7SVkCidGsn/2OLqwswtpC','User'),
    (2, 'xenoadmin','$2y$10$S1a59TKiFxK80XZLp07sHeTRIbx8IdAk7SVkCidGsn/2OLqwswtpC','Admin');

INSERT INTO 
  `user_profiles`
VALUES
  (1, 'John', 'Doe', 'a@b.c', 'Tg. Cucu, Iasi, Romania', '2000-05-31', 1);


UNLOCK TABLES;