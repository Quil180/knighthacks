from flask import Flask, Response, render_template
from gemiknight.vision_package.livestream import generate_video_stream
from gemiknight.gui_package.logger_setup import logger, log_stream
import threading
import time


app = Flask(__name__)

@app.route('/')
def index():
    logger.debug("Serving index page.")
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    logger.debug("Starting video feed stream.")
    return Response(generate_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/logs')
def view_logs():
    log_stream.seek(0)  # Rewind
    log_contents = log_stream.read().replace('\n', '<br>')
    logger.debug("Log view requested.")
    return f"<div style='background:#f4f4f4; padding:10px;'>{log_contents}</div>"

def periodic_logger():
    while True:
        logger.info("Periodic log message from background thread.")
        time.sleep(5)

threading.Thread(target=periodic_logger, daemon=True).start()

if __name__ == '__main__':
    logger.info("webpage started")
    app.run(debug=True)
    mili = 0
    while(mili < 5):
        time.sleep(1)

