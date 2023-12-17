from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Access the environment variables within your FastAPI application
DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG")