import os
from dotenv import load_dotenv
load_dotenv()

TOKEN=os.getenv("TOKEN")

HOST=os.getenv("HOST")
USER=os.getenv("USER")
PASSWORD=os.getenv("PASSWORD")
PORT=os.getenv("PORT")

DBNAME=os.getenv("DBNAME")
TASK_TABLE=os.getenv("TASK_TABLE")
THREAD_TABLE=os.getenv("THREAD_TABLE")