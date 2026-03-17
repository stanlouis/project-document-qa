# core/config.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize the client once to be imported by other modules
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))