CREATE TABLE `admin` (
  `id` int NOT NULL,
  `username` varchar(24) DEFAULT NULL,
  `password` char(32) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='管理员表';

CREATE TABLE `bonous` (
  `bonousno` bigint unsigned NOT NULL AUTO_INCREMENT,
  `sno` bigint NOT NULL,
  `sname` varchar(24) DEFAULT NULL,
  `dno` int DEFAULT NULL,
  `dname` varchar(24) DEFAULT NULL,
  `bonous` decimal(10,0) NOT NULL COMMENT '奖金',
  `cause` text NOT NULL COMMENT '奖励原因',
  `date` date NOT NULL COMMENT '奖励日期',
  PRIMARY KEY (`bonousno`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3 COMMENT='奖金表';

CREATE TABLE `department` (
  `dno` int NOT NULL,
  `dname` varchar(20) DEFAULT NULL COMMENT '部门名',
  `nop` int DEFAULT NULL COMMENT 'number of people',
  `avesalary` decimal(10,0) DEFAULT NULL COMMENT '部门平均工资',
  `date` date DEFAULT NULL COMMENT '发工资日期',
  PRIMARY KEY (`dno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='部门';

CREATE TABLE `fine` (
  `fineno` bigint unsigned NOT NULL AUTO_INCREMENT,
  `sno` bigint NOT NULL,
  `sname` varchar(24) DEFAULT NULL,
  `dno` int DEFAULT NULL,
  `dname` varchar(24) DEFAULT NULL,
  `date` date NOT NULL COMMENT '罚款日期',
  `cause` text CHARACTER SET utf8 COLLATE utf8_general_ci COMMENT '罚款原因',
  `fine` decimal(10,0) NOT NULL COMMENT '单次罚金',
  PRIMARY KEY (`fineno`,`sno`)
) ENGINE=InnoDB AUTO_INCREMENT=238 DEFAULT CHARSET=utf8mb3 COMMENT='罚金';

CREATE TABLE `salary` (
  `sno` bigint NOT NULL,
  `sname` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `dno` int DEFAULT NULL,
  `dname` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `date` date NOT NULL COMMENT '发工资时间，只管年月，固定日',
  `bsalary` decimal(10,0) NOT NULL COMMENT '基本工资',
  `sumbonous` decimal(10,0) DEFAULT '0' COMMENT '总奖金',
  `sumfine` decimal(10,0) DEFAULT '0' COMMENT '总罚金',
  `sumsalary` decimal(10,0) DEFAULT '0' COMMENT '税后总工资',
  PRIMARY KEY (`sno`,`date`),
  KEY `depno` (`dno`),
  CONSTRAINT `depno` FOREIGN KEY (`dno`) REFERENCES `department` (`dno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='工资表';

CREATE TABLE `staff_info` (
  `sno` int NOT NULL AUTO_INCREMENT,
  `sname` varchar(24) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `dno` int DEFAULT NULL,
  `dname` varchar(24) DEFAULT NULL,
  `position` varchar(24) DEFAULT NULL,
  `age` tinyint DEFAULT NULL,
  `gender` char(1) DEFAULT NULL COMMENT 'm男，f女',
  `phone` varchar(24) DEFAULT NULL,
  `education` varchar(24) DEFAULT NULL,
  `bsalary` decimal(10,0) DEFAULT NULL COMMENT '基本工资',
  `allowance` decimal(10,0) DEFAULT NULL COMMENT '津贴',
  `annualbonous` decimal(10,0) DEFAULT NULL COMMENT '年终奖',
  `entrydate` date DEFAULT NULL COMMENT '入职日期',
  `password` char(32) DEFAULT NULL,
  PRIMARY KEY (`sno`),
  KEY `fk_staff_dep` (`dno`),
  CONSTRAINT `fk_staff_dep` FOREIGN KEY (`dno`) REFERENCES `department` (`dno`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3004 DEFAULT CHARSET=utf8mb3 COMMENT='员工基本信息：员工号，姓名，部门，职位，年龄，性别，电话，学历，基本工资,入职时间';

