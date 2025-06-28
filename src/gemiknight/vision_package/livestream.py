from camera import Camera

camera = Camera(0)

def generate_video_stream():
    while True:
        frame = camera.capture_jpeg_bytes()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
