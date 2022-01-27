USE users_db;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(128) NOT NULL,
  `password` varchar(128) NOT NULL,
  `role` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_UN` (`username`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

LOCK TABLES `users` WRITE;

INSERT INTO
  `users`
VALUES
    (1, 'xenojohn','$2y$10$S1a59TKiFxK80XZLp07sHeTRIbx8IdAk7SVkCidGsn/2OLqwswtpC','User'),
    (2, 'xenoadmin','$2y$10$S1a59TKiFxK80XZLp07sHeTRIbx8IdAk7SVkCidGsn/2OLqwswtpC','Admin');

UNLOCK TABLES;