import logging
import time
from utils_package.logger import setup_logger
from config import settings
from vision_package.vision.camera import Camera
from vision_package.vision.gemini_api import GeminiAPI
from vision_package.vision.response_parser import ResponseParser
from tts_package.speech import TTSEngine
from voice_package.voice_activation import VoiceActivation
from mode_package.mode_control import ModeController, OperatingMode

# Initialize the centralized logger
logger = logging.getLogger(__name__)

def handle_voice_command(command: str, mode_controller: ModeController, tts: TTSEngine) -> bool:
    
    # processes a voice command to check for mode switching.

    # command (str): the transcribed voice command.
    # mode_controller (ModeController): The controller for switching modes.
    # tts (TTSEngine): The text-to-speech engine for feedback.

    if command and settings.switch_mode_command in command:
        new_mode = mode_controller.switch_mode()
        tts.speak(f"Switched to {new_mode.name} mode.")
        return True
    return False

def perform_scene_analysis(camera: Camera, gemini: GeminiAPI, tts: TTSEngine, prompt: str):

    # single cycle of capturing, analyzing using a specific prompt, and speaking

    logger.info(f"Starting analysis with prompt: {prompt[:30]}...")

    if "pathfinding" in prompt.lower():
        tts.speak("Scanning path.")
    else:
        tts.speak("Looking closely.")

    image_bytes = camera.capture_jpeg_bytes()
    if not image_bytes:
        tts.speak("Error: Failed to capture image.")
        return

    description = gemini.analyze_image(prompt=prompt, image_bytes=image_bytes)
    summary = ResponseParser.summarize_text(description)
    print(f"\n--- AI Description ---\n{summary}\n----------------------\n")
    tts.speak(summary)

def main():

    # main function to run the complete vision assistance pipeline with mode control

    if not settings.google_api_key:
        logger.critical("FATAL: GOOGLE_API_KEY is not configured.")
        return

    try:
        # intialization
        camera = Camera(camera_index=settings.camera_index)
        gemini = GeminiAPI(api_key=settings.google_api_key, model_name=settings.gemini_model_name)
        tts = TTSEngine(rate=settings.tts_rate)
        voice_activator = VoiceActivation(wake_word=settings.wake_word)
        mode_controller = ModeController(initial_mode=OperatingMode.INTERACTION)

        tts.speak(f"System ready. Current mode is {mode_controller.mode.name}.")

        # application loop
        while True:
            current_mode = mode_controller.mode
            
            # listen for the wake word then process command
            # the mode determines the default action if it's not a mode-switch command
            print(f"\n[{current_mode.name} MODE] Say '{settings.wake_word}' to issue a command.")

            if voice_activator.listen_for_wake_word():
                tts.speak("Yes?")
                command = voice_activator.listen_for_command()

                # check for a mode switch command first
                is_mode_switched = handle_voice_command(command, mode_controller, tts)

                # if the mode was not switched, perform the default action for the current mode
                if not is_mode_switched:
                    if current_mode == OperatingMode.INTERACTION:
                        if command: # requires a specific command like "what do you see"
                            perform_scene_analysis(camera, gemini, tts, settings.interaction_prompt)
                        else:
                            tts.speak("I didn't catch a command.")
                    
                    elif current_mode == OperatingMode.PATHFINDING:
                        # in pathfinding, any command that isn't a mode switch triggers a scan
                        perform_scene_analysis(camera, gemini, tts, settings.pathfinding_prompt)

            # this is the "continuous" part of pathfinding, if no wake word, it will loop
            # to make it auto-scan, you'd add a non-blocking listener or threading
            # pathfinding is also triggered to ensure consistency for this logic

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in the main loop: {e}", exc_info=True)
    finally:
        tts.speak("Shutting down.")
        print("Application shutting down.")

if __name__ == "__main__":
    main()