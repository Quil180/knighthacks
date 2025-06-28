import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

class VoiceActivation:
    # handles voice activation and command transcription using speech_recognition

    def __init__(self, wake_word: str = "hey gemini", ambient_adjust_duration: float = 0.5):
        # initializes the voice recognizer
        logger.info("Initializing VoiceActivation...")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = wake_word.lower()
        
        # --- important: calibrate for ambient noise only once for efficiency
        with self.microphone as source:
            logger.info(f"Calibrating for ambient noise ({ambient_adjust_duration}s)...")
            self.recognizer.adjust_for_ambient_noise(source, duration=ambient_adjust_duration)
        logger.info("Calibration complete.")

    def listen_for_wake_word(self) -> bool:
        # listens continuously for the wake word
        logger.info(f"Listening for wake word: '{self.wake_word}'...")
        with self.microphone as source:
            try:
                # use a shorter listen timeout here to be more responsive
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = self.recognizer.recognize_google(audio).lower()
                logger.info(f"Heard: '{text}'")
                
                if self.wake_word in text:
                    logger.info("Wake word detected!")
                    return True
            except sr.WaitTimeoutError:
                # this is not an error, just means no speech was detected
                logger.debug("Listening for wake word timed out.")
            except sr.UnknownValueError:
                logger.debug("Could not understand audio while listening for wake word.")
            except sr.RequestError as e:
                logger.error(f"Google API request failed: {e}")
        
        return False

    def listen_for_command(self) -> str:
        # listens for and transcribes a single command after activation
        logger.info("Listening for a command...")
        with self.microphone as source:
            try:
                # give the user more time to speak the command
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = self.recognizer.recognize_google(audio).lower()
                logger.info(f"Command heard: '{command}'")
                return command
            except sr.WaitTimeoutError:
                logger.warning("Listening timed out while waiting for a command.")
            except sr.UnknownValueError:
                logger.warning("Could not understand the command.")
            except sr.RequestError as e:
                logger.error(f"Google API request failed: {e}")
        
        return None