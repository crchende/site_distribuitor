/*drop database site_distribuitor; */ /* daca se doreste si stergerea bazei de date */
CREATE DATABASE  IF NOT EXISTS `site_distribuitor` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `site_distribuitor`;
-- MySQL dump 10.19  Distrib 10.3.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: site_distribuitor
-- ------------------------------------------------------
-- Server version	10.3.34-MariaDB-0ubuntu0.20.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `comenzi`
--

DROP TABLE IF EXISTS `comenzi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comenzi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_producator` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_producatori_idx` (`id_producator`),
  CONSTRAINT `id_producatori` FOREIGN KEY (`id_producator`) REFERENCES `producatori` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comenzi`
--

LOCK TABLES `comenzi` WRITE;
/*!40000 ALTER TABLE `comenzi` DISABLE KEYS */;
INSERT INTO `comenzi` VALUES (1,1),(2,2),(3,3);
/*!40000 ALTER TABLE `comenzi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `continut_comenzi_la_producatori`
--

DROP TABLE IF EXISTS `continut_comenzi_la_producatori`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `continut_comenzi_la_producatori` (
  `id_comanda` int(11) NOT NULL,
  `id_produs` int(11) NOT NULL,
  `cantitate` int(11) NOT NULL,
  PRIMARY KEY (`id_comanda`,`id_produs`),
  KEY `id_produs_idx` (`id_produs`),
  CONSTRAINT `id_comanda` FOREIGN KEY (`id_comanda`) REFERENCES `comenzi` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `id_produs` FOREIGN KEY (`id_produs`) REFERENCES `produse` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `producatori` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nume` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nume_UNIQUE` (`nume`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `produse` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_producator` int(11) NOT NULL,
  `nume` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_producator_idx` (`id_producator`),
  CONSTRAINT `id_producator` FOREIGN KEY (`id_producator`) REFERENCES `producatori` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produse`
--

LOCK TABLES `produse` WRITE;
/*!40000 ALTER TABLE `produse` DISABLE KEYS */;
INSERT INTO `produse` VALUES (1,1,'Ciocolata cu lapte'),(2,1,'Ciocolata cu alune'),(3,2,'Ciocolata cu iaurt'),(4,2,'Ciocolata cu caramel sarat'),(5,2,'Ciocolata cu biscuiti'),(6,2,'Ciocolata amaruie'),(7,3,'Ciocolata cu fructe de padure'),(8,3,'Ciocolata cu lapte');
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

-- Dump completed on 2022-07-20 22:47:55
