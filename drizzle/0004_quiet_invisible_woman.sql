CREATE TABLE `instagramConnections` (
	`id` int AUTO_INCREMENT NOT NULL,
	`userId` int NOT NULL,
	`instagramUserId` varchar(80),
	`username` varchar(120),
	`accountType` enum('business','creator') NOT NULL DEFAULT 'business',
	`status` enum('ready','connected','expired','revoked','error') NOT NULL DEFAULT 'ready',
	`grantedScopes` text,
	`accessTokenEncrypted` text,
	`tokenExpiresAt` timestamp,
	`consentVersion` varchar(32),
	`connectedAt` timestamp,
	`revokedAt` timestamp,
	`createdAt` timestamp NOT NULL DEFAULT (now()),
	`updatedAt` timestamp NOT NULL DEFAULT (now()) ON UPDATE CURRENT_TIMESTAMP,
	CONSTRAINT `instagramConnections_id` PRIMARY KEY(`id`)
);
