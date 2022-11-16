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
);

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
);

INSERT INTO tags VALUES (10,989,'original-tag-1','classes',NULL,'','','','',''),(11,345,'original-tag-2','classes',NULL,'','','','','');