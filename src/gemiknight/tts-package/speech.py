import pyttsx3
import logging

logger = logging.getLogger(__name__)

class TTSEngine:
    # wrapper for pyttsx3
    def __init__(self, rate: int = 150):
        # this initalizes the TTS engine with a specified speaking rate.
        # rate (int): this is the speaking rate in words per minute.
        try:
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', rate)
            logger.info("TTS engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine: {e}")
            self.engine = None

    def speak(self, text: str):

        # speaks the text aloud

        # text (str): The text to be spoken

        if not self.engine:
            logger.error("TTS engine not available. Cannot speak.")
            return

        if not text:
            logger.warning("No text provided to speak.")
            return
            
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            logger.error(f"An error occurred during speech synthesis: {e}")