import speech_recognition as sr
import time
import logging as log # for logging/debugging
from gemiknight.settings import wake_word

logger = log.getLogger(__name__)

class VoiceActivation:
    # Constructor
    def __init__(self, wake_word: str):
        self.wake_word = wake_word.lower()
        self.r = sr.Recognizer()
        # Calibrate once for efficiency
        with sr.Microphone() as source:
            logger.info("Calibrating for ambient noise...")
            self.r.adjust_for_ambient_noise(source, duration=0.5)
            logger.info("Calibration complete.")

    def start_voice(self):
        # Listen for a wake word or command
        logger.info("Listening...")
        with sr.Microphone() as mic:
            try:
                # This logic is now correctly inside the 'try' block
                audio = self.r.listen(mic)
                logger.info("Recognizing Words.....")
                words = self.r.recognize_google(audio).lower()

                # Add this debug line to always see what Google heard
                logger.info(f"Google recognized: '{words}'")

                # --- THE FIX ---
                # Check for single words OR longer phrases for each mode.
                if "interaction" in words:
                    logger.info("Interaction mode command detected!")
                    return "Interaction"

                if "pathing" in words or "passing" in words:
                    logger.info("Pathing mode command detected!")
                    return "Pathing"
                
                if "freeform" in words:
                    logger.info("Freeform mode command detected!")
                    return "Freeform"
                
                # Fallback to the general wake word
                if self.wake_word in words:
                    logger.info("Wake Word found!!!!! 😊")
                    return words.partition(self.wake_word)[2].strip()

            except sr.UnknownValueError:
                logger.error("Google could not understand audio, try again.")
            except sr.RequestError as err:
                logger.error(f"Google request did not go through: {err}")
            except Exception as err:
                print(f"Some other error occured: {err}")
        
        return None