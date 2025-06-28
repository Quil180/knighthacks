# knighthacks

A Python-based assistive application for visually impaired users, leveraging Google's Gemini Vision AI, camera input, and text-to-speech. This project captures images from a camera, analyzes the scene (focusing on people and their expressions), and speaks a concise description aloud.

## Features

- **Live Scene Analysis:** Captures images from your camera and analyzes them using Google Gemini Vision AI.
- **Assistive Focus:** Describes only the people in view, their locations (left, center, right), and facial expressions (smiling, neutral, angry).
- **Real-time Feedback:** Converts scene descriptions to speech for live audio output.
- **Configurable and Modular:** Easy to adapt prompt, TTS settings, and camera source.

## Example Output

```
"Two people are in front of you. One is slightly to the left and smiling."
"One person is standing directly ahead. They appear neutral."
"Three people are visible. One on the left is smiling, the others look neutral."
```

## Getting Started

### Prerequisites

- Python 3.8+
- Camera (e.g., USB webcam)
- Google Gemini API key
- Nix (optional, for reproducible development environments)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Quil180/knighthacks.git
   cd knighthacks
   ```

2. **Set up environment (recommended):**
   - If you use [Nix](https://nixos.org/download.html):
     ```bash
     nix-shell
     ```

3. **Configure your API key:**
   - Edit the `.env` file in the project root:
     ```
     key=YOUR_GOOGLE_API_KEY
     ```

## Project Structure

```
src/gemiknight/
  main.py               # Main entry point
  settings.py           # Configuration (API keys, prompts, TTS rate)
  vision-package/
    vision/
      camera.py         # Camera capture logic
      gemini.py         # Gemini Vision API wrapper
  tts-package/
    speech.py           # Text-to-speech engine
  utils-package/
    logger.py           # Logger setup
  voice-package/
    voice-activation.py # Speech to Text Engine/Capture
```

## Development & Customization

- **Prompt Customization:** Edit `assistive_prompt` in `settings.py` to tailor what the AI describes.
- **TTS Settings:** Adjust `TTS_RATE` in `settings.py`.
- **Camera Index:** Change `camera_index` in `settings.py` if you have multiple cameras.

## Dependencies

- [OpenCV](https://opencv.org/) (camera access)
- [google-generativeai](https://pypi.org/project/google-generativeai/) (Gemini Vision API)
- [pyttsx3](https://pyttsx3.readthedocs.io/) (text-to-speech)
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) (speech-to-text)
- [Flask](https://flask.palletsprojects.com/) (Web GUI)

For full reproducibility, see the `shell.nix`.

## Acknowledgments

- Built for KnightHacks Gemiknights 2025, inspired by the need for real-time visual assistance.
```
