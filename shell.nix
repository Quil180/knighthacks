{ pkgs ? import <nixpkgs> {} }:

let
  # The idiomatic Nix way to define a Python environment is to use
  # python.withPackages. This ensures all dependencies are built correctly
  # by Nix before the shell is started.
  pythonEnv = pkgs.python3.withPackages (ps: with ps; [
    # List your Python dependencies here. Note that package names on Nix
    # are often lowercase and may differ slightly from PyPI.
    speechrecognition
    pyaudio
    google-generativeai
    pyttsx3
    flask
    python-dotenv
    opencv-python
    pillow
    uv # We can include uv here if you still want to use it manually
  ]);

in
pkgs.mkShell {
  # Use 'buildInputs' for dependencies needed to build and run your code.
  buildInputs = with pkgs; [
    pythonEnv

    python3
    portaudio
    pipewire
    espeak
    pkg-config
    uv
    
    glibc
  ];

  shellHook = ''
    echo "Nix environment is ready."
    echo "Python packages including pyaudio, flask, etc., are available."

    # The 'pip install -e .' command is for an "editable" install of your
    # local project. The Nix equivalent is to add the current directory
    # to the Python path.
    # export PYTHONPATH="$PWD:$PYTHONPATH"

    echo "Building the Repo..."
    uv venv
    source .venv/bin/activate
    # uv pip install speechrecognition pyaudio google-generativeai pyttsx3 flask dotenv opencv-python pillow
    uv run src/gemiknight/main.py
    rm -rf .venv
  '';
}
