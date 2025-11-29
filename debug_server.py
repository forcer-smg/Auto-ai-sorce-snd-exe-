"""Debug server with enhanced logging"""
import os
import sys
import logging
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Add Auto_Punch Ai to path
AUTO_PUNCH_DIR = Path(r"C:\Users\Administrator\Auto_Punch Ai")
sys.path.insert(0, str(AUTO_PUNCH_DIR))

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

# Log all requests
@app.before_request
def log_request_info():
    logger.info(f"→ {request.method} {request.path}")
    if request.is_json:
        logger.debug(f"  JSON data: {request.json}")

@app.after_request
def log_response_info(response):
    logger.info(f"← {response.status_code} {request.path}")
    return response

@app.route('/')
def index():
    """Main IDE interface"""
    logger.info("Serving main IDE page")
    try:
        template_path = os.path.join(app.template_folder, 'index.html')
        logger.debug(f"Template path: {template_path}")
        logger.debug(f"Template exists: {os.path.exists(template_path)}")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering template: {e}", exc_info=True)
        return f"Error: {e}", 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files with logging"""
    logger.debug(f"Serving static file: {filename}")
    try:
        return send_from_directory(app.static_folder, filename)
    except Exception as e:
        logger.error(f"Error serving static file {filename}: {e}")
        return f"File not found: {filename}", 404

@app.route('/test')
def test():
    """Test endpoint"""
    return jsonify({
        'status': 'ok',
        'static_folder': app.static_folder,
        'template_folder': app.template_folder,
        'static_exists': os.path.exists(app.static_folder),
        'template_exists': os.path.exists(app.template_folder)
    })

if __name__ == '__main__':
    port = 5001
    
    print("\n" + "="*70)
    print("  Auto_Punch IDE - DEBUG SERVER")
    print("="*70)
    print(f"\n✓ Port: {port}")
    print(f"✓ Static folder: {app.static_folder}")
    print(f"✓ Template folder: {app.template_folder}")
    print(f"✓ Static exists: {os.path.exists(app.static_folder)}")
    print(f"✓ Templates exist: {os.path.exists(app.template_folder)}")
    
    # Check key files
    key_files = [
        'static/css/ide.css',
        'static/js/ide.js',
        'templates/index.html'
    ]
    print(f"\n✓ Checking key files:")
    for f in key_files:
        exists = os.path.exists(f)
        status = "✓" if exists else "✗"
        print(f"  {status} {f}")
    
    print(f"\n{'='*70}")
    print(f"  Server starting on http://localhost:{port}")
    print(f"  Watch this window for detailed request logs")
    print(f"{'='*70}\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=False)

