from pathlib import Path
from dotenv import load_dotenv

def load_settings():
    return load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
