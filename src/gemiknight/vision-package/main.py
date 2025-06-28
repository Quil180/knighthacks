# main.py

import logging
from utils.logger import setup_logger  # Sets up the logger first
from config import settings
from vision.camera import Camera
from vision.gemini_api import GeminiAPI
from tts.speech import TTSEngine

# Initialize the centralized logger
logger = logging.getLogger(__name__)

def run_vision_assistance():

    # main function to run the complete vision assistance pipeline

    # checks for API Key
    if not settings.GOOGLE_API_KEY:
        logger.error("FATAL: GOOGLE_API_KEY is not set in the environment.")
        print("Error: GOOGLE_API_KEY is not configured. Please check your .env file.")
        return

    try:
        # initializes all modules
        logger.info("Initializing system modules...")
        camera = Camera(camera_index=settings.CAMERA_INDEX)
        gemini = GeminiAPI(api_key=settings.GOOGLE_API_KEY, model_name=settings.GEMINI_MODEL_NAME)
        tts = TTSEngine(rate=settings.TTS_RATE)

        # this is where your main application loop would go!
        # for this example, we'll simulate a single trigger, like a voice command....
        input("Press Enter to capture and analyze the scene...") # simulates a trigger

        # self explanatory.. captures an image
        logger.info("Capturing image...")
        tts.speak("Looking now.")
        image_bytes = camera.capture_jpeg_bytes()

        if not image_bytes:
            error_message = "Failed to capture image. Please check the camera."
            logger.error(error_message)
            tts.speak(error_message)
            return

        # 4. analyze the image with Gemini
        logger.info("Analyzing image with Gemini...")
        description = gemini.analyze_image(
            prompt=settings.ASSISTIVE_PROMPT,
            image_bytes=image_bytes
        )

        # 5. outputs the result!
        print("\n--- Scene Description ---")
        print(description)
        print("-------------------------\n")
        tts.speak(description)

    except IOError as e:
        logger.error(f"Camera hardware error: {e}")
        print(f"A camera error occurred: {e}")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in the main loop: {e}", exc_info=True)
        print(f"A critical error occurred. Check logs for details.")
    finally:
        logger.info("Vision assistance application shutting down.")
        
        # the camera is released automatically by its destructor..
        # but you could add explicit cleanup here if needed.

if __name__ == "__main__":
    run_vision_assistance()