import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID")  # Custom Search Engine ID
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 465))
EMAIL_PASS = os.getenv("EMAIL_PASS")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Local paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
REPORTS_DIR = os.path.join(DATA_DIR, "reports")
STARTUPS_JSON = os.path.join(DATA_DIR, "startups.json")

# Ensure data directories exist
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)