import speech_recognition as sr
import time
import logging as log # for logging/debugging

DEBUG_VOICE     = 0 # Debug Prints?
adjust_time     = 0.5 # assumed to be per second
wake_word       = "hey gemini"
wake_word_delay = 1

logger = logging.getLogger(__name__)

def start_voice():
    # Listen for a wak word of choice and then respondssss
    
    # used for recognizing what is said
    r = sr.Recognizer()
    # is the actual microohone input that is used to recognize
    mic = sr.Microphone()

    log.info("Voice Activation is ready, waiting for wake word '" + wake_word + "'")

    while True:
        try:
            r.adjust_for_ambient_noise(mic, duration=adjust_time)
            audio = r.listen(mic)

            log.info("Recognizing Words.....")

            # Sending words to google to beg them to decipher it
            words = r.recognize_google(audio)
            
            # If the wake word is found in the text, say you found it
            if wake_word in words.lower():
                log.info("Wake Word found!!!!! 😊")
                time.sleep(wake_word_delay)

                # returning whole words list
                return words.partition(wake_word)

        except sr.UnknownValueError:
            log.error("Google could not understand audio, try again.")
        except sr.RequestError as err:
            log.error("Google request did not go through: {err}")
        except Exception as err:
            print("Some other error occured: {err}")
            break # critical failure occured

