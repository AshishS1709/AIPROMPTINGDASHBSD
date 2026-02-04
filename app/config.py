import os
import sys
from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

# Manually load .env file to ensure variables are present
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(ROOT_DIR, ".env")

print(f"DEBUG: Config initializing...")
print(f"DEBUG: Resolution path: {ENV_PATH}")

if os.path.exists(ENV_PATH):
    print("DEBUG: Found .env file, loading...")
    load_dotenv(ENV_PATH, override=True, encoding="utf-8-sig")
else:
    print("DEBUG: ERROR - .env file NOT FOUND at expected path!")
    # List directory to see what's actually there
    try:
        print(f"DEBUG: Contents of {ROOT_DIR}: {os.listdir(ROOT_DIR)}")
    except Exception as e:
        print(f"DEBUG: Failed to list dir: {e}")

# Check if keys are actually loaded in env
print(f"DEBUG: Env GROQ_API_KEY present? {'GROQ_API_KEY' in os.environ}")

class Settings(BaseSettings):
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    # Make HF optional to isolate the issue if needed, but keeping explicitly required for now as per user request history
    HUGGINGFACE_API_KEY: str = Field(..., env="HUGGINGFACE_API_KEY")
    OUTPUT_DIR: str = "output"

    class Config:
        env_file = None # Disable pydantic auto-loading since we did it manually
        env_file_encoding = "utf-8"

try:
    settings = Settings()
    print("DEBUG: Settings validation passed")
except Exception as e:
    print("DEBUG: Settings validation FAILED")
    print(f"DEBUG: Current Env Keys: {[k for k in os.environ.keys() if 'KEY' in k]}")
    raise e
