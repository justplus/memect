/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50622
 Source Host           : 127.0.0.1
 Source Database       : memect

 Target Server Type    : MySQL
 Target Server Version : 50622
 File Encoding         : utf-8

 Date: 03/20/2015 00:25:11 AM
*/

SET NAMES utf8;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `memect_comment`
-- ----------------------------
DROP TABLE IF EXISTS `memect_comment`;
CREATE TABLE `memect_comment` (
  `id` int(11) NOT NULL COMMENT '编号',
  `comment_content` varchar(1000) DEFAULT NULL COMMENT '评论内容',
  `is_delete` tinyint(4) DEFAULT NULL COMMENT '是否被删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `memect_tag`
-- ----------------------------
DROP TABLE IF EXISTS `memect_tag`;
CREATE TABLE `memect_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `tag_name` varchar(255) NOT NULL COMMENT '标签名称',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_name` (`tag_name`)
) ENGINE=InnoDB AUTO_INCREMENT=651 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `memect_thread`
-- ----------------------------
DROP TABLE IF EXISTS `memect_thread`;
CREATE TABLE `memect_thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `weibo_id` bigint(20) DEFAULT NULL COMMENT '对应的微博编号',
  `weibo_content` text COMMENT '对应的微博内容',
  `memect_type` smallint(6) NOT NULL COMMENT 'memect_type',
  `create_time` date DEFAULT NULL COMMENT '发布日期',
  `memect_category` tinyint(4) DEFAULT NULL COMMENT '所属类别 0:推荐 1:最新动态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `memect_thread_tag`
-- ----------------------------
DROP TABLE IF EXISTS `memect_thread_tag`;
CREATE TABLE `memect_thread_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `thread_id` int(11) DEFAULT NULL COMMENT 'thread编号',
  `tag_name` varchar(50) DEFAULT NULL COMMENT 'tag名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=475 DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `memect_type`
-- ----------------------------
DROP TABLE IF EXISTS `memect_type`;
CREATE TABLE `memect_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `name` varchar(50) NOT NULL COMMENT '分类名称',
  `abbr` varchar(20) DEFAULT NULL COMMENT '分类缩写',
  `url` varchar(255) DEFAULT NULL COMMENT '分类url',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
