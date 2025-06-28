import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# api key and settings
# loads the API key from environment variables
google_api_key = os.getenv("key")

# camera settings 
camera_index = 0  # 0 for the default camera

# gemini api settings
gemini_model_name = "gemini-pro-vision"

# --- Prompts ---
# A detailed prompt for the vision model to guide its analysis
assistive_prompt = (
    "You are an AI assistant for a visually impaired user. "
    "Look at the image and describe only the people you see. "
    "Focus on how many people are present, where they are located (e.g., left, center, right), "
    "and what facial expressions are visible (e.g., smiling, neutral, angry). "
    "Do not describe objects, text, or background details. "
    "Keep the response brief and easy to speak aloud in real time. "
    "Example outputs: "
    "'Two people are in front of you. One is slightly to the left and smiling.' "
    "'One person is standing directly ahead. They appear neutral.' "
    "'Three people are visible. One on the left is smiling, the others look neutral.'"
    )

switch_mode_command = "Switch mode"

wake_word  = "Hello Gemini"

interaction_prompt = (
    ""
    )

pathfinding_prompt = (
    ""
    )

# tts settings
# we can add TTS-specific settings here if needed, like speech rate or volume, but I dont want to do that right now
tts_rate = 150
