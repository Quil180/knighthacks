# gemiknight/mode_package/mode_control.py

from enum import Enum, auto
import logging

logger = logging.getLogger(__name__)

class OperatingMode(Enum):
    # defines the three possible operating modes for the device.
    INTERACTION = auto()
    PATHFINDING = auto()
    FREEFORM = auto()

class ModeController:
    # manages the operational mode of the assistive device.

    def __init__(self, initial_mode: OperatingMode = OperatingMode.INTERACTION):
        # initializes the controller, defaulting to INTERACTION mode.
        self._current_mode = initial_mode
        logger.info(f"ModeController initialized in '{self._current_mode.name}' mode.")

    @property
    def mode(self) -> OperatingMode:
        # returns the current operating mode.
        return self._current_mode

    def switch_mode(self, mode_id: int):
        # sets the device to a new operating mode based on a numeric ID.
        if mode_id == 1:
            self._current_mode = OperatingMode.INTERACTION
        elif mode_id == 2:
            self._current_mode = OperatingMode.PATHFINDING
        elif mode_id == 3:
            self._current_mode = OperatingMode.FREEFORM
        else:
            logger.warning(f"Attempted to switch to an invalid mode ID: {mode_id}")
        
        logger.info(f"Switched to '{self._current_mode.name}' mode.")
        return self._current_mode