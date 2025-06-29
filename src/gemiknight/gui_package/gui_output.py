from flask import Flask, Response, render_template
from gemiknight.vision_package.livestream import generate_video_stream
from gemiknight.gui_package.logger_setup import logger, log_stream



app = Flask(__name__)

summary_history = []

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
    history_html = "<br><hr><br>".join(
        f"<div class='summary-block'>{s}</div>" for s in (summary_history)
    )
    return f"""
        <div id='summary-container' style='background:#f4f4f4; padding:10px; height:400px; overflow-y:auto;'>
            {history_html}
        </div>
    """
