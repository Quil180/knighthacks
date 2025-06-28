import logging
import time
from utils_package.logger import setup_logger
from settings import tts_rate, wake_word, switch_mode_command, interaction_prompt, pathfinding_prompt, camera_index, google_api_key, gemini_model_name
from vision_package.camera import Camera
from vision_package.gemini import GeminiAPI
from vision_package.response_parser import ResponseParser
from tts_package.speech import TTSEngine
from voice_package.voice_activation import VoiceActivation # corrected class name
from mode_package.mode_control import ModeController, OperatingMode

# initialize the centralized logger
logger = logging.getLogger(__name__)

def handle_voice_command(command: str, mode_controller: ModeController, tts: TTSEngine) -> bool:
    # processes a voice command to check for mode switching.
    if command and switch_mode_command in command:
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
    if not google_api_key:
        logger.critical("FATAL: GOOGLE_API_KEY is not configured.")
        return

    try:
        # initialization
        camera = Camera(camera_index=camera_index)
        gemini = GeminiAPI(api_key=google_api_key, model_name=gemini_model_name)
        tts = TTSEngine(rate=tts_rate)
        # correctttion here, using the correct VoiceActivation class
        voice_activator = VoiceActivation(wake_word=wake_word)
        mode_controller = ModeController(initial_mode=OperatingMode.INTERACTION)

        tts.speak(f"System ready. Current mode is {mode_controller.mode.name}.")

        # application loop
        while True:
            current_mode = mode_controller.mode
            print(f"\n[{current_mode.name} MODE] Say '{wake_word}' to issue a command.")

            # correcttion here, now were using the methods from the new VoiceActivation class
            if voice_activator.listen_for_wake_word():
                tts.speak("Yes?")
                command = voice_activator.listen_for_command()

                if command is not None:
                    is_mode_switched = handle_voice_command(command, mode_controller, tts)

                    if not is_mode_switched:
                        if current_mode == OperatingMode.INTERACTION:
                            perform_scene_analysis(camera, gemini, tts, interaction_prompt)
                        elif current_mode == OperatingMode.PATHFINDING:
                            perform_scene_analysis(camera, gemini, tts, pathfinding_prompt)
                else:
                    tts.speak("I didn't catch a command.")

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in the main loop: {e}", exc_info=True)
    finally:
        tts.speak("Shutting down.")
        print("Application shutting down.")

if __name__ == "__main__":
    main()
