import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# api key
google_api_key = os.getenv("key")

# camera settings
camera_index = 0  # 0 for the default camera

# api settings 
gemini_model_name = "gemini-pro-vision"

# prompts

# pathing mode
pathfinding_prompt = (
    "You are an AI assistant for a visually impaired user in pathfinding mode. "
    "Describe the scene with a focus on navigation. Identify pathways, doors, potential obstacles like chairs, steps, or cables on the floor. "
    "Describe the general layout of the room or area. Keep descriptions concise and actionable. "
    "Example: 'You are in a hallway. There is a closed door directly in front of you. The path to your right is clear.'"
)

# interaction mode
interaction_prompt = (
    "You are an AI assistant for a visually impaired user in interaction mode. "
    "Describe the scene with a focus on people and objects for interaction. "
    "Identify any people, their approximate distance, and their facial expressions if visible. "
    "Read any clear text on signs or objects. "
    "Example: 'A person is standing about 5 feet in front of you, smiling. They are holding a cup.'"
)

# -voice activation word
wake_word = "hey gemini"

switch_mode_command = "switch mode"

# tts settings
tts_rate = 160
