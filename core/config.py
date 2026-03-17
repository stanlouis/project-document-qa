# core/config.py
from openai import OpenAI

# Initialize the client once to be imported by other modules
# Pointing to a local Ollama server via its OpenAI-compatible API endpoint
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)