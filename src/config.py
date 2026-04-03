# src/config.py
import os
from dotenv import load_dotenv

def load_config():
    """Loads and strictly validates required environment variables."""
    load_dotenv()
    
    config = {
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
        "DATABRICKS_HOST": os.getenv("DATABRICKS_HOST"),
        "DATABRICKS_TOKEN": os.getenv("DATABRICKS_TOKEN")
    }
    
    if not config["GROQ_API_KEY"]:
        raise ValueError("CRITICAL ERROR: GROQ_API_KEY is missing in the .env file.")
        
    return config

CONFIG = load_config()