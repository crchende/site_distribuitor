-- MySQL dump 10.13  Distrib 8.0.30, for Linux (x86_64)
--
-- Host: localhost    Database: site_distribuitor
-- ------------------------------------------------------
-- Server version	8.0.30

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comenzi_la_producatori`
--

-- **********************************************

DROP TABLE IF EXISTS `comenzi_la_producatori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comenzi_la_producatori` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `id_producator` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_comenzi_la_producatori_1_idx` (`id_producator`),
  CONSTRAINT `fk_comenzi_la_producatori_1` FOREIGN KEY (`id_producator`) REFERENCES `producatori` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comenzi_la_producatori`
--

LOCK TABLES `comenzi_la_producatori` WRITE;
/*!40000 ALTER TABLE `comenzi_la_producatori` DISABLE KEYS */;
INSERT INTO `comenzi_la_producatori` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `comenzi_la_producatori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `continut_comenzi_la_producatori`
--

DROP TABLE IF EXISTS `continut_comenzi_la_producatori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `continut_comenzi_la_producatori` (
  `id_comanda` int unsigned NOT NULL,
  `id_produs` int unsigned NOT NULL,
  `cantitate` int NOT NULL,
  PRIMARY KEY (`id_comanda`,`id_produs`),
  KEY `fk_continut_comenzi_la_producatori_2_idx` (`id_produs`),
  CONSTRAINT `fk_continut_comenzi_la_producatori_1` FOREIGN KEY (`id_comanda`) REFERENCES `comenzi_la_producatori` (`id`),
  CONSTRAINT `fk_continut_comenzi_la_producatori_2` FOREIGN KEY (`id_produs`) REFERENCES `produse` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `continut_comenzi_la_producatori`
--

LOCK TABLES `continut_comenzi_la_producatori` WRITE;
/*!40000 ALTER TABLE `continut_comenzi_la_producatori` DISABLE KEYS */;
INSERT INTO `continut_comenzi_la_producatori` VALUES (1,1,100),(1,2,150),(2,3,200),(2,4,250),(3,7,50);
/*!40000 ALTER TABLE `continut_comenzi_la_producatori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producatori`
--

DROP TABLE IF EXISTS `producatori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producatori` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `nume` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  UNIQUE KEY `nume_UNIQUE` (`nume`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producatori`
--

LOCK TABLES `producatori` WRITE;
/*!40000 ALTER TABLE `producatori` DISABLE KEYS */;
INSERT INTO `producatori` VALUES (2,'Kandia'),(3,'Milka'),(1,'Poiana');
/*!40000 ALTER TABLE `producatori` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produse`
--

DROP TABLE IF EXISTS `produse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produse` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `id_producator` int unsigned NOT NULL,
  `nume` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_produse_1_idx` (`id_producator`),
  CONSTRAINT `fk_produse_1` FOREIGN KEY (`id_producator`) REFERENCES `producatori` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produse`
--

LOCK TABLES `produse` WRITE;
/*!40000 ALTER TABLE `produse` DISABLE KEYS */;
INSERT INTO `produse` VALUES (1,1,'Ciocolata cu lapte'),(2,1,'Ciocolata cu alune'),(3,2,'Ciocolata cu iaurt'),(4,2,'Ciocolata cu caramel sarat'),(5,2,'Ciocolata cu biscuiti'),(6,2,'Ciocolata amaruie'),(7,3,'Cicolata cu fructe de padure'),(8,3,'Ciocolata cu lapte');
/*!40000 ALTER TABLE `produse` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-07-28 16:05:01
