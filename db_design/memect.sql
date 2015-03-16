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

 Date: 03/16/2015 21:48:33 PM
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
--  Table structure for `memect_content`
-- ----------------------------
DROP TABLE IF EXISTS `memect_content`;
CREATE TABLE `memect_content` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `weibo_id` bigint(20) DEFAULT NULL COMMENT '对应的微博编号',
  `weibo_content` text COMMENT '对应的微博内容',
  `memect_type` smallint(6) NOT NULL COMMENT 'memect_type',
  `create_time` date DEFAULT NULL COMMENT '发布日期',
  `memect_category` tinyint(4) DEFAULT NULL COMMENT '所属类别 0:推荐 1:最新动态',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `memect_tag`
-- ----------------------------
DROP TABLE IF EXISTS `memect_tag`;
CREATE TABLE `memect_tag` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `tag_name` varchar(255) NOT NULL COMMENT '标签名称',
  `memect_type` smallint(6) DEFAULT NULL COMMENT '对应的memect_type',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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

-- ----------------------------
--  Records of `memect_type`
-- ----------------------------
BEGIN;
INSERT INTO `memect_type` VALUES ('1', 'python日报', 'py', 'http://py.memect.com/'), ('2', '机器学些日报', 'ml', 'http://ml.memect.com/'), ('3', 'web技术日报', 'web', 'http://web.memect.com/'), ('4', '大数据日报', 'bd', 'http://bd.memect.com/'), ('5', 'app开发日报', 'app', 'http://app.memect.com/');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
