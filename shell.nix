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
    # 1. The full Python environment defined above.
    #    This provides python, pip, and all the libraries you listed.
    #    Crucially, it includes the development headers (like Python.h).
    pythonEnv

    # 2. System-level dependency for 'pyaudio'.
    #    pyaudio is a C-extension that wraps PortAudio.
    portaudio
    pipewire
    espeak

    # 3. Corrected typo for 'pkg-config'.
    #    This is a helper tool for build scripts to find libraries.
    pkg-config


  ];

  shellHook = ''
    echo "Nix environment is ready."
    echo "Python packages including pyaudio, flask, etc., are available."

    # The 'pip install -e .' command is for an "editable" install of your
    # local project. The Nix equivalent is to add the current directory
    # to the Python path.
    export PYTHONPATH="$PWD:$PYTHONPATH"

    echo "Building the Repo..."
    uv pip install -e .
    cd src/gemiknight
    python main.py
  '';
}
