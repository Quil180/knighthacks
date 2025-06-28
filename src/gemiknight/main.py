import logging
import time
from datetime import datetime
# FIX: Re-enable the logger setup and call the function.
from gemiknight.utils_package.logger import setup_logger
from gemiknight.settings import tts_rate, wake_word, switch_mode_command, interaction_prompt, pathfinding_prompt, camera_index, google_api_key, gemini_model_name
from gemiknight.vision_package.camera import Camera
from gemiknight.vision_package.gemini import GeminiAPI
from gemiknight.vision_package.response_parser import ResponseParser
from gemiknight.tts_package.speech import TTSEngine
from gemiknight.voice_package.voice_activation import VoiceActivation
from gemiknight.mode_package.mode_control import ModeController, OperatingMode
from threading import Thread
from gemiknight.gui_package import gui_output

# actually call sthe setup_logger function to configure logging now lol
setup_logger()

# initialize the centralized logger
logger = logging.getLogger(__name__)

def print_gui(output: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {output}"
    gui_output.summary_history.append(output)
    # limit to last 50 summaries
    if len(gui_output.summary_history) > 50:
        gui_output.summary_history.pop(0)

def handle_voice_command(command: str, mode_controller: ModeController, tts: TTSEngine) -> bool:
    # processes a voice command to check for mode switching.
    # switch mode command
    if command == "Switch":
        new_mode = mode_controller.switch_mode()
        print_gui(f"Switched to {new_mode.name} mode.")
        tts.speak(f"Switched to {new_mode.name} mode.")
        return True
    return False

def perform_scene_analysis(camera: Camera, gemini: GeminiAPI, tts: TTSEngine, prompt: str):
    # single cycle of capturing, analyzing using a specific prompt, and speaking
    logger.info(f"Starting analysis with prompt: {prompt[:30]}...")

    if "pathfinding" in prompt.lower():
        print_gui("Scanning path.")
        tts.speak("Scanning path.")
    else:
        print_gui("Looking closely.")
        tts.speak("Looking closely.")

    image_bytes = camera.capture_jpeg_bytes()
    if not image_bytes:
        print_gui("Error: Failed to capture image.")
        tts.speak("Error: Failed to capture image.")
        return

    description = gemini.analyze_image(prompt=prompt, image_bytes=image_bytes)
    summary = ResponseParser.summarize_text(description)
    print(f"\n--- AI Description ---\n{summary}\n----------------------\n")
    # this line correctly updates the summary for the GUI
    print_gui(summary)
    tts.speak(summary)

def main():
    # main function to run the complete vision assistance pipeline with mode control
    def run_gui():
        # this will run the Flask app in a separate thread
        gui_output.app.run(debug=True, use_reloader=False)

    # starts GUI in a daemon thread so it closes when the main app closes
    Thread(target=run_gui, daemon=True).start()

    if not google_api_key:
        logger.critical("FATAL: GOOGLE_API_KEY is not configured.")
        return

    try:
        # initialization
        camera = Camera(camera_index=camera_index)
        gemini = GeminiAPI(api_key=google_api_key, model_name=gemini_model_name)
        tts = TTSEngine(rate=tts_rate)
        voice_activator = VoiceActivation(wake_word=wake_word)
        mode_controller = ModeController(initial_mode=OperatingMode.INTERACTION)

        print_gui(f"System ready. Current mode is {mode_controller.mode.name}.")
        tts.speak(f"System ready. Current mode is {mode_controller.mode.name}.")

        # application loop
        while True:
            current_mode = mode_controller.mode
            print(f"\n[{current_mode.name} MODE] Say '{wake_word}' to issue a command.")

            command = voice_activator.start_voice()

            if command is not None:
                is_mode_switched = handle_voice_command(command, mode_controller, tts)

                if not is_mode_switched:
                    if current_mode == OperatingMode.INTERACTION:
                        perform_scene_analysis(camera, gemini, tts, interaction_prompt)
                    elif current_mode == OperatingMode.PATHFINDING:
                        perform_scene_analysis(camera, gemini, tts, pathfinding_prompt)
            else:
                 # Tadding this for clarity haha
                 tts.speak("I didn't catch a command.")

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user.")
    except Exception as e:
        logger.critical(f"An unhandled error occurred in the main loop: {e}", exc_info=True)
    finally:
        print_gui("Shutting down")
        tts.speak("Shutting down.")
        print("Application shutting down.")

if __name__ == "__main__":
    main()