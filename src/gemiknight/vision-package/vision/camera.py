import cv2
import logging
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)

class Camera:

    # Handles all camera operations using OpenCV.

    def __init__(self, camera_index: int):
        #Initializes the camera.

        # camera_index (int): The index of the camera device.

        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(self.camera_index)
        if not self.camera.isOpened():
            logger.error(f"Failed to open camera at index {camera_index}.")
            raise IOError(f"Cannot open camera at index {camera_index}.")
        logger.info(f"Camera at index {camera_index} initialized.")

    def capture_jpeg_bytes(self) -> bytes:

        # captures a single frame, converts it to RGB, and encodes it as JPEG bytes.
   
        # bytes: The JPEG-encoded image data, or None if capture fails.

        ret, frame = self.camera.read()
        if not ret:
            logger.error("Failed to capture frame from camera.")
            return None

        # OpenCV uses BGR format by default.. convert to RGB for standard Pillow/JPEG
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame_rgb)

        # encode the image to JPEG format in memory
        with BytesIO() as buffer:
            pil_image.save(buffer, format="JPEG")
            return buffer.getvalue()

    def release(self):
        # releases the camera source 
        if self.camera.isOpened():
            self.camera.release()
            logger.info("Camera released.")

    def __del__(self):
        # makes sure the camera is released when the object is destroyed
        self.release()