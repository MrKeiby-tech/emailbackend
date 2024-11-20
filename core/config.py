import os
from dotenv import load_dotenv

load_dotenv()

current_file_path = os.path.abspath(__file__)

# Получаем путь до директории 'core'
core_dir_path = os.path.dirname(current_file_path)

# Получаем путь до директории 'app'
app_dir_path = os.path.dirname(core_dir_path)


class Config: 
    SERNTRYDNS = os.getenv("SERNTRYDNS")
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")
