-- CREATE DESTINATION TABLES
CREATE DATABASE IF NOT EXISTS `$DATABASE$`;
USE `$DATABASE$`;

DROP TABLE IF EXISTS `$PREFIX$authors`;
CREATE TABLE `$PREFIX$authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(255) NOT NULL DEFAULT '',
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `doNotImport` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `$PREFIX$bookmarks`;
CREATE TABLE `$PREFIX$bookmarks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `authorId` int(11) DEFAULT '0',
  `rating` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `date` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT '',
  `tags` varchar(1024) NOT NULL DEFAULT '',
  `warnings` varchar(1024) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `donotimport` tinyint(1) NOT NULL DEFAULT '0',
  `ao3url` varchar(255) DEFAULT NULL,
  `brokenlink` tinyint(1) DEFAULT '0',
  `importnotes` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `authorId` (`authorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `$PREFIX$chapters`;
CREATE TABLE `$PREFIX$chapters` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Position` bigint(22) DEFAULT NULL,
  `Title` varchar(255) NOT NULL DEFAULT '',
  `AuthorID` int(11) NOT NULL DEFAULT '0',
  `Text` mediumtext,
  `Date` datetime DEFAULT NULL,
  `StoryID` int(11) NOT NULL DEFAULT '0',
  `Notes` text,
  `Url` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `id_UNIQUE` (`ID`),
  KEY `storyid` (`StoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `$PREFIX$stories`;
CREATE TABLE `$PREFIX$stories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `authorId` int(11) DEFAULT '0',
  `coauthorId` int(11) DEFAULT '0',
  `rating` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `date` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT '',
  `tags` varchar(1024) NOT NULL DEFAULT '',
  `warnings` varchar(1024) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `donotimport` tinyint(1) NOT NULL DEFAULT '0',
  `ao3url` varchar(255) DEFAULT NULL,
  `importnotes` varchar(1024) DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `authorId` (`authorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
