DROP DATABASE IF EXISTS test_working_open_doors;
CREATE DATABASE test_working_open_doors;
USE test_working_open_doors;
CREATE TABLE item_tags (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int DEFAULT NULL,
  `item_type` enum('story','story_link','chapter') DEFAULT NULL,
  `tag_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) -- ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO item_tags VALUES (1,333,'story',10),(2,444,'story',10),(3,333,'story',11),(4,444,'story',11),(5,555,'story',11);

CREATE TABLE tags (
  `id` int NOT NULL AUTO_INCREMENT,
  `original_tagid` int DEFAULT NULL,
  `original_tag` varchar(1024) DEFAULT NULL,
  `original_type` varchar(255) DEFAULT NULL,
  `original_parent` varchar(255) DEFAULT NULL,
  `original_description` varchar(1024) DEFAULT NULL,
  `ao3_tag` varchar(1024) DEFAULT NULL,
  `ao3_tag_type` varchar(255) DEFAULT NULL,
  `ao3_tag_category` varchar(255) DEFAULT NULL,
  `ao3_tag_fandom` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) -- ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;

INSERT INTO tags VALUES (10,989,'original-tag-1','classes',NULL,'','','','',''),(11,345,'original-tag-2','classes',NULL,'','','','','');
UE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_tags`
--

LOCK TABLES `item_tags` WRITE;
/*!40000 ALTER TABLE `item_tags` DISABLE KEYS */;
INSERT INTO `item_tags` VALUES (1,333,'story',10),(2,444,'story',10),(3,333,'story',11),(4,444,'story',11),(5,555,'story',11);
/*!40000 ALTER TABLE `item_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tags` (
  `id` int NOT NULL AUTO_INCREMENT,
  `original_tagid` int DEFAULT NULL,
  `original_tag` varchar(1024) DEFAULT NULL,
  `original_type` varchar(255) DEFAULT NULL,
  `original_parent` varchar(255) DEFAULT NULL,
  `original_description` varchar(1024) DEFAULT NULL,
  `ao3_tag` varchar(1024) DEFAULT NULL,
  `ao3_tag_type` varchar(255) DEFAULT NULL,
  `ao3_tag_category` varchar(255) DEFAULT NULL,
  `ao3_tag_fandom` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES (10,989,'original-tag-1','classes',NULL,'','','','',''),(11,345,'original-tag-2','classes',NULL,'','','','','');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-10-16 18:03:39
