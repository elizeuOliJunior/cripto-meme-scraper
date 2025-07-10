from dotenv import load_dotenv
import os

load_dotenv()
FIREBASE_DB_URL = os.getenv("FIREBASE_DB_URL")
