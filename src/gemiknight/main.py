# gemiknight/main.py

import logging
import time
# FIX: The logger must be set up to see debug messages.
from gemiknight.utils_package.logger import setup_logger
from gemiknight.settings import tts_rate, wake_word, switch_mode_command, interaction_prompt, pathfinding_prompt, freeform_prompt, camera_index, google_api_key, gemini_model_name
from gemiknight.vision_package.camera import Camera
from gemiknight.vision_package.gemini import GeminiAPI
from gemiknight.vision_package.response_parser import ResponseParser
from gemiknight.tts_package.speech import TTSEngine
from gemiknight.voice_package.voice_activation import VoiceActivation
from gemiknight.mode_package.mode_control import ModeController, OperatingMode
from threading import Thread
from gemiknight.gui_package import gui_output

# FIX: Call the logger setup function.
setup_logger()
logger = logging.getLogger(__name__)

def handle_voice_command(command: str, mode_controller: ModeController, tts: TTSEngine) -> bool:
    # (This function is correct and requires no changes)
    if command == "Interaction":
        new_mode = mode_controller.switch_mode(1)
        tts.speak(f"Switched to {new_mode.name} mode.")
        return True
    if command == "Pathing":
        new_mode = mode_controller.switch_mode(2)
        tts.speak(f"Switched to {new_mode.name} mode.")
        return True
    if command == "Freeform":
        new_mode = mode_controller.switch_mode(3)
        tts.speak(f"Switched to {new_mode.name} mode.")
        return True
    return False

def perform_scene_analysis(camera: Camera, gemini: GeminiAPI, tts: TTSEngine, prompt: str):
    # (This function is correct and requires no changes)
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
    gui_output.latest_summary = summary
    tts.speak(summary)

def main():
    # (GUI setup and initialization are correct)
    def run_gui():
        gui_output.app.run(debug=True, use_reloader=False)
    Thread(target=run_gui, daemon=True).start()
    if not google_api_key:
        logger.critical("FATAL: GOOGLE_API_KEY is not configured.")
        return

    try:
        camera = Camera(camera_index=camera_index)
        gemini = GeminiAPI(api_key=google_api_key, model_name=gemini_model_name)
        tts = TTSEngine(rate=tts_rate)
        voice_activator = VoiceActivation(wake_word=wake_word)
        mode_controller = ModeController(initial_mode=OperatingMode.INTERACTION)
        tts.speak(f"System ready. Current mode is {mode_controller.mode.name}.")

        while True:
            current_mode = mode_controller.mode
            print(f"\n[{current_mode.name} MODE] Say '{wake_word}' to issue a command.")
            command = voice_activator.start_voice()

            if command is not None:
                is_mode_switched = handle_voice_command(command, mode_controller, tts)

                if not is_mode_switched:
                    # If it wasn't a mode switch, perform the default action
                    if current_mode == OperatingMode.INTERACTION:
                        perform_scene_analysis(camera, gemini, tts, interaction_prompt)
                    elif current_mode == OperatingMode.PATHFINDING:
                        perform_scene_analysis(camera, gemini, tts, pathfinding_prompt)
                    elif current_mode == OperatingMode.FREEFORM:
                        # FIX: Combine the user's command with the freeform prompt
                        # This tells the AI its role AND gives it the user's specific question.
                        if command: # Make sure the command isn't empty
                             full_prompt = f"{freeform_prompt} The user's question is: '{command}'"
                             perform_scene_analysis(camera, gemini, tts, full_prompt)
                        else:
                             tts.speak("Please ask a question after the wake word in freeform mode.")
            else:
                logger.info("No command was understood.")

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in the main loop: {e}", exc_info=True)
    finally:
        tts.speak("Shutting down.")
        print("Application shutting down.")

if __name__ == "__main__":
    main()