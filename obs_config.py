from dotenv import load_dotenv
import os

load_dotenv()

host = os.getenv("OBS_HOST")
port = int(os.getenv("OBS_PORT"))
password = os.getenv("OBS_PASSWORD")
