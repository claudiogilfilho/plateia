ALTER TABLE `observatoryPatterns`
  MODIFY COLUMN `stage` enum('observation','hypothesis','supported_hypothesis','provisional','validated','experimentally_validated','contradicted','inconclusive','obsolete','archived') NOT NULL DEFAULT 'hypothesis';

ALTER TABLE `observatoryPatterns` ADD COLUMN `patternType` varchar(80) NOT NULL DEFAULT 'outro' AFTER `name`;

UPDATE `observatoryPatterns` SET `stage` = 'experimentally_validated' WHERE `stage` = 'validated';
UPDATE `observatoryPatterns` SET `stage` = 'archived' WHERE `stage` = 'obsolete';
ALTER TABLE `observatoryPatterns`
  MODIFY COLUMN `stage` enum('observation','hypothesis','supported_hypothesis','provisional','experimentally_validated','contradicted','inconclusive','archived') NOT NULL DEFAULT 'hypothesis';
UPDATE `observatoryReferences` SET `promptVersion` = '3.0' WHERE `promptVersion` = '2.0';
