DROP DATABASE IF EXISTS test_final_open_doors;
CREATE DATABASE test_final_open_doors;

USE test_final_open_doors;

CREATE TABLE IF NOT EXISTS `authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(255) NOT NULL DEFAULT '',
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `do_not_import` tinyint(1) NOT NULL DEFAULT '0',
  `to_delete` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE IF NOT EXISTS `chapters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position` bigint(22) DEFAULT NULL,
  `title` varchar(255) NOT NULL DEFAULT '',
  `author_id` int(11) NOT NULL DEFAULT '0',
  `text` mediumtext,
  `date` datetime DEFAULT NULL,
  `story_id` int(11) DEFAULT '0',
  `notes` text,
  `url` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `storyid` (`story_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `stories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `author_id` int(11) DEFAULT '0',
  `rating` varchar(255) NOT NULL DEFAULT '',
  `date` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT NULL,
  `tags` varchar(255) NOT NULL DEFAULT '',
  `warnings` varchar(255) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `language_code` varchar(5) DEFAULT 'en',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `do_not_import` tinyint(1) NOT NULL DEFAULT '0',
  `ao3_url` varchar(255) DEFAULT NULL,
  `import_notes` varchar(1024) DEFAULT '',
  `coauthor_id` int(11) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `authorId` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS `story_links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `author_id` int(11) DEFAULT '0',
  `rating` varchar(255) NOT NULL DEFAULT '',
  `date` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT NULL,
  `tags` varchar(255) NOT NULL DEFAULT '',
  `warnings` varchar(255) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `language_code` varchar(5) DEFAULT 'en',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `do_not_import` tinyint(1) NOT NULL DEFAULT '0',
  `ao3_url` varchar(255) DEFAULT NULL,
  `broken_link` tinyint(1) NOT NULL DEFAULT '0',
  `import_notes` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `authorId` (`author_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
