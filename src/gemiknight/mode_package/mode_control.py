# mode_package/mode_control.py

from enum import Enum, auto
import logging

logger = logging.getLogger(__name__)

class OperatingMode(Enum):

    # defines the specific operating modes for the device based on user context.
    # PATHFINDING: For navigation, providing continuous updates about surroundings.
    # INTERACTION: For identifying faces, text, and objects up close on command.

    PATHFINDING = auto()
    INTERACTION = auto()
    FREEFORM = auto()

class ModeController:

    # manages the operational mode of the assistive device.

    def __init__(self, initial_mode: OperatingMode = OperatingMode.INTERACTION):
        # initializes the controller, defaulting to INTERACTION mode.
        self._current_mode = initial_mode
        logger.info(f"ModeController initialized in '{self._current_mode.name}' mode.")

    @property
    def mode(self) -> OperatingMode:
        # Returns the current operating mode."""
        return self._current_mode

    def switch_mode(self, mode: int):
        # Toggles between the available modes."""
        if mode == 1:
            self._current_mode = OperatingMode.INTERACTION
        elif mode == 2:
            self._current_mode = OperatingMode.PATHFINDING
        elif mode == 3:
            self._current_mode = OperationMode.FREEFORM
        else:
            self._current_mode = self._current_mode
        
        logger.info(f"Switched to '{self._current_mode.name}' mode.")
        return self._current_mode
