# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.23)
# Database: efiction
# Generation Time: 2018-12-07 21:32:02 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

# These commands should be ignored by load_database!

CREATE DATABASE test_efiction_original_database_name_we_dont_want;
USE test_efiction_original_database_name_we_dont_want;


# Dump of table fanfiction_authorfields
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_authorfields`;

CREATE TABLE `fanfiction_authorfields` (
  `field_id` int(11) NOT NULL AUTO_INCREMENT,
  `field_type` tinyint(4) NOT NULL DEFAULT '0',
  `field_name` varchar(30) NOT NULL DEFAULT ' ',
  `field_title` varchar(255) NOT NULL DEFAULT ' ',
  `field_options` text,
  `field_code_in` text,
  `field_code_out` text,
  `field_on` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`field_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_authorfields` WRITE;
/*!40000 ALTER TABLE `fanfiction_authorfields` DISABLE KEYS */;

INSERT INTO `fanfiction_authorfields` (`field_id`, `field_type`, `field_name`, `field_title`, `field_options`, `field_code_in`, `field_code_out`, `field_on`)
VALUES
	(1,4,'lj','Live Journal','http://{info}.livejournal.com','','',0),
	(2,1,'website','Web Site','','','',1),
	(6,5,'Yahoo','Yahoo IM','','$output .= \"<div><label for=\'AOL\'>\".$field[\'field_title\'].\":</label><INPUT type=\'text\' class=\'textbox\'  name=\'af_\".$field[\'field_name\'].\"\' maxlength=\'40\' value=\'\".(!empty($user[\'af_\'.$field[\'field_id\']]) ? $user[\'af_\'.$field[\'field_id\']] : \"\").\"\' size=\'20\'></div>\";','$thisfield = \"<a href=\\\"http://edit.yahoo.com/config/send_webmesg?.target=\".$field[\'info\'].\"&.src=pg\\\"><img border=\'0\' src=\\\"http://opi.yahoo.com/online?u=\".$field[\'info\'].\"&m=g&t=1\\\"> \".format_email($field[\'info\']).\"</a>\";',1);

/*!40000 ALTER TABLE `fanfiction_authorfields` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_authorinfo
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_authorinfo`;

