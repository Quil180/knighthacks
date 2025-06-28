import speech_recognition as sr
import time
import logging as log # for logging/debugging

DEBUG_VOICE     = 0 # Debug Prints?
adjust_time     = 0.5 # assumed to be per second
wake_word       = "hey gemini"
wake_word_delay = 1

# renamed to avoid conflict with the 'log' module alias
logger = log.getLogger(__name__)

class VoiceRecognition:
    def start_voice(self):
        # Listen for a wak word of choice and then respondssss
        
        # used for recognizing what is said
        r = sr.Recognizer()
        # is the actual microohone input that is used to recognize
        mic = sr.Microphone()

        logger.info("Voice Activation is ready, waiting for wake word '" + wake_word + "'")

        while True:
            try:
                r.adjust_for_ambient_noise(mic, duration=adjust_time)
                audio = r.listen(mic)

                logger.info("Recognizing Words.....")

                # Sending words to google to beg them to decipher it
                words = r.recognize_google(audio)
                
                # If the wake word is found in the text, say you found it
                if wake_word in words.lower():
                    logger.info("Wake Word found!!!!! 😊")
                    time.sleep(wake_word_delay)

                    # returning the text AFTER the wake word
                    return words.partition(wake_word)[2].strip()

            except sr.UnknownValueError:
                logger.error("Google could not understand audio, try again.")
            except sr.RequestError as err:
                logger.error(f"Google request did not go through: {err}")
            except Exception as err:
                print(f"Some other error occured: {err}")
                break # critical failure occured

# how to use new class
if __name__ == '__main__':
    # create an instance of the class
    voice_processor = VoiceRecognition()

    # call the method to start listening
    command = voice_processor.start_voice()

    # print the result after the wake word is found
    if command:
        print(f"\nCommand Captured: '{command}'")