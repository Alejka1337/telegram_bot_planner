import os
from pathlib import Path
from dotenv import dotenv_values

dotenv_path = os.path.join(Path(__file__).resolve().parent, '.env')

TG_TOKEN = dotenv_values(dotenv_path)['TG_TOKEN']
DATABASE_TYPE = dotenv_values(dotenv_path)['DATABASE_TYPE']
USERNAME = dotenv_values(dotenv_path)['USERNAME']
PASSWORD = dotenv_values(dotenv_path)['PASSWORD']
DATABASE_NAME = dotenv_values(dotenv_path)['DATABASE_NAME']
PORT = dotenv_values(dotenv_path)['PORT']

