-- MySQL dump 10.17  Distrib 10.3.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 192.168.1.5    Database: order_manager_sandbox
-- ------------------------------------------------------
-- Server version	8.0.13

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `claims`
--

DROP TABLE IF EXISTS `claims`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `claims` (
  `customerFirstName` text,
  `customerLastName` text,
  `customerPhoneNo` bigint(20) DEFAULT NULL,
  `customerEmail` text,
  `productDesc` text,
  `productPartNo` text,
  `productSupplier` text,
  `dateRequested` date DEFAULT NULL,
  `dateOrdered` date DEFAULT NULL,
  `orderID` bigint(20) DEFAULT NULL,
  `orderStatus` tinyint(4) DEFAULT NULL,
  `orderDesc` text,
  `paymentStatus` tinyint(4) DEFAULT NULL,
  `isWorkOrder` tinyint(1) DEFAULT NULL,
  `salesRep` text,
  `objectID` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `dimLength` int(11) DEFAULT NULL,
  `dimWidth` int(11) DEFAULT NULL,
  `dimHeight` int(11) DEFAULT NULL,
  `raNumber` text,
  `probDesc` text,
  `dateRecieved` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `claims`
--

LOCK TABLES `claims` WRITE;
/*!40000 ALTER TABLE `claims` DISABLE KEYS */;
/*!40000 ALTER TABLE `claims` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `customerFirstName` text,
  `customerLastName` text,
  `customerPhoneNo` bigint(20) DEFAULT NULL,
  `customerEmail` text,
  `productDesc` text,
  `productPartNo` text,
  `productSupplier` text,
  `dateRequested` date DEFAULT NULL,
  `dateOrdered` date DEFAULT NULL,
  `orderID` bigint(20) DEFAULT NULL,
  `orderStatus` tinyint(4) DEFAULT NULL,
  `orderDesc` text,
  `paymentStatus` tinyint(4) DEFAULT NULL,
  `isWorkOrder` tinyint(1) DEFAULT NULL,
  `salesRep` text,
  `objectID` int(11) DEFAULT NULL,
  `price` float DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `dimLength` int(11) DEFAULT NULL,
  `dimWidth` int(11) DEFAULT NULL,
  `dimHeight` int(11) DEFAULT NULL,
  `qty` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-05 17:43:20
