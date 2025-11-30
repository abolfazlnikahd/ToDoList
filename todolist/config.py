import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/todolist")
MAX_NUMBER_OF_PROJECT = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
MAX_NUMBER_OF_TASK = int(os.getenv("MAX_NUMBER_OF_TASK", "200"))
