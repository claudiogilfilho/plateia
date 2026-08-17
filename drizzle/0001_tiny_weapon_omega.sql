CREATE TABLE `analyses` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`contentType` enum('post','carrossel','reel','copy') NOT NULL,
	`contentText` text NOT NULL,
	`product` varchar(300) NOT NULL,
	`objective` varchar(300) NOT NULL,
	`targetAudience` text NOT NULL,
	`mediaUrl` text,
	`mediaKey` varchar(1024),
	`mediaMimeType` varchar(120),
	`status` enum('processing','completed','failed') NOT NULL DEFAULT 'processing',
	`reportJson` text,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `analyses_id` PRIMARY KEY(`id`)
);
