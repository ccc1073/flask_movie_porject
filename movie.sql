-- MySQL dump 10.13  Distrib 8.0.11, for macos10.13 (x86_64)
--
-- Host: localhost    Database: movie
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `adminer`
--

DROP TABLE IF EXISTS `adminer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `adminer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `is_super` smallint(6) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `role_id` (`role_id`),
  KEY `ix_adminer_addtime` (`addtime`),
  CONSTRAINT `adminer_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminer`
--

LOCK TABLES `adminer` WRITE;
/*!40000 ALTER TABLE `adminer` DISABLE KEYS */;
INSERT INTO `adminer` VALUES (1,'imoocmovie','pbkdf2:sha256:50000$eCarWlIi$3343b9b6e152dc6138dd4c4702eb3f7c4892405f6bcb0edafb38259a046d8468',0,1,'2018-10-04 16:43:19'),(2,'imoocmovie1','pbkdf2:sha256:50000$dPMfp8qn$57081b279f0f79f000b41141c319dabbf9ea5aed6426dd96a8f5d5f1ab15f5af',0,1,'2018-10-05 08:19:21'),(3,'movieadmin','pbkdf2:sha256:50000$fpmBvNQa$2afa7506e36072b68321f4c5d0b4ffbebb3a20922bb744889a5ff06d4265e4c0',1,4,'2018-10-06 05:14:53');
/*!40000 ALTER TABLE `adminer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminlog`
--

DROP TABLE IF EXISTS `adminlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `adminlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_adminlog_addtime` (`addtime`),
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `adminer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminlog`
--

LOCK TABLES `adminlog` WRITE;
/*!40000 ALTER TABLE `adminlog` DISABLE KEYS */;
INSERT INTO `adminlog` VALUES (1,2,'127.0.0.1','2018-10-05 11:07:42'),(2,2,'127.0.0.1','2018-10-05 11:07:42'),(3,2,'127.0.0.1','2018-10-05 12:17:34'),(4,2,'127.0.0.1','2018-10-06 02:12:42'),(5,2,'127.0.0.1','2018-10-06 05:02:02'),(6,2,'127.0.0.1','2018-10-06 05:04:12'),(7,3,'127.0.0.1','2018-10-06 05:14:53'),(8,2,'127.0.0.1','2018-10-06 12:32:30'),(9,2,'127.0.0.1','2018-10-06 12:59:13');
/*!40000 ALTER TABLE `adminlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('5eaef59da96d');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `url` (`url`),
  KEY `ix_auth_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (1,'添加标签','admin/tag/add/','2018-10-05 12:42:04'),(2,'标签列表','admin/tag/list/<int:page>/','2018-10-05 12:42:04'),(3,'删除标签','admin/tag/del/<int:id>/','2018-10-05 12:42:04'),(5,'编辑标签','admin/tag/edit/<int:id>/','2018-10-05 12:42:04'),(6,'添加电影','admin/movie/add/','2018-10-06 04:46:51'),(7,'电影列表','admin/movie/list/<int:page>','2018-10-06 04:46:51'),(8,'删除电影','admin/movie/del/<int:id>','2018-10-06 04:46:51');
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_comment_addtime` (`addtime`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (1,'好看',1,1,'2018-10-05 14:47:41'),(3,'给力',2,3,'2018-10-05 14:47:41'),(4,'经典！！！',1,4,'2018-10-05 14:47:41'),(5,'无感~~',2,5,'2018-10-05 14:47:43');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movie`
--

DROP TABLE IF EXISTS `movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `movie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `info` text,
  `logo` varchar(255) DEFAULT NULL,
  `star` smallint(6) DEFAULT NULL,
  `playnum` bigint(20) DEFAULT NULL,
  `commentnum` bigint(20) DEFAULT NULL,
  `tag_id` int(11) DEFAULT NULL,
  `area` varchar(255) DEFAULT NULL,
  `release_time` date DEFAULT NULL,
  `length` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `title` (`title`),
  UNIQUE KEY `url` (`url`),
  KEY `tag_id` (`tag_id`),
  KEY `ix_movie_addtime` (`addtime`),
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movie`
--

LOCK TABLES `movie` WRITE;
/*!40000 ALTER TABLE `movie` DISABLE KEYS */;
INSERT INTO `movie` VALUES (1,'冰海陷落','2018100511553411c051f50a03420cbd8c756f54410b2f.mp4','科幻电影~~~','2018100511553403356612762f4a2fac64233e57e3dcc2.png',5,2,0,1,'北美','2018-10-04','1:27','2018-10-05 03:53:59'),(2,'蜘蛛线 平行世界','20181005144531b777f4186dfe46d0a0dccfbb36f3877d.mp4','蜘蛛侠~~~~~~~~~~1','20181005144531a926152cb473480c882011a581ca2b15.png',5,3,0,2,'南美','2018-10-11','2:45','2018-10-05 06:43:01'),(3,'超胆侠','20181006204631900a9cd4d4eb428d97b1de6c3f977181.mp4','飞起~~~~~','20181006204631de9ecb58cb0a4a5fb4e65ec7f77bfb3b.jpg',4,0,0,2,'中国','2018-10-25','2:22','2018-10-06 12:32:30'),(4,'新灰姑娘','2018100620482894202c6a33dc423eaf5d02aea2ae5085.mp4','啦啦啦啦啦 玻璃鞋','201810062048285879a6313e274e308b7079c190d82e57.jpg',4,0,0,3,'欧洲','2018-10-10','1：36','2018-10-06 12:32:30'),(5,'古剑奇谭','2018100620493321e8c735eba14142a1139dec33d2f75f.mp4','游戏游戏游戏~~~~','2018100620493340116a9a8125488f8bb0607ecc6c5ae1.jpg',3,0,0,2,'中国','2018-10-03','2:22','2018-10-06 12:32:30'),(6,'霍格沃茨','201810062050453d4e1a9ec1034416bf352c19c89325ea.mp4','魔法魔法魔法~','2018100620504517ca3c3915d64f3d94871b3815db6ad2.jpg',5,0,0,1,'欧洲','2018-10-11','2：11','2018-10-06 12:32:30');
/*!40000 ALTER TABLE `movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `moviecol`
--

DROP TABLE IF EXISTS `moviecol`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `moviecol` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `movie_id` (`movie_id`),
  KEY `user_id` (`user_id`),
  KEY `ix_moviecol_addtime` (`addtime`),
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`),
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `moviecol`
--

LOCK TABLES `moviecol` WRITE;
/*!40000 ALTER TABLE `moviecol` DISABLE KEYS */;
INSERT INTO `moviecol` VALUES (2,1,3,'2018-10-05 15:06:25'),(3,2,1,'2018-10-05 15:06:25'),(4,2,4,'2018-10-05 15:06:25'),(5,1,5,'2018-10-05 15:06:27');
/*!40000 ALTER TABLE `moviecol` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oplog`
--

DROP TABLE IF EXISTS `oplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `oplog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `reason` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `admin_id` (`admin_id`),
  KEY `ix_oplog_addtime` (`addtime`),
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `adminer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oplog`
--

LOCK TABLES `oplog` WRITE;
/*!40000 ALTER TABLE `oplog` DISABLE KEYS */;
INSERT INTO `oplog` VALUES (1,2,'127.0.0.1','添加标签爱情','2018-10-05 11:12:52'),(2,2,'127.0.0.1','添加标签历史','2018-10-05 11:12:52');
/*!40000 ALTER TABLE `oplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `preview`
--

DROP TABLE IF EXISTS `preview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `preview` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `logo` (`logo`),
  UNIQUE KEY `title` (`title`),
  KEY `ix_preview_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `preview`
--

LOCK TABLES `preview` WRITE;
/*!40000 ALTER TABLE `preview` DISABLE KEYS */;
INSERT INTO `preview` VALUES (1,'冰海陷落','20181005131822c06684c628584f9a9a71935e61683619.jpg','2018-10-05 05:17:46'),(3,'滑稽的微笑','20181006203635943d0136b2e54f48a734eab2fcc2de52.png','2018-10-06 12:32:30'),(4,'蜘蛛侠','20181006203650ddf0e1fce2734f5594cec5c1c36da211.png','2018-10-06 12:32:30'),(5,'新灰姑娘','20181006210843100cb0135dd940639c7d8999fa84a298.jpg','2018-10-06 13:07:15'),(6,'古剑奇谭','201810062109014b1f5e61e2824493ba6d0cb893bd2655.jpg','2018-10-06 13:07:15'),(7,'超胆侠','20181006210921a3187591ebfb47e9843bd2fa8e37f428.jpg','2018-10-06 13:07:15');
/*!40000 ALTER TABLE `preview` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `auths` varchar(600) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_role_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'超级管理员',' ','2018-10-04 16:43:19'),(2,'超级管理员1',' ','2018-10-05 08:19:21'),(4,'电影管理员','6,7,8','2018-10-06 05:04:12'),(5,'标签管理员','1,2,3,5','2018-10-06 05:14:53');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag`
--

DROP TABLE IF EXISTS `tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `ix_tag_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag`
--

LOCK TABLES `tag` WRITE;
/*!40000 ALTER TABLE `tag` DISABLE KEYS */;
INSERT INTO `tag` VALUES (1,'科幻','2018-10-04 16:44:12'),(2,'动作','2018-10-04 16:44:12'),(3,'爱情','2018-10-05 11:12:52'),(4,'历史','2018-10-05 11:12:52');
/*!40000 ALTER TABLE `tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `info` text,
  `face` varchar(255) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  `uuid` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `face` (`face`),
  UNIQUE KEY `name` (`name`),
  UNIQUE KEY `phone` (`phone`),
  UNIQUE KEY `uuid` (`uuid`),
  KEY `ix_user_addtime` (`addtime`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'鸡','1240','12390@163.com','13888888991','鸡','1f4p3.png','2018-10-05 14:10:24','d32a72bdac524478b7e4f6dc8394fc1'),(3,'够','1240','1259@163.com','13888888992','狗','1t413.png','2018-10-05 14:16:48','d32a72bdac524478b7e4f6dc8394fc2'),(4,'鱼','1240','12e9@163.com','13888888993','鱼','1f213.png','2018-10-05 14:16:48','d32a72bdac524478b7e4f6dc8394fc3'),(5,'猫','1240','123t9@163.com','13888888994','猫','1f417.png','2018-10-05 14:16:48','d32a72bdac524478b7e4f6dc8394fc4'),(6,'狐狸','1240','12329@163.com','13888888995','狐狸','1f513.png','2018-10-05 14:16:48','d32a72bdac524478b7e4f6dc8394fc5'),(7,'浣熊','1240','123u9@163.com','13888888996','浣熊','1k413.png','2018-10-05 14:16:55','d32a72bdac524478b7e4f6dc8394fc6'),(8,'kumu','pbkdf2:sha256:50000$ZDQmYOUH$81ed0009e44c985464cf86dd881549daf1f94ed61fd319c8fbdba0a047d8d7fc','1qe234@qq.com','13803112068','巴拉巴拉巴拉巴拉','1111.jpg','2018-10-06 15:41:20','5dabef9c444d4b1c98235da81109ce72');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userlog`
--

DROP TABLE IF EXISTS `userlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `userlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `ip` varchar(100) DEFAULT NULL,
  `addtime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_userlog_addtime` (`addtime`),
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userlog`
--

LOCK TABLES `userlog` WRITE;
/*!40000 ALTER TABLE `userlog` DISABLE KEYS */;
/*!40000 ALTER TABLE `userlog` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-07  2:06:38