CREATE TABLE `fanfiction_authorinfo` (
  `uid` int(11) NOT NULL DEFAULT '0',
  `field` int(11) NOT NULL DEFAULT '0',
  `info` varchar(255) NOT NULL DEFAULT ' ',
  PRIMARY KEY (`uid`,`field`),
  KEY `uid` (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_authorinfo` WRITE;
/*!40000 ALTER TABLE `fanfiction_authorinfo` DISABLE KEYS */;

INSERT INTO `fanfiction_authorinfo` (`uid`, `field`, `info`)
VALUES
	(3,2,'http://example.com'),
	(4,3,'0'),
	(1,8,'No'),
	(5,8,'No'),
	(0,2,'http://example.com');

/*!40000 ALTER TABLE `fanfiction_authorinfo` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_authorprefs
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_authorprefs`;

CREATE TABLE `fanfiction_authorprefs` (
  `uid` int(11) NOT NULL DEFAULT '0',
  `newreviews` tinyint(1) NOT NULL DEFAULT '0',
  `newrespond` tinyint(1) NOT NULL DEFAULT '0',
  `ageconsent` tinyint(1) NOT NULL DEFAULT '0',
  `alertson` tinyint(1) NOT NULL DEFAULT '0',
  `tinyMCE` tinyint(1) NOT NULL DEFAULT '0',
  `sortby` tinyint(1) NOT NULL DEFAULT '0',
  `storyindex` tinyint(1) NOT NULL DEFAULT '0',
  `validated` tinyint(1) NOT NULL DEFAULT '0',
  `userskin` varchar(60) NOT NULL DEFAULT 'default',
  `level` tinyint(1) NOT NULL DEFAULT '0',
  `categories` varchar(200) NOT NULL DEFAULT '0',
  `contact` tinyint(1) NOT NULL DEFAULT '0',
  `stories` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_authorprefs` WRITE;
/*!40000 ALTER TABLE `fanfiction_authorprefs` DISABLE KEYS */;

INSERT INTO `fanfiction_authorprefs` (`uid`, `newreviews`, `newrespond`, `ageconsent`, `alertson`, `tinyMCE`, `sortby`, `storyindex`, `validated`, `userskin`, `level`, `categories`, `contact`, `stories`)
VALUES
	(1,0,0,1,0,0,0,0,0,'test',1,'0',1,0),
	(5,1,0,1,1,0,0,0,1,'BillBob',2,'0',1,77);

/*!40000 ALTER TABLE `fanfiction_authorprefs` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_authors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_authors`;

CREATE TABLE `fanfiction_authors` (
  `uid` int(11) NOT NULL AUTO_INCREMENT,
  `penname` varchar(200) NOT NULL DEFAULT '',
  `realname` varchar(200) NOT NULL DEFAULT '',
  `email` varchar(200) NOT NULL DEFAULT '',
  `website` varchar(200) NOT NULL DEFAULT '',
  `bio` text,
  `image` varchar(200) NOT NULL DEFAULT '',
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `admincreated` char(1) NOT NULL DEFAULT '0',
  `password` varchar(40) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`),
  KEY `penname` (`penname`),
  KEY `admincreated` (`admincreated`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_authors` WRITE;
/*!40000 ALTER TABLE `fanfiction_authors` DISABLE KEYS */;

INSERT INTO `fanfiction_authors` (`uid`, `penname`, `realname`, `email`, `website`, `bio`, `image`, `date`, `admincreated`, `password`)
VALUES
	(1,'Author1','Author1','A1@example.com','','','','2006-01-06 01:02:13','0','xfghtu'),
	(2,'B Author 2','B Author 2','B2@example.com','','','bauthor2','2006-02-09 01:37:24','1','xfghtu'),
	(3,'C Author 3','C Author 3','C3@example.com','http://example.com','An author bio with some text in it','','2006-02-16 22:58:02','1','xfghtu'),
	(4,'D Author 4','D Author 4','D4@example.com','','','','2006-02-15 23:00:00','1','xfghtu'),
	(5,'E Author 5','E Author 5','E5@example.com','www.example.com','','eauthor5','2006-02-16 23:00:00','1','xfghtu');

/*!40000 ALTER TABLE `fanfiction_authors` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_blocks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_blocks`;

CREATE TABLE `fanfiction_blocks` (
  `block_id` int(11) NOT NULL AUTO_INCREMENT,
  `block_name` varchar(30) NOT NULL DEFAULT '',
  `block_title` varchar(150) NOT NULL DEFAULT '',
  `block_file` varchar(200) NOT NULL DEFAULT '',
  `block_status` tinyint(1) NOT NULL DEFAULT '0',
  `block_variables` text NOT NULL,
  PRIMARY KEY (`block_id`),
  KEY `block_name` (`block_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_blocks` WRITE;
/*!40000 ALTER TABLE `fanfiction_blocks` DISABLE KEYS */;

INSERT INTO `fanfiction_blocks` (`block_id`, `block_name`, `block_title`, `block_file`, `block_status`, `block_variables`)
VALUES
	(1,'categories','Story Categories','categories/categories.php',1,'a:2:{s:7:\"columns\";s:1:\"0\";s:8:\"template\";s:38:\"{image} {link} [{count}] {description}\";}'),
	(3,'info','About Efiction Test','info/info.php',1,'a:1:{s:5:\"style\";s:1:\"1\";}'),
	(5,'menu','Main Menu','menu/menu.php',1,'a:1:{s:7:\"content\";a:14:{i:0;s:4:\"home\";i:1;s:6:\"recent\";i:2;s:6:\"titles\";i:3;s:8:\"catslink\";i:4;s:6:\"series\";i:5;s:7:\"authors\";i:6;s:10:\"challenges\";i:7;s:6:\"search\";i:8;s:4:\"tens\";i:9;s:4:\"help\";i:10;s:9:\"contactus\";i:11;s:5:\"login\";i:12;s:6:\"logout\";i:13;s:9:\"adminarea\";}}'),
	(9,'news','Latest News','news/news.php',1,'a:1:{s:3:\"num\";s:1:\"2\";}');

/*!40000 ALTER TABLE `fanfiction_blocks` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_categories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_categories`;

CREATE TABLE `fanfiction_categories` (
  `catid` int(11) NOT NULL AUTO_INCREMENT,
  `parentcatid` int(11) NOT NULL DEFAULT '-1',
  `category` varchar(60) NOT NULL DEFAULT '',
  `description` text NOT NULL,
  `image` varchar(100) NOT NULL DEFAULT '',
  `locked` char(1) NOT NULL DEFAULT '0',
  `leveldown` tinyint(4) NOT NULL DEFAULT '0',
  `displayorder` int(11) NOT NULL DEFAULT '0',
  `numitems` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`catid`),
  KEY `byparent` (`parentcatid`,`displayorder`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_categories` WRITE;
/*!40000 ALTER TABLE `fanfiction_categories` DISABLE KEYS */;

INSERT INTO `fanfiction_categories` (`catid`, `parentcatid`, `category`, `description`, `image`, `locked`, `leveldown`, `displayorder`, `numitems`)
VALUES
	(1,-1,'General','','categoryfp.gif','0',0,1,1310),
	(2,-1,'Slash Pairings','','categoryfp.gif','1',0,2,2332),
	(3,-1,'Het Pairings','','categoryfp.gif','1',0,3,229),
	(5,-1,'Threesomes, Moresomes','','categoryfp.gif','0',0,4,29),
	(6,2,'Bill/Bob','','category.gif','0',1,7,2227),
	(7,2,'Bill/Václav','','category.gif','0',1,8,6),
	(8,2,'Bill/Olu','','category.gif','0',1,9,1),
	(9,2,'Bill/Other Male','','category.gif','0',1,10,17),
	(10,2,'Bob/Václav','','category.gif','0',1,11,8),
	(11,2,'Bob/Olu','','category.gif','0',1,12,11),
	(12,2,'Bob/Other Male','','category.gif','0',1,14,42),
	(13,2,'Olu/Václav','','category.gif','0',1,15,4),
	(14,2,'Olu/Other Male','','category.gif','0',1,16,1),
	(15,2,'Václav/Other Male','','category.gif','0',1,17,1),
	(16,2,'Fatima/Aisha','','category.gif','0',1,18,56),
	(17,2,'Fatima/Samia','','category.gif','0',1,19,3),
	(18,2,'Fatima/Other Female','','category.gif','0',1,20,4),
	(19,2,'Aisha/Other Female','','category.gif','0',1,21,0),
	(20,2,'Samia/Other Female','','category.gif','0',1,22,0),
	(21,2,'Other Slash Pairing','','category.gif','0',1,23,0),
	(22,2,'Multiple Slash Pairings','','category.gif','0',1,24,0),
	(23,3,'Bill/Fatima','','category.gif','0',1,2,53),
	(24,3,'Bill/Sara','','category.gif','0',1,3,14),
	(25,3,'Bill/Aisha','','category.gif','0',1,4,2),
	(26,3,'Bill/Other Female','','category.gif','0',1,5,14),
	(27,3,'Bob/Don','','category.gif','0',1,6,60),
	(28,3,'Bob/Fatima','','category.gif','0',1,7,30),
	(29,3,'Bob/Aisha','','category.gif','0',1,9,20),
	(30,3,'Bob/Other Female','','category.gif','0',1,10,12),
	(31,3,'Václav/Fatima','','category.gif','0',1,11,18),
	(32,3,'Václav/Aisha','','category.gif','0',1,12,2),
	(33,3,'Václav/Isabelle','','category.gif','0',1,13,1),
	(34,3,'Václav/Other Female','','category.gif','0',1,14,1),
	(35,3,'Olu/Fatima','','category.gif','0',1,15,1),
	(36,3,'Olu/Samia','','category.gif','0',1,16,0),
	(37,3,'Bob/Samia','','category.gif','0',1,8,22),
	(38,3,'Olu/Other Female','','category.gif','0',1,17,0),
	(39,3,'Fatima/Peter','','category.gif','0',1,18,8),
	(40,3,'Fatima/Other Male','','category.gif','0',1,19,10),
	(43,2,'Bob/Vincent','','category.gif','0',1,13,23),
	(44,3,'John Billson/Jane Billson','','category.gif','0',1,20,4),
	(45,3,'Don/Other Male','','category.gif','0',1,21,1),
	(47,3,'Vincent Corentin/Aisha Johnson','','category.gif','0',1,22,2),
	(49,3,'Other Male/Other Female','','category.gif','0',1,1,2),
	(50,2,'Other Male/Other Male','','category.gif','0',1,6,7),
	(52,2,'Clone Bill/Clone Bob','','category.gif','0',1,5,8),
	(53,2,'AU Bill/AU Bob','','category.gif','0',1,4,7),
	(54,2,'Liam/Vincent Corentin','','category.gif','0',1,3,1),
	(55,2,'Ben/Brad - Other Fandom','','category.gif','0',1,2,7),
	(56,2,'Lisa White/Tania','','category.gif','0',1,1,1),
	(57,5,'Bill/Bob/Olu','','category.gif','0',1,12,1),
	(58,5,'Bill/Bob/Fatima','','category.gif','0',1,4,7),
	(59,5,'Bill/Bob/Other Male','','category.gif','0',1,11,4),
	(60,5,'Bill/Fatima/Aisha','','category.gif','0',1,7,1),
	(61,5,'Bill/Bob/Václav','','category.gif','0',1,10,6),
	(62,5,'Bob/Fatima/Aisha','','category.gif','0',1,6,1),
	(63,5,'Bill/Bob/Vincent Corentin','','category.gif','0',1,9,3),
	(64,5,'Bill/Bob/Mikhael','','category.gif','0',1,8,1),
	(66,5,'Bill/Fatima/Václav','','category.gif','0',1,5,1),
	(68,5,'Bill/Bob/Don','','category.gif','0',1,2,1),
	(69,5,'Bill/Bob/Fatima/Aisha','','category.gif','0',1,3,1),
	(70,5,'Bill/Bob/Samia','','','0',1,1,2);

/*!40000 ALTER TABLE `fanfiction_categories` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_challenges
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_challenges`;

CREATE TABLE `fanfiction_challenges` (
  `chalid` int(11) NOT NULL AUTO_INCREMENT,
  `challenger` varchar(200) NOT NULL DEFAULT '',
  `uid` int(11) NOT NULL DEFAULT '0',
  `title` varchar(250) NOT NULL DEFAULT '',
  `catid` varchar(200) NOT NULL DEFAULT '',
  `characters` varchar(200) NOT NULL DEFAULT '',
  `summary` text NOT NULL,
  PRIMARY KEY (`chalid`),
  KEY `title` (`catid`),
  KEY `uid` (`uid`),
  KEY `title_2` (`title`),
  KEY `characters` (`characters`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



# Dump of table fanfiction_chapters
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_chapters`;

CREATE TABLE `fanfiction_chapters` (
  `chapid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL DEFAULT '',
  `inorder` int(11) NOT NULL DEFAULT '0',
  `notes` text NOT NULL,
  `storytext` text,
  `endnotes` text,
  `validated` char(1) NOT NULL DEFAULT '0',
  `wordcount` int(11) NOT NULL DEFAULT '0',
  `rating` tinyint(4) NOT NULL DEFAULT '0',
  `reviews` smallint(6) NOT NULL DEFAULT '0',
  `sid` int(11) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL DEFAULT '0',
  `count` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`chapid`),
  KEY `sid` (`sid`),
  KEY `uid` (`uid`),
  KEY `inorder` (`inorder`),
  KEY `title` (`title`),
  KEY `validated` (`validated`),
  KEY `forstoryblock` (`sid`,`validated`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_chapters` WRITE;
/*!40000 ALTER TABLE `fanfiction_chapters` DISABLE KEYS */;

INSERT INTO `fanfiction_chapters` (`chapid`, `title`, `inorder`, `notes`, `storytext`, `endnotes`, `validated`, `wordcount`, `rating`, `reviews`, `sid`, `uid`, `count`)
VALUES
	(1,'Chapter 1',1,'Bacon-related notes.','',NULL,'1',3992,0,2,1,2,2872),
	(3,'Chapter One',1,'','',NULL,'1',8482,0,7,3,4,4615),
	(4,'Chapter Two',2,'','',NULL,'1',1625,0,1,3,4,2390),
	(50,'Cat Lorem Ipsum 1',1,'','',NULL,'1',2135,0,1,50,2,5340),
	(51,'Chapter 1',1,'','',NULL,'1',4809,0,1,51,2,4474),
	(52,'Chapter 2',2,'','',NULL,'1',2254,0,0,51,2,1567),
	(53,'Chapter 3',1,'','',NULL,'1',5169,0,0,51,2,2238),
	(54,'Chapter 1',1,'','',NULL,'1',2426,0,0,54,2,2018),
	(109,'Cakes',1,'','',NULL,'1',13,0,0,108,3,2020),
	(748,'Bookmark',1,'','',NULL,'1',12,0,0,741,5,2080),
	(842,'Windows 1252',1,'Eôs in ipsum ocûrrëret. Also first in series.','',NULL,'1',12,0,0,835,5,2066),
	(845,'Part 2',1,'Second story in the series.','',NULL,'1',11,0,0,838,5,1310),
	(3906,'A chapter',1,'',NULL,'','1',12,0,1,3519,3,3408),
	(4265,'Japanese text',1,'',NULL,'Note about the story from the author.','1',9,0,2,3721,5,3273),
	(4290,'Chapter 1',1,'Accented lorem ipsum.',NULL,'','1',33225,0,7,3745,2,2303),
	(4340,'Zombies!',1,'',NULL,'','1',2828,0,1,3785,2,3225),
	(4687,'Chapter 1',1,'Slightly longer text.',NULL,'','1',4849,0,2,4035,2,2767);

/*!40000 ALTER TABLE `fanfiction_chapters` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_characters
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_characters`;

CREATE TABLE `fanfiction_characters` (
  `charid` int(11) NOT NULL AUTO_INCREMENT,
  `catid` int(11) NOT NULL DEFAULT '0',
  `charname` varchar(60) NOT NULL DEFAULT '',
  `bio` text NOT NULL,
  `image` varchar(200) NOT NULL DEFAULT '',
  PRIMARY KEY (`charid`),
  KEY `catid` (`catid`),
  KEY `charname` (`charname`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_characters` WRITE;
/*!40000 ALTER TABLE `fanfiction_characters` DISABLE KEYS */;

INSERT INTO `fanfiction_characters` (`charid`, `catid`, `charname`, `bio`, `image`)
VALUES
	(1,-1,'Bill O\'Connell','',''),
	(2,-1,'Bob Billson','',''),
	(3,-1,'Fatima Habibi','',''),
	(4,-1,'Václav','',''),
	(5,-1,'Spyros Papadopoulos','',''),
	(6,-1,'Olu Adebayo','',''),
	(7,-1,'Samia Ben Abdel','',''),
	(8,-1,'Einar Rønquist','',''),
	(9,-1,'Aisha Johnson','',''),
	(10,-1,'Mikhael Antonov','',''),
	(11,-1,'Liam Habibi','',''),
	(12,-1,'Bernard','',''),
	(13,-1,'Vincent Corentin','',''),
	(14,-1,'Other','','');

/*!40000 ALTER TABLE `fanfiction_characters` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_classes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_classes`;

CREATE TABLE `fanfiction_classes` (
  `class_id` int(11) NOT NULL AUTO_INCREMENT,
  `class_type` int(11) NOT NULL DEFAULT '0',
  `class_name` varchar(100) NOT NULL DEFAULT '',
  PRIMARY KEY (`class_id`),
  KEY `byname` (`class_type`,`class_name`,`class_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_classes` WRITE;
/*!40000 ALTER TABLE `fanfiction_classes` DISABLE KEYS */;

INSERT INTO `fanfiction_classes` (`class_id`, `class_type`, `class_name`)
VALUES
	(1,1,'Action/Adventure'),
	(2,1,'Alternate Universe'),
	(3,1,'Angst'),
	(4,1,'Badfic'),
	(6,1,'Challenge'),
	(7,1,'Character Study'),
	(8,1,'Crossover'),
	(5,1,'Dark'),
	(9,1,'Drabble'),
	(10,1,'Drama'),
	(11,1,'Established Relationship'),
	(12,1,'First Time'),
	(13,1,'Friendship'),
	(14,1,'Holiday'),
	(15,1,'Humor'),
	(16,1,'Hurt/Comfort'),
	(17,1,'Jammies'),
	(42,1,'Kidfic'),
	(18,1,'Meridian Fix'),
	(19,1,'Missing Scene/Episode-Related'),
	(20,1,'Parody'),
	(21,1,'Poem/Limerick/Filk'),
	(22,1,'Pre-Relationship (het)'),
	(23,1,'Pre-Slash'),
	(24,1,'PWP - Plot, What Plot?'),
	(25,1,'Romance'),
	(26,1,'Smarm'),
	(29,1,'Songfic'),
	(27,1,'Team'),
	(28,1,'Vignette'),
	(30,2,'Adult Themes'),
	(31,2,'BDSM -- Bondage, Kink, etc.'),
	(32,2,'Character Death'),
	(35,2,'Language'),
	(33,2,'Non-Consensual Sex Acts'),
	(34,2,'Partner Betrayal'),
	(36,2,'Sexual Situations'),
	(37,2,'Violence');

/*!40000 ALTER TABLE `fanfiction_classes` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_classtypes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_classtypes`;

CREATE TABLE `fanfiction_classtypes` (
  `classtype_id` int(11) NOT NULL AUTO_INCREMENT,
  `classtype_name` varchar(50) NOT NULL DEFAULT '',
  `classtype_title` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`classtype_id`),
  UNIQUE KEY `classtype_name` (`classtype_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_classtypes` WRITE;
/*!40000 ALTER TABLE `fanfiction_classtypes` DISABLE KEYS */;

INSERT INTO `fanfiction_classtypes` (`classtype_id`, `classtype_name`, `classtype_title`)
VALUES
	(1,'genres','Genres'),
	(2,'warnings','Warnings');

/*!40000 ALTER TABLE `fanfiction_classtypes` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_coauthors
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_coauthors`;

CREATE TABLE `fanfiction_coauthors` (
  `sid` int(11) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`sid`,`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_coauthors` WRITE;
/*!40000 ALTER TABLE `fanfiction_coauthors` DISABLE KEYS */;

INSERT INTO `fanfiction_coauthors` (`sid`, `uid`)
VALUES
	(1,5),
	(108,5);

/*!40000 ALTER TABLE `fanfiction_coauthors` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_codeblocks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_codeblocks`;

CREATE TABLE `fanfiction_codeblocks` (
  `code_id` int(11) NOT NULL AUTO_INCREMENT,
  `code_text` text NOT NULL,
  `code_type` varchar(20) DEFAULT NULL,
  `code_module` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`code_id`),
  KEY `code_type` (`code_type`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



# Dump of table fanfiction_comments
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_comments`;

CREATE TABLE `fanfiction_comments` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `nid` int(11) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL DEFAULT '0',
  `comment` text NOT NULL,
  `time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`cid`),
  KEY `commentlist` (`nid`,`time`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_comments` WRITE;
/*!40000 ALTER TABLE `fanfiction_comments` DISABLE KEYS */;

INSERT INTO `fanfiction_comments` (`cid`, `nid`, `uid`, `comment`, `time`)
VALUES
	(1,1,3,'The new archive is amazing :)','2006-04-03 18:12:00'),
	(2,1,305,'The site looks *stupendous*!','2006-04-05 18:37:36'),
	(3,1,360,'Looks great!  ','2006-08-01 23:42:32');

/*!40000 ALTER TABLE `fanfiction_comments` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_favorites
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_favorites`;

CREATE TABLE `fanfiction_favorites` (
  `uid` int(11) NOT NULL DEFAULT '0',
  `item` int(11) NOT NULL DEFAULT '0',
  `type` char(2) NOT NULL DEFAULT '',
  `comments` text NOT NULL,
  UNIQUE KEY `byitem` (`item`,`type`,`uid`),
  UNIQUE KEY `byuid` (`uid`,`type`,`item`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_favorites` WRITE;
/*!40000 ALTER TABLE `fanfiction_favorites` DISABLE KEYS */;

INSERT INTO `fanfiction_favorites` (`uid`, `item`, `type`, `comments`)
VALUES
	(1,1,'ST',''),
	(0,2559,'ST',''),
	(0,2277,'ST',''),
	(0,1386,'ST',''),
	(0,2331,'ST',''),
	(0,2540,'ST',''),
	(0,71,'ST',''),
	(0,72,'ST',''),
	(0,73,'ST',''),
	(0,2084,'ST',''),
	(0,2,'AU',''),
	(0,24,'AU',''),
	(2,2694,'ST',''),
	(2,1961,'ST',''),
	(2,3176,'ST',''),
	(2,1881,'ST',''),
	(2,248,'ST',''),
	(2,342,'ST',''),
	(2,2934,'ST',''),
	(2,322,'ST',''),
	(2,375,'ST',''),
	(2,3525,'ST',''),
	(2,2411,'ST',''),
	(2,2414,'ST',''),
	(2,2645,'ST',''),
	(2,308,'ST',''),
	(2,3540,'ST',''),
	(2,1090,'ST',''),
	(2,2442,'ST',''),
	(2,2034,'ST',''),
	(2,2697,'ST',''),
	(2,3472,'ST',''),
	(2,2868,'ST',''),
	(2,3161,'ST',''),
	(2,2795,'ST',''),
	(2,2126,'ST',''),
	(2,3308,'ST',''),
	(2,236,'ST',''),
	(2,2679,'ST',''),
	(2,2791,'ST',''),
	(2,746,'ST',''),
	(2,2327,'ST',''),
	(2,800,'ST',''),
	(2,3491,'ST',''),
	(2,2984,'ST',''),
	(2,2285,'ST',''),
	(2,588,'ST',''),
	(2,3209,'ST',''),
	(2,3467,'ST',''),
	(2,1926,'ST','');

/*!40000 ALTER TABLE `fanfiction_favorites` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_inseries
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_inseries`;

CREATE TABLE `fanfiction_inseries` (
  `seriesid` int(11) NOT NULL DEFAULT '0',
  `sid` int(11) NOT NULL DEFAULT '0',
  `subseriesid` int(11) NOT NULL DEFAULT '0',
  `confirmed` int(11) NOT NULL DEFAULT '0',
  `inorder` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`sid`,`seriesid`,`subseriesid`),
  KEY `seriesid` (`seriesid`,`inorder`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_inseries` WRITE;
/*!40000 ALTER TABLE `fanfiction_inseries` DISABLE KEYS */;

INSERT INTO `fanfiction_inseries` (`seriesid`, `sid`, `subseriesid`, `confirmed`, `inorder`)
VALUES
	(169,108,0,1,19),
	(118,838,0,1,2),
	(118,835,0,1,1),
	(224,3721,0,1,5);

/*!40000 ALTER TABLE `fanfiction_inseries` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_log`;

CREATE TABLE `fanfiction_log` (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `log_action` varchar(255) DEFAULT NULL,
  `log_uid` int(11) NOT NULL,
  `log_ip` int(11) unsigned DEFAULT NULL,
  `log_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `log_type` varchar(2) NOT NULL,
  PRIMARY KEY (`log_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



# Dump of table fanfiction_messages
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_messages`;

CREATE TABLE `fanfiction_messages` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `message_name` varchar(50) NOT NULL DEFAULT '',
  `message_title` varchar(200) NOT NULL DEFAULT '',
  `message_text` text NOT NULL,
  PRIMARY KEY (`message_id`),
  KEY `message_name` (`message_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_messages` WRITE;
/*!40000 ALTER TABLE `fanfiction_messages` DISABLE KEYS */;

INSERT INTO `fanfiction_messages` (`message_id`, `message_name`, `message_title`, `message_text`)
VALUES
	(1,'copyright','Copyright Footer','<div align=\"center\" style= \"font-size: .8em\">\r\nThis site is powered by <a href=\"http://efiction.org/index.php\">eFiction 3.5.3</a>. Skin design by Moderator.'),
	(9,'welcome','Welcome','Welcome to Efiction Test!'),
	(13,'rules','EFiction Submission Rules',''),
	(14,'tos','Terms of Service','');

/*!40000 ALTER TABLE `fanfiction_messages` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_modules
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_modules`;

CREATE TABLE `fanfiction_modules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL DEFAULT 'Test Module',
  `version` varchar(10) CHARACTER SET latin1 COLLATE latin1_general_ci NOT NULL DEFAULT '1.0',
  PRIMARY KEY (`id`),
  KEY `name_version` (`name`,`version`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



# Dump of table fanfiction_news
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_news`;

CREATE TABLE `fanfiction_news` (
  `nid` int(11) NOT NULL AUTO_INCREMENT,
  `author` varchar(60) NOT NULL DEFAULT '',
  `title` varchar(255) NOT NULL DEFAULT '',
  `story` text NOT NULL,
  `time` datetime DEFAULT NULL,
  `comments` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`nid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_news` WRITE;
/*!40000 ALTER TABLE `fanfiction_news` DISABLE KEYS */;

INSERT INTO `fanfiction_news` (`nid`, `author`, `title`, `story`, `time`, `comments`)
VALUES
	(1,'Moderator','New Archive Open for Business!','Welcome to the new Efiction Test archive!','2006-04-03 13:21:07',3);

/*!40000 ALTER TABLE `fanfiction_news` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_pagelinks
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_pagelinks`;

CREATE TABLE `fanfiction_pagelinks` (
  `link_id` int(11) NOT NULL AUTO_INCREMENT,
  `link_name` varchar(50) NOT NULL DEFAULT '',
  `link_text` varchar(100) NOT NULL DEFAULT '',
  `link_key` char(1) DEFAULT NULL,
  `link_url` varchar(250) NOT NULL DEFAULT '',
  `link_target` char(1) NOT NULL DEFAULT '0',
  `link_access` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`link_id`),
  KEY `link_name` (`link_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_pagelinks` WRITE;
/*!40000 ALTER TABLE `fanfiction_pagelinks` DISABLE KEYS */;

INSERT INTO `fanfiction_pagelinks` (`link_id`, `link_name`, `link_text`, `link_key`, `link_url`, `link_target`, `link_access`)
VALUES
	(1,'home','Home',NULL,'index.php','0',0),
	(9,'authors','Authors',NULL,'authors.php?list=authors','0',0),
	(12,'series','Series',NULL,'browse.php?type=series','0',0),
	(15,'contactus','Contact Us',NULL,'contact.php','0',0);

/*!40000 ALTER TABLE `fanfiction_pagelinks` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_panels
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_panels`;

CREATE TABLE `fanfiction_panels` (
  `panel_id` int(11) NOT NULL AUTO_INCREMENT,
  `panel_name` varchar(50) NOT NULL DEFAULT 'unknown',
  `panel_title` varchar(100) NOT NULL DEFAULT 'Unnamed Panel',
  `panel_url` varchar(100) DEFAULT NULL,
  `panel_level` tinyint(4) NOT NULL DEFAULT '3',
  `panel_order` tinyint(4) NOT NULL DEFAULT '0',
  `panel_hidden` tinyint(1) NOT NULL DEFAULT '0',
  `panel_type` varchar(20) NOT NULL DEFAULT 'A',
  PRIMARY KEY (`panel_id`),
  KEY `panel_type` (`panel_type`,`panel_name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_panels` WRITE;
/*!40000 ALTER TABLE `fanfiction_panels` DISABLE KEYS */;

INSERT INTO `fanfiction_panels` (`panel_id`, `panel_name`, `panel_title`, `panel_url`, `panel_level`, `panel_order`, `panel_hidden`, `panel_type`)
VALUES
	(1,'submitted','Submissions','',3,5,0,'A'),
	(2,'versioncheck','Version Check','',3,8,0,'A'),
	(3,'newstory','Add New Story','stories.php?action=newstory&admin=1',3,2,0,'A'),
	(4,'addseries','Add New Series','series.php?action=add',3,1,0,'A'),
	(5,'news','News','',3,4,0,'A'),
	(6,'featured','Featured Stories','',3,3,0,'A'),
	(7,'characters','Characters','',2,2,0,'A'),
	(8,'ratings','Ratings','',2,3,0,'A'),
	(9,'members','Members','',2,5,0,'A'),
	(10,'mailusers','Mail Users','',2,6,0,'A'),
	(11,'settings','Settings','',1,2,0,'A'),
	(12,'blocks','Blocks','',1,3,0,'A'),
	(13,'censor','Censor','',1,0,1,'A'),
	(14,'admins','Admins','',1,6,0,'A'),
	(15,'classifications','Classifications','',2,4,0,'A'),
	(16,'categories','Categories','',2,1,0,'A');

/*!40000 ALTER TABLE `fanfiction_panels` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_ratings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_ratings`;

CREATE TABLE `fanfiction_ratings` (
  `rid` int(11) NOT NULL AUTO_INCREMENT,
  `rating` varchar(60) NOT NULL DEFAULT '',
  `ratingwarning` char(1) NOT NULL DEFAULT '0',
  `warningtext` text NOT NULL,
  PRIMARY KEY (`rid`),
  KEY `rating` (`rating`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_ratings` WRITE;
/*!40000 ALTER TABLE `fanfiction_ratings` DISABLE KEYS */;

INSERT INTO `fanfiction_ratings` (`rid`, `rating`, `ratingwarning`, `warningtext`)
VALUES
	(1,'All Ages','',''),
	(2,'Pre-Teen','',''),
	(3,'Teen','',''),
	(4,'Mature','',''),
	(5,'Adult','','');

/*!40000 ALTER TABLE `fanfiction_ratings` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_reviews
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_reviews`;

CREATE TABLE `fanfiction_reviews` (
  `reviewid` int(11) NOT NULL AUTO_INCREMENT,
  `item` int(11) NOT NULL DEFAULT '0',
  `chapid` int(11) NOT NULL DEFAULT '0',
  `reviewer` varchar(60) NOT NULL DEFAULT '0',
  `uid` int(11) NOT NULL DEFAULT '0',
  `review` text NOT NULL,
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `rating` int(11) NOT NULL DEFAULT '0',
  `respond` char(1) NOT NULL DEFAULT '0',
  `type` varchar(2) NOT NULL DEFAULT 'ST',
  PRIMARY KEY (`reviewid`),
  KEY `psid` (`chapid`),
  KEY `rating` (`rating`),
  KEY `respond` (`respond`),
  KEY `avgrating` (`type`,`item`,`rating`),
  KEY `bychapter` (`chapid`,`rating`),
  KEY `byuid` (`uid`,`item`,`type`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_reviews` WRITE;
/*!40000 ALTER TABLE `fanfiction_reviews` DISABLE KEYS */;

INSERT INTO `fanfiction_reviews` (`reviewid`, `item`, `chapid`, `reviewer`, `uid`, `review`, `date`, `rating`, `respond`, `type`)
VALUES
	(1,54,117,'Reviewer 3',3,'Magical :)','2006-03-12 16:43:50',0,'1','ST'),
	(8,3,2120,'Reviewer 1',7,'Absolutely beautiful! ','2006-03-28 17:36:50',0,'0','ST'),
	(10,4,932,'Reviewer 2',0,'Awesome!!!  This was so much fun to read :)<br><br><i>Author\'s Response: Glad you liked it!</i>','2006-04-03 19:34:02',0,'1','ST'),
	(13,54,650,'Reviewer 4',0,'MUUUUUCH better than the actual episode. :-) Thanks!','2006-04-04 01:19:24',0,'0','ST'),
	(14,741,2087,'Reviewer 1',316,'More ! More!  ^___^','2006-04-04 03:09:28',0,'0','ST'),
	(15,741,2623,'Reviewer 2',0,'Oh. Ow. Wow! <br />','2006-04-04 05:55:36',0,'1','ST');

/*!40000 ALTER TABLE `fanfiction_reviews` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_series
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_series`;

CREATE TABLE `fanfiction_series` (
  `seriesid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL DEFAULT '',
  `summary` text,
  `uid` int(11) NOT NULL DEFAULT '0',
  `isopen` tinyint(4) NOT NULL DEFAULT '0',
  `catid` varchar(200) NOT NULL DEFAULT '0',
  `classes` varchar(200) DEFAULT NULL,
  `rating` tinyint(4) NOT NULL DEFAULT '0',
  `warnings` varchar(250) NOT NULL DEFAULT '',
  `genres` varchar(250) NOT NULL DEFAULT '',
  `characters` varchar(250) NOT NULL DEFAULT '',
  `reviews` smallint(6) NOT NULL DEFAULT '0',
  `challenges` varchar(200) NOT NULL DEFAULT '',
  `numstories` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`seriesid`),
  KEY `catid` (`catid`),
  KEY `challenges` (`challenges`),
  KEY `warnings` (`warnings`),
  KEY `characters` (`characters`),
  KEY `genres` (`genres`),
  KEY `owner` (`uid`,`title`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_series` WRITE;
/*!40000 ALTER TABLE `fanfiction_series` DISABLE KEYS */;

INSERT INTO `fanfiction_series` (`seriesid`, `title`, `summary`, `uid`, `isopen`, `catid`, `classes`, `rating`, `warnings`, `genres`, `characters`, `reviews`, `challenges`, `numstories`)
VALUES
	(118,'Windows 1252','This series takes place several months after the episode Need and deals with the aftermath of certain events - how they have affected Bob and what happens to the friendship between Bill and Bob as a result of Bill discovering his \'secret\'.',5,0,'1','3,7,10,13,26,30',0,'Adult Themes','Angst,Character Study,Drama,Friendship,Smarm','2,1',1,'',5),
	(169,'Cakes','A challenge about cakes.',3,0,'6','1,3,7,10,12,13,14,15,16,17,19,25',0,'','Action/Adventure,Angst,Character Study,Drama,First Time,Friendship,Holiday,Humor,Hurt/Comfort,Jammies,Missing Scene/Episode-Related,Romance','2,5,1,11,9,13,3,4',7,'',24),
	(224,'Japanese series','Chapter is in Japanese anyway.',5,0,'6','3,11,14,15,25',0,'','Angst,Established Relationship,Holiday,Humor,Romance','2,1,3',4,'',5);

/*!40000 ALTER TABLE `fanfiction_series` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_settings
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_settings`;

CREATE TABLE `fanfiction_settings` (
  `sitekey` varchar(50) NOT NULL DEFAULT '1',
  `sitename` varchar(200) NOT NULL DEFAULT 'Your Site',
  `slogan` varchar(200) NOT NULL DEFAULT 'It''s a cool site!',
  `url` varchar(200) NOT NULL DEFAULT 'http://www.yoursite.com',
  `siteemail` varchar(200) NOT NULL DEFAULT 'you@yoursite.com',
  `tableprefix` varchar(50) NOT NULL DEFAULT '',
  `skin` varchar(50) NOT NULL DEFAULT 'default',
  `hiddenskins` varchar(255) DEFAULT '',
  `language` varchar(10) NOT NULL DEFAULT 'en',
  `submissionsoff` tinyint(1) NOT NULL DEFAULT '0',
  `storiespath` varchar(20) NOT NULL DEFAULT 'stories',
  `store` varchar(5) NOT NULL DEFAULT 'files',
  `autovalidate` tinyint(1) NOT NULL DEFAULT '0',
  `coauthallowed` int(1) NOT NULL DEFAULT '0',
  `maxwords` int(11) NOT NULL DEFAULT '0',
  `minwords` int(11) NOT NULL DEFAULT '0',
  `imageupload` tinyint(1) NOT NULL DEFAULT '0',
  `imageheight` int(11) NOT NULL DEFAULT '200',
  `imagewidth` int(11) NOT NULL DEFAULT '200',
  `roundrobins` tinyint(1) NOT NULL DEFAULT '0',
  `allowseries` tinyint(4) NOT NULL DEFAULT '2',
  `tinyMCE` tinyint(1) NOT NULL DEFAULT '0',
  `allowed_tags` varchar(200) NOT NULL DEFAULT '<b><i><u><center><hr><p><br /><br><blockquote><ol><ul><li><img><strong><em>',
  `favorites` tinyint(1) NOT NULL DEFAULT '0',
  `multiplecats` tinyint(1) NOT NULL DEFAULT '0',
  `newscomments` tinyint(1) NOT NULL DEFAULT '0',
  `logging` tinyint(1) NOT NULL DEFAULT '0',
  `maintenance` tinyint(1) NOT NULL DEFAULT '0',
  `debug` tinyint(1) NOT NULL DEFAULT '0',
  `captcha` tinyint(1) NOT NULL DEFAULT '0',
  `dateformat` varchar(20) NOT NULL DEFAULT 'd/m/y',
  `timeformat` varchar(20) NOT NULL DEFAULT '- h:i a',
  `recentdays` tinyint(2) NOT NULL DEFAULT '7',
  `displaycolumns` tinyint(1) NOT NULL DEFAULT '1',
  `itemsperpage` tinyint(2) NOT NULL DEFAULT '25',
  `extendcats` tinyint(1) NOT NULL DEFAULT '0',
  `displayindex` tinyint(1) NOT NULL DEFAULT '0',
  `defaultsort` tinyint(1) NOT NULL DEFAULT '0',
  `displayprofile` tinyint(1) NOT NULL DEFAULT '0',
  `linkstyle` tinyint(1) NOT NULL DEFAULT '0',
  `linkrange` tinyint(2) NOT NULL DEFAULT '5',
  `reviewsallowed` tinyint(1) NOT NULL DEFAULT '0',
  `ratings` tinyint(1) NOT NULL DEFAULT '0',
  `anonreviews` tinyint(1) NOT NULL DEFAULT '0',
  `revdelete` tinyint(1) NOT NULL DEFAULT '0',
  `rateonly` tinyint(1) NOT NULL DEFAULT '0',
  `pwdsetting` tinyint(1) NOT NULL DEFAULT '0',
  `alertson` tinyint(1) NOT NULL DEFAULT '0',
  `disablepopups` tinyint(1) NOT NULL DEFAULT '0',
  `agestatement` tinyint(1) NOT NULL DEFAULT '0',
  `words` text,
  `version` varchar(10) NOT NULL DEFAULT '3.3',
  `smtp_host` varchar(200) DEFAULT NULL,
  `smtp_username` varchar(50) DEFAULT NULL,
  `smtp_password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`sitekey`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_settings` WRITE;
/*!40000 ALTER TABLE `fanfiction_settings` DISABLE KEYS */;

INSERT INTO `fanfiction_settings` (`sitekey`, `sitename`, `slogan`, `url`, `siteemail`, `tableprefix`, `skin`, `hiddenskins`, `language`, `submissionsoff`, `storiespath`, `store`, `autovalidate`, `coauthallowed`, `maxwords`, `minwords`, `imageupload`, `imageheight`, `imagewidth`, `roundrobins`, `allowseries`, `tinyMCE`, `allowed_tags`, `favorites`, `multiplecats`, `newscomments`, `logging`, `maintenance`, `debug`, `captcha`, `dateformat`, `timeformat`, `recentdays`, `displaycolumns`, `itemsperpage`, `extendcats`, `displayindex`, `defaultsort`, `displayprofile`, `linkstyle`, `linkrange`, `reviewsallowed`, `ratings`, `anonreviews`, `revdelete`, `rateonly`, `pwdsetting`, `alertson`, `disablepopups`, `agestatement`, `words`, `version`, `smtp_host`, `smtp_username`, `smtp_password`)
VALUES
	('VxDE9ij5nX','Efiction Test','A Testing Fan Fiction Archive','http://www.example.com','admin@example.com','','classicsg1','CSSZen','en',0,'storiesef','files',0,1,0,0,1,200,300,0,2,0,'<b><i><u><center><hr><p><br /><br><blockquote><ol><ul><li><img><strong><em><a>',1,1,0,1,0,0,1,'d M Y','h:i a',127,1,20,0,0,0,1,2,5,1,0,0,2,0,1,1,1,1,'','3.5.3','mail.test.com','agsender@example.com','!BillBob!');

/*!40000 ALTER TABLE `fanfiction_settings` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_stats
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_stats`;

CREATE TABLE `fanfiction_stats` (
  `sitekey` varchar(50) NOT NULL DEFAULT '0',
  `stories` int(11) NOT NULL DEFAULT '0',
  `chapters` int(11) NOT NULL DEFAULT '0',
  `series` int(11) NOT NULL DEFAULT '0',
  `reviews` int(11) NOT NULL DEFAULT '0',
  `wordcount` int(11) NOT NULL DEFAULT '0',
  `authors` int(11) NOT NULL DEFAULT '0',
  `members` int(11) NOT NULL DEFAULT '0',
  `reviewers` int(11) NOT NULL DEFAULT '0',
  `newestmember` int(11) NOT NULL DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_stats` WRITE;
/*!40000 ALTER TABLE `fanfiction_stats` DISABLE KEYS */;

INSERT INTO `fanfiction_stats` (`sitekey`, `stories`, `chapters`, `series`, `reviews`, `wordcount`, `authors`, `members`, `reviewers`, `newestmember`)
VALUES
	('VxDE9ij5nX',3835,4556,249,4505,23176094,378,1138,1684,1613);

/*!40000 ALTER TABLE `fanfiction_stats` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table fanfiction_stories
# ------------------------------------------------------------

DROP TABLE IF EXISTS `fanfiction_stories`;

CREATE TABLE `fanfiction_stories` (
  `sid` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(200) NOT NULL DEFAULT '',
  `summary` text,
  `storynotes` text,
  `catid` varchar(100) NOT NULL DEFAULT '0',
  `classes` varchar(200) DEFAULT NULL,
  `charid` varchar(250) NOT NULL DEFAULT '0',
  `rid` varchar(25) NOT NULL DEFAULT '0',
  `date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `uid` int(11) NOT NULL DEFAULT '0',
  `coauthors` varchar(200) DEFAULT NULL,
  `featured` char(1) NOT NULL DEFAULT '0',
  `validated` char(1) NOT NULL DEFAULT '0',
  `completed` char(1) NOT NULL DEFAULT '0',
  `rr` char(1) NOT NULL DEFAULT '0',
  `wordcount` int(11) NOT NULL DEFAULT '0',
  `rating` tinyint(4) NOT NULL DEFAULT '0',
  `reviews` smallint(6) NOT NULL DEFAULT '0',
  `count` int(11) NOT NULL DEFAULT '0',
  `challenges` varchar(200) NOT NULL DEFAULT '0',
  PRIMARY KEY (`sid`),
  KEY `title` (`title`),
  KEY `catid` (`catid`),
  KEY `charid` (`charid`),
  KEY `rid` (`rid`),
  KEY `uid` (`uid`),
  KEY `featured` (`featured`),
  KEY `completed` (`completed`),
  KEY `rr` (`rr`),
  KEY `challenges` (`challenges`),
  KEY `validateduid` (`validated`,`uid`),
  KEY `recent` (`updated`,`validated`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

LOCK TABLES `fanfiction_stories` WRITE;
/*!40000 ALTER TABLE `fanfiction_stories` DISABLE KEYS */;

INSERT INTO `fanfiction_stories` (`sid`, `title`, `summary`, `storynotes`, `catid`, `classes`, `charid`, `rid`, `date`, `updated`, `uid`, `coauthors`, `featured`, `validated`, `completed`, `rr`, `wordcount`, `rating`, `reviews`, `count`, `challenges`)
VALUES
	(1,'Bacon ipsum','Meat-related text.',NULL,'1','3,10,16,26','2,1','3','2006-02-09 22:21:35','2006-02-09 22:21:35',2,NULL,'','1','1','',3992,0,2,2872,'0'),
	(3,'Lorem ipsum','Short, and no tricky characters.',NULL,'6','3,10,12,15,25','2,1,3,4','5','2006-03-04 13:00:45','2006-03-04 13:00:45',4,NULL,'','1','1','',8482,0,7,4615,'0'),
	(4,'Email story','Email-related story.',NULL,'6','15','2,1','3','2006-03-04 13:16:12','2006-03-04 13:16:12',4,NULL,'','1','1','',1625,0,1,2390,'0'),
	(50,'Cat-related ipsum','Meow all night chew iPad power cord.',NULL,'6','3,10,11,14','2,1','2','2006-03-05 17:12:16','2006-03-05 17:12:16',2,NULL,'','1','1','0',2135,0,1,5340,'0'),
	(51,'Cupcake ipsum','Biscuit candy cake candy macaroon. Soufflé marzipan croissant gummi bears. Wafer lollipop tart topping. Bonbon danish dragée lemon drops lemon drops caramels jelly. Tootsie roll chocolate cookie cake. Topping cheesecake lollipop halvah jujubes brownie bear claw. ',NULL,'6','3,10,11,16','2,1','3','2006-03-05 17:20:38','2006-03-05 17:20:38',2,NULL,'','1','1','0',4809,0,1,4474,'0'),
	(54,'Carl Sagan ipsum','Only shorter.',NULL,'6','11,16','2,1','3','2006-03-05 17:27:05','2006-03-05 17:27:05',2,NULL,'','1','1','0',2426,0,0,2018,'0'),
	(108,'A lot of cakes','Lots and lots of cakes.',NULL,'6','7,12,25','2,1,4','5','2006-03-06 15:42:57','2006-03-06 15:42:57',3,NULL,'','1','1','',13,0,0,2020,'0'),
	(741,'Actually a bookmark','This is a story containing only a link to another location.',NULL,'1','3,7,13,19','2,1','1','2006-03-17 15:26:36','2006-03-17 15:26:36',5,NULL,'','1','1','',12,0,0,2080,'0'),
	(835,'Windows 1252 Story','Eôs in ipsum ocûrrëret.',NULL,'1','3,7,13,19,30','2,1','3','2006-03-18 12:56:43','2006-03-18 12:56:43',5,NULL,'','1','1','0',12,0,0,2066,'0'),
	(838,'Another story in series','Things happen.',NULL,'1','3,7,13,19','2,1,14','3','2006-03-18 13:42:27','2006-03-18 13:42:27',5,NULL,'','1','1','',11,0,0,1310,'0'),
	(3519,'Beans and other vegetables','More vegetables.','Written for someone\'s birthday as a small thank you for all their hard work and dedication here on Efiction Test archive and the Testing Solutions website.  Moderator, you\'re a star!','6','3,7,12,25','2,1','4','2008-02-11 13:32:43','2008-02-11 13:33:02',3,'1','0','1','1','0',12,0,1,3408,'0'),
	(3721,'Japanese','Database is Latin-1 and doesn\'t support Japanese text.','','6','37,1,2,3,7,10,11,14,15,16,25','2,5,1,9,14,3,4','4','2008-10-08 20:58:26','2008-10-08 20:58:29',5,'1','1','1','1','0',9,0,2,3273,'0'),
	(3745,'Accented lorem ipsum','A nice little summary.','','27','2,3,13,16','2,1,3,4','3','2008-11-28 14:10:56','2008-11-28 14:10:59',2,'1','0','1','1','0',33225,0,7,2303,'0'),
	(3785,'Zombies','Zombie-related lorem ipsum.','Some story notes about Zombies.','1','13,14,27','2,1,3,4','1','2008-12-27 07:18:06','2008-12-27 07:18:09',2,'1','0','1','1','0',2828,0,1,3225,'0'),
	(4035,'Hipster ipsum','Bushwick man braid vaporware hot chicken yuccie snackwave cold-pressed +1 3 wolf moon.','Thanks to betas.','6','16','2,1,11,9,3,4','3','2010-01-03 10:04:12','2010-01-03 10:04:16',2,'0','0','1','1','0',4849,0,2,2767,'0');

/*!40000 ALTER TABLE `fanfiction_stories` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
