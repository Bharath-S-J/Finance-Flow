
CREATE TABLE `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT 'admin',
  `address` varchar(500) DEFAULT 'adress',
  `email` varchar(100) DEFAULT 'email',
  `phone1` varchar(20) DEFAULT 'phone_1',
  `phone2` varchar(20) DEFAULT 'phone_2',
  `discription` varchar(1000) DEFAULT 'discription',
  `goals` varchar(100) DEFAULT 'goals',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `customer` (
  `loan_acc_number` int NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(45) DEFAULT NULL,
  `customer_mobie` varchar(45) DEFAULT NULL,
  `loan_name` varchar(45) DEFAULT NULL,
  `principal_amount` int DEFAULT NULL,
  `total_amount` int DEFAULT NULL,
  `remaining_amount` int DEFAULT NULL,
  `loan_ten_year` int DEFAULT NULL,
  `loan_ten_month` int DEFAULT NULL,
  `remaing_tenure_number` int DEFAULT NULL,
  `EMI` int DEFAULT NULL,
  `interest_type` varchar(45) DEFAULT NULL,
  `interest` decimal(4,2) DEFAULT NULL,
  `pre_payment_intrest` decimal(4,2) DEFAULT NULL,
  `late_payment_intrest` decimal(4,2) DEFAULT NULL,
  `loan_start_date` date DEFAULT NULL,
  `loan_end_date` date DEFAULT NULL,
  `total_amount_paid` int DEFAULT '0',
  `last_pay_date` date DEFAULT NULL,
  `sanctioned_amount` int DEFAULT NULL,
  PRIMARY KEY (`loan_acc_number`)
) ENGINE=InnoDB AUTO_INCREMENT=20221207 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `phone` varchar(45) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `acc_number` varchar(45) DEFAULT NULL,
  `date_payed` datetime DEFAULT NULL,
  `loan_name` varchar(45) DEFAULT NULL,
  `emi` int DEFAULT NULL,
  `principal_paid` int DEFAULT NULL,
  `interest_paid` int DEFAULT NULL,
  `remaining_amount` int DEFAULT NULL,
  `paid_amount` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `loan` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `maxamount` int DEFAULT NULL,
  `intrat` decimal(4,2) DEFAULT NULL,
  `inttype` varchar(45) DEFAULT NULL,
  `loanten` varchar(45) DEFAULT NULL,
  `prepaypen` decimal(4,2) DEFAULT NULL,
  `penint` decimal(4,2) DEFAULT NULL,
  `recdoc` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`,`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(45) DEFAULT NULL,
  `password` varchar(25) DEFAULT NULL,
  `userphone1` varchar(15) DEFAULT NULL,
  `useraddress1` varchar(300) DEFAULT NULL,
  `useraddress2` varchar(300) DEFAULT NULL,
  `userphone2` varchar(15) DEFAULT NULL,
  `useremail` varchar(45) DEFAULT NULL,
  `adharnumber` varchar(45) DEFAULT NULL,
  `pannumber` varchar(45) DEFAULT NULL,
  `photo` longblob,
  `pancardphoto` longblob,
  `adharcardphoto` longblob,
  `loanscheme` varchar(50) DEFAULT NULL,
  `fathername` varchar(45) DEFAULT NULL,
  `mothername` varchar(45) DEFAULT NULL,
  `motherphonenumber` varchar(45) DEFAULT NULL,
  `familyincome` int DEFAULT NULL,
  `pincode` int DEFAULT NULL,
  `bankaccnumber` varchar(45) DEFAULT NULL,
  `bankifsc` varchar(45) DEFAULT NULL,
  `passbookphoto` longblob,
  `doc1` varchar(45) DEFAULT NULL,
  `doc2` varchar(45) DEFAULT NULL,
  `doc3` varchar(45) DEFAULT NULL,
  `doc4` varchar(45) DEFAULT NULL,
  `amountrec` int DEFAULT NULL,
  `tenure` int DEFAULT NULL,
  `submitdate` datetime DEFAULT NULL,
  `status` varchar(5) DEFAULT NULL,
  `remark` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
