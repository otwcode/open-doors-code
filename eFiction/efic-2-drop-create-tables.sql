-- REPLACE "PREFIX" and "DATABASE"

use DATABASE;

-- DROP TABLES WE DON'T IMPORT (some many not exist in all versions of eFiction)
DROP TABLE `1fanfiction_settings`;
DROP TABLE `2songs`;
DROP TABLE `desire_fanfiction_settings`;
DROP TABLE `desirefanfiction_settings`;
DROP TABLE `fanfiction_authorfields`;
DROP TABLE `fanfiction_authorinfo`;
DROP TABLE `fanfiction_authorprefs`;
DROP TABLE `fanfiction_blocks`;
DROP TABLE `fanfiction_challenges`;
DROP TABLE `fanfiction_codeblocks`;
DROP TABLE `fanfiction_comments`;
DROP TABLE `fanfiction_favauth`;
DROP TABLE `fanfiction_favorites`;
DROP TABLE `fanfiction_favstor`;
DROP TABLE `fanfiction_log`;
DROP TABLE `fanfiction_messages`;
DROP TABLE `fanfiction_modules`;
DROP TABLE `fanfiction_news`;
DROP TABLE `fanfiction_online`;
DROP TABLE `fanfiction_pagelinks`;
DROP TABLE `fanfiction_panels`;
DROP TABLE `fanfiction_poll`;
DROP TABLE `fanfiction_poll_votes`;
DROP TABLE `fanfiction_reviews`;
DROP TABLE `fanfiction_settings`;
DROP TABLE `fanfiction_shoutbox`;
DROP TABLE `fanfiction_stats`;
DROP TABLE `fanfiction_tracker`;
DROP TABLE `fiction_settings_old`;
DROP TABLE `sd1_songs`;
DROP TABLE `sd_songs`;
DROP TABLE `sendsongs`;
DROP TABLE `settingsfanfiction_settings`;
DROP TABLE `wincest_fanfiction_settings`;

-- ALTER TABLES
ALTER TABLE `fanfiction_authors` 
DROP COLUMN `password`,
DROP COLUMN `admincreated`,
DROP COLUMN `date`,
DROP COLUMN `image`,
DROP COLUMN `bio`,
DROP COLUMN `website`,
DROP COLUMN `realname`,
CHANGE COLUMN `uid` `id` INT(11) NOT NULL AUTO_INCREMENT ,
CHANGE COLUMN `penname` `name` VARCHAR(200) NOT NULL DEFAULT '' ,
ADD COLUMN `imported` TINYINT(1) NULL DEFAULT 0 AFTER `email`,
ADD COLUMN `doNotImport` TINYINT(1) NULL DEFAULT 0 AFTER `imported`,
DROP INDEX `admincreated`;

ALTER TABLE `fanfiction_chapters` 
DROP COLUMN `count`,
DROP COLUMN `reviews`,
DROP COLUMN `rating`,
DROP COLUMN `wordcount`,
DROP COLUMN `validated`,
CHANGE COLUMN `inorder` `position` INT(11) NOT NULL DEFAULT '0' AFTER `id`,
CHANGE COLUMN `uid` `authorid` INT(11) NOT NULL DEFAULT '0' AFTER `title`,
CHANGE COLUMN `storytext` `text` LONGTEXT NULL DEFAULT NULL AFTER `authorid`,
CHANGE COLUMN `sid` `storyid` INT(11) NOT NULL DEFAULT '0' AFTER `text`,
CHANGE COLUMN `chapid` `id` INT(11) NOT NULL AUTO_INCREMENT ,
CHANGE COLUMN `title` `title` VARCHAR(255) NOT NULL DEFAULT '' ,
ADD COLUMN `url` VARCHAR(1024) NULL DEFAULT NULL AFTER `endnotes`,
ADD COLUMN `date` DATETIME NULL AFTER `url`,
DROP INDEX `forstoryblock` ,
DROP INDEX `validated` ,
DROP INDEX `title` ,
DROP INDEX `inorder`,
DROP INDEX `uid` ;

