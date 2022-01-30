# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Generation Time: 2018-12-02 17:38:44 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE IF NOT EXISTS $DATABASE$;
USE $DATABASE$;

# Dump of table authors
# ------------------------------------------------------------

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



# Dump of table chapters
# ------------------------------------------------------------

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



# Dump of table stories
# ------------------------------------------------------------

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
  `tags` varchar(1024) NOT NULL DEFAULT '',
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



# Dump of table story_links
# ------------------------------------------------------------

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
  `tags` varchar(1024) NOT NULL DEFAULT '',
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




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
