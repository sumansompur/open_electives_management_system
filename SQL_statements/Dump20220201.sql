CREATE DATABASE  IF NOT EXISTS `open_electives` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `open_electives`;
-- MySQL dump 10.13  Distrib 8.0.27, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: open_electives
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `department_code` varchar(5) NOT NULL,
  `department_name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`department_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES ('CIV','Civil Engineering'),('CSE','Computer Science and Engineering'),('ISE','Information Science and Engineering'),('MEC','Mechanical Engineer');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `open_elective`
--

DROP TABLE IF EXISTS `open_elective`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `open_elective` (
  `subject_code` varchar(8) NOT NULL,
  `elective_name` varchar(25) DEFAULT NULL,
  `department_code` varchar(5) NOT NULL,
  `teacher_code` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`subject_code`,`department_code`),
  KEY `fk_oe_teach_code` (`teacher_code`),
  KEY `fk_oe_dept_code` (`department_code`),
  CONSTRAINT `fk_oe_dept_code` FOREIGN KEY (`department_code`) REFERENCES `department` (`department_code`),
  CONSTRAINT `fk_oe_teach_code` FOREIGN KEY (`teacher_code`) REFERENCES `teacher` (`teacher_code`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `open_elective`
--

LOCK TABLES `open_elective` WRITE;
/*!40000 ALTER TABLE `open_elective` DISABLE KEYS */;
INSERT INTO `open_elective` VALUES ('18CS61','ABCD','CSE','BI101'),('18CS62','ABCDE','CSE','BI101'),('18CS62','ABCDEFG','ISE','BI103'),('18CS63','ABCDEF','ISE','BI102'),('18CS64','XYZJD','CSE','BI102');
/*!40000 ALTER TABLE `open_elective` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `student`
--

DROP TABLE IF EXISTS `student`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `student` (
  `usn` varchar(10) NOT NULL,
  `sname` varchar(25) DEFAULT NULL,
  `semester` int DEFAULT NULL,
  `section` char(1) DEFAULT NULL,
  `subject_code` varchar(8) DEFAULT NULL,
  `department_code` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`usn`),
  KEY `fk_stu_sub` (`subject_code`),
  KEY `fk_stu_dcode` (`department_code`),
  CONSTRAINT `fk_stu_dcode` FOREIGN KEY (`department_code`) REFERENCES `department` (`department_code`),
  CONSTRAINT `fk_stu_sub` FOREIGN KEY (`subject_code`) REFERENCES `open_elective` (`subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES ('1BI19CS158','Sujan',5,'C','18CS62','CSE'),('1BI19CS159','Suman',5,'C','18CS63','CSE'),('1BI19Cs186','Vinayaka',5,'C',NULL,'CSE');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `teacher_code` varchar(10) NOT NULL,
  `tname` varchar(25) DEFAULT NULL,
  `department_code` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`teacher_code`),
  KEY `fk_teacher_dept_code` (`department_code`),
  CONSTRAINT `fk_teacher_dept_code` FOREIGN KEY (`department_code`) REFERENCES `department` (`department_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('BI101','MCV','CSE'),('BI102','MBV','CSE'),('BI103','SBR','ISE'),('BI104','XYZ','CSE');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` varchar(15) NOT NULL,
  `user_name` varchar(25) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `password_hash` varchar(100) DEFAULT NULL,
  `user_privileges` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('1BI19CS158','Sujan H C','sujan@gmail.com','123456','Student'),('1BI19CS159','Suman T D','sumansompur@gmail.com','suman123','Student'),('admin','Admin','admin.bit@gmail.com','123456','Admin'),('BI101','Mahalakshmi CV','mahalakshmi@gmail.com','123456','Teacher'),('CSE','CSE','cse.bit@gmail.com','123456','Department'),('ISE','ISE','ise.bit@gmail.com','123456','Department');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'open_electives'
--

--
-- Dumping routines for database 'open_electives'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-01  2:36:33
