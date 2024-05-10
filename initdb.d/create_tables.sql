CREATE TABLE IF NOT EXISTS `task`(
    `message_id` BIGINT NOT NULL,
    `thread_id` BIGINT NOT NULL,
    `deadline` DATETIME NOT NULL,
    PRIMARY KEY (`message_id`)     
);

INSERT INTO `task`(
    `message_id`,`thread_id`,`deadline`
) VALUES (
    "1238547904772313282","1162382305898274836","2024-05-12 02:48:00"
);