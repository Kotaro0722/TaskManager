CREATE TABLE IF NOT EXISTS `task`(
    `message_id` BIGINT NOT NULL,
    `thread_id` BIGINT NOT NULL,
    `deadline` DATETIME NOT NULL,
    PRIMARY KEY (`message_id`)     
);