ALTER TABLE `fanfiction_stories` 
DROP COLUMN `counter`,
DROP COLUMN `numreviews`,
DROP COLUMN `wordcount`,
DROP COLUMN `rr`,
DROP COLUMN `completed`,
DROP COLUMN `validated`,
DROP COLUMN `featured`,
CHANGE COLUMN `sid` `id` INT(11) NOT NULL AUTO_INCREMENT ,
CHANGE COLUMN `psid` `id` INT(11) NOT NULL AUTO_INCREMENT ,
CHANGE COLUMN `title` `title` VARCHAR(255) NOT NULL DEFAULT 'Untitled' ,
CHANGE COLUMN `storynotes` `notes` TEXT NULL DEFAULT NULL ,
CHANGE COLUMN `gid` `tags` VARCHAR(1024) NULL DEFAULT NULL ,
CHANGE COLUMN `charid` `characters` VARCHAR(1024) NULL DEFAULT NULL ,
CHANGE COLUMN `rid` `rating` VARCHAR(25) NOT NULL DEFAULT '' ,
CHANGE COLUMN `updated` `updated` DATETIME NULL DEFAULT NULL ,
CHANGE COLUMN `uid` `authorid` INT(11) NOT NULL DEFAULT '0' ,
CHANGE COLUMN `date` `date` DATETIME NULL DEFAULT NULL ,
CHANGE COLUMN `wid` `warnings` varchar(255) DEFAULT NULL,
CHANGE COLUMN `inorder` `position` INT(11) NOT NULL DEFAULT '0' AFTER `id`,
ADD COLUMN `fandoms` varchar(255) DEFAULT NULL,
ADD COLUMN `relationships` varchar(1024) DEFAULT NULL,
CHANGE COLUMN `catid` `categories` varchar(1024) DEFAULT NULL,
ADD COLUMN `url` varchar(255) DEFAULT NULL,
ADD COLUMN `imported` tinyint(1) NOT NULL DEFAULT '0',
ADD COLUMN `doNotImport` tinyint(1) NOT NULL DEFAULT '0',
ADD COLUMN `Ao3Url` varchar(255) DEFAULT NULL,
DROP INDEX `gid` ,
DROP INDEX `charid` ,
DROP INDEX `wid` ,
DROP INDEX `rid` ,
DROP INDEX `rr` ,
DROP INDEX `completed` ,
DROP INDEX `featured` ,
DROP INDEX `catid` ;

-- OPTIONAL: CREATE chapters table if not present
CREATE TABLE IF NOT EXISTS `fanfiction_chapters` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `position` int(11) NOT NULL DEFAULT '0',
  `title` varchar(255) NOT NULL DEFAULT '',
  `authorid` int(11) NOT NULL DEFAULT '0',
  `text` longtext,
  `storyid` int(11) NOT NULL DEFAULT '0',
  `notes` text,
  `endnotes` text,
  `url` varchar(1024) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sid` (`storyid`)
);

CREATE TABLE `fanfiction_bookmarks` (
  `id` int(11) NOT NULL DEFAULT '0',
  `title` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `authorId` int(11) DEFAULT '0',
  `rating` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `date` date DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT '',
  `tags` varchar(1024) NOT NULL DEFAULT '',
  `warnings` varchar(255) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `donotimport` tinyint(1) NOT NULL DEFAULT '0',
  `ao3url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `authorId` (`authorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


-- CREATE DESTINATION TABLES

use od_sgf;

CREATE TABLE `PREFIX_authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL DEFAULT '',
  `email` varchar(255) NOT NULL DEFAULT '',
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `doNotImport` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `PREFIX_bookmarks` (
  `id` int(11) NOT NULL DEFAULT '0',
  `title` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `authorId` int(11) DEFAULT '0',
  `rating` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `date` date DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT '',
  `tags` varchar(1024) NOT NULL DEFAULT '',
  `warnings` varchar(255) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `donotimport` tinyint(1) NOT NULL DEFAULT '0',
  `ao3url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `authorId` (`authorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `PREFIX_chapters` (
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

CREATE TABLE `PREFIX_stories` (
  `id` int(11) NOT NULL DEFAULT '0',
  `title` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `summary` text,
  `notes` text,
  `authorId` int(11) DEFAULT '0',
  `rating` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `date` datetime DEFAULT NULL,
  `updated` datetime DEFAULT NULL,
  `categories` varchar(45) DEFAULT '',
  `tags` varchar(1024) NOT NULL DEFAULT '',
  `warnings` varchar(255) DEFAULT '',
  `fandoms` varchar(255) DEFAULT '',
  `characters` varchar(1024) DEFAULT '',
  `relationships` varchar(1024) DEFAULT '',
  `url` varchar(255) DEFAULT NULL,
  `imported` tinyint(1) NOT NULL DEFAULT '0',
  `donotimport` tinyint(1) NOT NULL DEFAULT '0',
  `ao3url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `authorId` (`authorId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;