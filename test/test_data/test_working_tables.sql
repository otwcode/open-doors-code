DROP DATABASE IF EXISTS $DATABASE$;
CREATE DATABASE $DATABASE$;
USE $DATABASE$;

CREATE TABLE IF NOT EXISTS `authors` (
    `id`            int(11)      NOT NULL AUTO_INCREMENT,
    `name`          varchar(255) NOT NULL DEFAULT '',
    `email`         varchar(255) NOT NULL DEFAULT '',
    `imported`      tinyint(1)   NOT NULL DEFAULT '0',
    `do_not_import` tinyint(1)   NOT NULL DEFAULT '0',
    `to_delete`     tinyint(1)            DEFAULT '0',
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;
  
INSERT INTO `authors` (`id`, `name`, `email`, `imported`, `do_not_import`, `to_delete`) VALUES 
(1,'Author 1','test1@opendoors.org',0,0,0),
(2,'Author 2','test2@opendoors.org',0,0,0),
(3,'Author 3','test3@opendoors.org',0,0,0),
(4,'Author 4','test4@opendoors.org',0,0,0),
(5,'Author 5','test5@opendoors.org',0,0,0);

CREATE TABLE IF NOT EXISTS `chapters` (
    `id`       int(11)      NOT NULL AUTO_INCREMENT,
    `position` bigint(22)            DEFAULT NULL,
    `title`    varchar(255) NOT NULL DEFAULT '',
    `text`     mediumtext,
    `date`     datetime              DEFAULT NULL,
    `story_id` int(11)               DEFAULT '0',
    `notes`    text,
    `url`      varchar(1024)         DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`),
    KEY `storyid` (`story_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

INSERT INTO `chapters` (`id`, `position`, `title`, `text`, `date`, `story_id`, `notes`, `url`) VALUES 
(1,1,'Chapter 1','',NULL,1,'',NULL),
(2,1,'Chapter 1','',NULL,2,'',NULL),
(3,1,'Chapter 1','',NULL,3,'',NULL),
(4,1,'Chapter 1','',NULL,4,'',NULL),
(5,1,'Chapter 1','',NULL,5,'',NULL);

CREATE TABLE IF NOT EXISTS `item_authors` (
    `id`        int(11) NOT NULL AUTO_INCREMENT,
    `author_id` int(11) NOT NULL,
    `item_id`   int(11) NOT NULL,
    `item_type` ENUM ('story', 'story_link', 'chapter'),
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`),
    KEY `item_id` (`item_id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

INSERT INTO `item_authors` (`id`, `author_id`, `item_id`, `item_type`) VALUES 
(1,1,1,'story'),
(2,2,2,'story'),
(3,3,3,'story'),
(4,4,4,'story'),
(5,5,5,'story');

CREATE TABLE IF NOT EXISTS `item_tags` (
    `id`        int(11) NOT NULL AUTO_INCREMENT,
    `item_id`   int(11),
    `item_type` ENUM ('story', 'story_link', 'chapter'),
    `tag_id`    int(11),
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

INSERT INTO `item_tags` (`id`, `item_id`, `item_type`, `tag_id`) VALUES 
(1,1,'story',1),
(2,2,'story',2),
(3,3,'story',3),
(4,4,'story',4),
(5,5,'story',5);

CREATE TABLE IF NOT EXISTS `stories` (
    `id`            int(11)      NOT NULL AUTO_INCREMENT,
    `title`         varchar(255) NOT NULL DEFAULT '',
    `summary`       text,
    `notes`         text,
    `date`          datetime              DEFAULT NULL,
    `updated`       datetime              DEFAULT NULL,
    `categories`    varchar(45)           DEFAULT NULL,
    `tags`          varchar(255) NOT NULL DEFAULT '',
    `warnings`      varchar(255)          DEFAULT '',
    `fandoms`       varchar(255)          DEFAULT '',
    `characters`    varchar(1024)         DEFAULT '',
    `relationships` varchar(1024)         DEFAULT '',
    `language_code` varchar(5)            DEFAULT 'en',
    `url`           varchar(255)          DEFAULT NULL,
    `imported`      tinyint(1)   NOT NULL DEFAULT '0',
    `do_not_import` tinyint(1)   NOT NULL DEFAULT '0',
    `ao3_url`       varchar(255)          DEFAULT NULL,
    `import_notes`  varchar(1024)         DEFAULT '',
    `rating`        varchar(21)           DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

INSERT INTO `stories` (`id`, `title`, `summary`, `notes`, `date`, `updated`, `categories`, `tags`, `warnings`, `fandoms`, `characters`, `relationships`, `language_code`, `url`, `imported`, `do_not_import`, `ao3_url`, `import_notes`, `rating`) VALUES 
(1,'Story 1','Summary 1','','2004-07-01 18:10:04','2004-07-01 18:59:02',NULL,'','','','','','',NULL,0,0,NULL,'',NULL),
(2,'Story 2','Summary 2','','2004-07-01 19:33:10','2004-07-01 21:43:45',NULL,'','','','','','',NULL,0,0,NULL,'',NULL),
(3,'Story 3','Summary 3','','2004-07-01 21:54:47','2004-07-24 20:24:38',NULL,'','','','','','',NULL,0,0,NULL,'',NULL),
(4,'Story 4','Summary 4','','2004-07-01 22:04:33','2004-07-24 22:05:42',NULL,'','','','','','',NULL,0,0,NULL,'',NULL),
(5,'Story 5','Summary 5','','2004-07-04 14:32:24','2004-07-04 14:32:24',NULL,'','','','','','',NULL,0,0,NULL,'',NULL);

CREATE TABLE IF NOT EXISTS `story_links` (
    `id`            int(11)      NOT NULL AUTO_INCREMENT,
    `title`         varchar(255) NOT NULL DEFAULT '',
    `summary`       text,
    `notes`         text,
    `rating`        varchar(255) NOT NULL DEFAULT '',
    `date`          datetime              DEFAULT NULL,
    `updated`       datetime              DEFAULT NULL,
    `categories`    varchar(45)           DEFAULT NULL,
    `tags`          varchar(255) NOT NULL DEFAULT '',
    `warnings`      varchar(255)          DEFAULT '',
    `fandoms`       varchar(255)          DEFAULT '',
    `characters`    varchar(1024)         DEFAULT '',
    `relationships` varchar(1024)         DEFAULT '',
    `language_code` varchar(5)            DEFAULT 'en',
    `url`           varchar(255)          DEFAULT NULL,
    `imported`      tinyint(1)   NOT NULL DEFAULT '0',
    `do_not_import` tinyint(1)   NOT NULL DEFAULT '0',
    `ao3_url`       varchar(255)          DEFAULT NULL,
    `broken_link`   tinyint(1)   NOT NULL DEFAULT '0',
    `import_notes`  varchar(1024)         DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS `tags` (
    `id`                   int(11) AUTO_INCREMENT,
    `original_tagid`       int(11)       DEFAULT NULL,
    `original_tag`         varchar(1024) DEFAULT NULL,
    `original_type`        varchar(255)  DEFAULT NULL,
    `original_parent`      varchar(255)  DEFAULT NULL,
    `original_description` varchar(1024) DEFAULT NULL,
    `ao3_tag`              varchar(1024) DEFAULT NULL,
    `ao3_tag_type`         varchar(255)  DEFAULT NULL,
    `ao3_tag_category`     varchar(255)  DEFAULT NULL,
    `ao3_tag_fandom`       varchar(255)  DEFAULT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8;
  
INSERT INTO `tags` (`id`, `original_tagid`, `original_tag`, `original_type`, `original_parent`, `original_description`, `ao3_tag`, `ao3_tag_type`, `ao3_tag_category`, `ao3_tag_fandom`) VALUES 
(1,1,'G','rating',NULL,'General Audience',NULL,NULL,NULL,NULL),
(2,2,'PG','rating',NULL,'Parental Guidance Suggested',NULL,NULL,NULL,NULL),
(3,3,'PG-13','rating',NULL,'Parents Strongly Cautioned',NULL,NULL,NULL,NULL),
(4,4,'R','rating',NULL,'Restricted-Under 17',NULL,NULL,NULL,NULL),
(5,5,'NC-17','rating',NULL,'No One 17 and Under Admitted',NULL,NULL,NULL,NULL);