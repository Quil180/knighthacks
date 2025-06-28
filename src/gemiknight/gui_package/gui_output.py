# gemiknight/gui_package/gui_output.py

from flask import Flask, Response, render_template
# FIX: Removed 'gemiknight.' prefix
from vision_package.livestream import generate_video_stream
# FIX: Changed to a relative import '.' since it's in the same package
from .logger_setup import logger, log_stream

app = Flask(__name__)

latest_summary = "No summary yet."

@app.route('/')
def index():
    logger.debug("Serving index page.")
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    logger.debug("Starting video feed stream.")
    return Response(generate_video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/summary')
def show_summary():
    return f"<div style='background:#f4f4f4; padding:10px;'>{latest_summary}</div>"

if __name__ == '__main__':
    logger.info("webpage started")
    app.run(debug=True)