# vision/gemini_api.py

import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class GeminiAPI:

    # wrapper for google gemini vision API

    def __init__(self, api_key: str, model_name: str):
        # initializes the Gemini model.

        # api_key (str): The Google API key.

        # model_name (str): The name of the Gemini model to use.

        if not api_key:
            raise ValueError("Google API key is missing.")
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Gemini model '{model_name}' loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to configure Gemini AI: {e}")
            raise

    def analyze_image(self, prompt: str, image_bytes: bytes) -> str:

        # sends an image and a prompt to the Gemini API for analysis

        # prompt (str): The text prompt to guide the analysis

        # image_bytes (bytes): The JPEG image data

        # str: the textual description from the API or an error message

        if not image_bytes:
            return "Cannot analyze as no image was provided."

        image_part = {"mime_type": "image/jpeg", "data": image_bytes}
        
        try:
            logger.info("Sending request to Gemini API...")
            response = self.model.generate_content([prompt, image_part])
            return response.text
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return f"Sorry, I could not analyze the image. Error: {e}"