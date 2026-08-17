ALTER TABLE `analyses` ADD `sourceUrl` text;--> statement-breakpoint
ALTER TABLE `analyses` ADD `sourceKind` enum('direct_media','published_post');--> statement-breakpoint
ALTER TABLE `analyses` ADD `sourceMediaMimeType` varchar(120);