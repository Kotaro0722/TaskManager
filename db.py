from mydblib import my_update
import config

dbname=config.DBNAME
task_table=config.TASK_TABLE

sql_drop_db=f"DROP DATABASE IF EXISTS {dbname};"
sql_create_db=f"CREATE DATABASE IF NOT EXISTS {dbname};"
sql_use_db=f"USE {dbname};"
sql_drop_table=f"DROP TABLE IF EXISTS {task_table}"
sql_create_table=f"""
    CREATE TABLE IF NOT EXISTS {task_table}
        (message_id BIGINT NOT NULL,
         thread_id BIGINT NOT NULL,
         deadline DATETIME NOT NULL,
         PRIMARY KEY (message_id)     
    );"""


my_update(dbname,sql_create_table)