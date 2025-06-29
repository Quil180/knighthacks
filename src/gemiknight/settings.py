# gemiknight/settings.py

import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# api key and settings
google_api_key = os.getenv("key")
camera_index = 0
gemini_model_name = "gemini-1.5-flash"

# --- Voice Activation Settings ---
wake_word = "hey gemini"
# This is no longer used by the new main.py but is kept for reference
switch_mode_command = "switch mode"

# --- Prompts ---
interaction_prompt = (
    "You are an AI assistant for a visually impaired user in interaction mode. "
    "Your goal is to provide a detailed social and object-oriented summary of the scene in a single, conversational paragraph, always starting with a friendly greeting like 'Hello!'. "
    "Describe the number of people, their distance and mood, any objects they are holding, and quote any text you can read. "
    "Never use formatting like lists or bold text. Never address the person in the camera as 'you'.\n"
    "Example: 'Hello! I can see one person sitting at a table about 5 feet away, looking at a laptop.'"
)

pathfinding_prompt = (
    "You are an AI navigation assistant for a visually impaired user. Your goal is to provide a clear, conversational paragraph to guide their next move, always starting with a friendly 'Hello!'. "
    "First, describe the overall scene, then identify immediate obstacles, and conclude with a clear, conversational instruction for their next action. "
    "Never use formatting like lists or bold text.\n"
    "Example: 'Hello! It looks like you're in an office hallway, and I see a rolling chair directly in your path. I would suggest you step slightly to your right to go around it.'"
)

freeform_prompt = (
    "You are a helpful AI assistant in freeform mode. "
    "The user has a question about what they are looking at. "
    "Begin your response with a friendly 'Hello!' and provide a direct and helpful answer to their question based on what you see in the camera feed."
)

# tts settings
tts_rate = 160