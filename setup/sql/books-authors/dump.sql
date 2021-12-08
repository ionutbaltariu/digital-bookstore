-- MariaDB dump 10.19  Distrib 10.6.4-MariaDB, for osx10.16 (arm64)
--
-- Host: localhost    Database: bookstore
-- ------------------------------------------------------
-- Server version	10.6.4-MariaDB
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */
;

/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */
;

/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */
;

/*!40101 SET NAMES utf8mb4 */
;

/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */
;

/*!40103 SET TIME_ZONE='+00:00' */
;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */
;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */
;

/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */
;

/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */
;

--
-- Table structure for table `authors`
--
USE bookstore;
DROP TABLE IF EXISTS `authors`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!40101 SET character_set_client = utf8 */
;

CREATE TABLE `authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `authors_UN` (`first_name`, `last_name`)
) ENGINE = InnoDB AUTO_INCREMENT = 15 DEFAULT CHARSET = utf8mb4;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `authors`
--
LOCK TABLES `authors` WRITE;

/*!40000 ALTER TABLE `authors` DISABLE KEYS */
;

INSERT INTO
  `authors`
VALUES
  (7, 'Alfred', 'Whitehead'),
  (8, 'Bertrand', 'Russel'),
  (1, 'Robert C.', 'Martin');

/*!40000 ALTER TABLE `authors` ENABLE KEYS */
;

UNLOCK TABLES;

--
-- Table structure for table `books`
--
DROP TABLE IF EXISTS `books`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!40101 SET character_set_client = utf8 */
;

CREATE TABLE `books` (
  `isbn` varchar(100) NOT NULL,
  `title` varchar(100) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `year_of_publishing` int(11) NOT NULL,
  `genre` varchar(100) NOT NULL,
  `price` double(5, 2) NOT NULL,
  `stock` int(11) NOT NULL,
  PRIMARY KEY (`isbn`),
  UNIQUE KEY `books_UN` (`title`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `books`
--
LOCK TABLES `books` WRITE;

/*!40000 ALTER TABLE `books` DISABLE KEYS */
;

INSERT INTO
  `books`
VALUES
  (
    '9780132350884',
    'Clean Code',
    'Prentice Hall',
    2009,
    'Computer Science',
    49.50,
    5
  ),
  (
    '9780511623585',
    'Principia Mathematica',
    'Cambridge University Press',
    1912,
    'Pure Mathematics',
    89.99,
    1
  ),
  (
    '9781628251999',
    'Agile Practic Guide',
    'Project Management Institute',
    2017,
    'Computer Science',
    70.00,
    2
  );

/*!40000 ALTER TABLE `books` ENABLE KEYS */
;

UNLOCK TABLES;

--
-- Table structure for table `books-authors`
--
DROP TABLE IF EXISTS `books-authors`;

/*!40101 SET @saved_cs_client     = @@character_set_client */
;

/*!40101 SET character_set_client = utf8 */
;

CREATE TABLE `books-authors` (
  `isbn` varchar(100) NOT NULL,
  `author_id` int(11) NOT NULL,
  `index` int(11) NOT NULL,
  PRIMARY KEY (`isbn`, `author_id`),
  KEY `books_authors_FK_1` (`author_id`),
  CONSTRAINT `books_authors_FK` FOREIGN KEY (`isbn`) REFERENCES `books` (`isbn`) ON DELETE CASCADE,
  CONSTRAINT `books_authors_FK_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

/*!40101 SET character_set_client = @saved_cs_client */
;

--
-- Dumping data for table `books-authors`
--
LOCK TABLES `books-authors` WRITE;

/*!40000 ALTER TABLE `books-authors` DISABLE KEYS */
;

INSERT INTO
  `books-authors`
VALUES
  ('9780132350884', 1, 2),
  ('9780511623585', 7, 3),
  ('9780511623585', 8, 1);

/*!40000 ALTER TABLE `books-authors` ENABLE KEYS */
;

UNLOCK TABLES;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */
;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */
;

/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */
;

/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */
;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */
;

/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */
;

/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */
;

/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */
;

-- Dump completed on 2021-11-04 20:23:46
