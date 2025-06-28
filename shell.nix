# shell.nix for setting up development environment for Nixos/Nix
let
  # We pin to a specific nixpkgs commit for reproducibility.
  # Last updated: 2024-04-29. Check for new commits at https://status.nixos.org.
  pkgs = import <nixpkgs> {};
in
  pkgs.mkShell {
    packages = [
      pkgs.uv
    ];
    shellHook = ''
      uv pip install -e .
    '';
  }
