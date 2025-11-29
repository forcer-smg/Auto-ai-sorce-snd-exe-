"""Test server startup"""
import sys
from pathlib import Path

# Add Auto_Punch Ai to path
AUTO_PUNCH_DIR = Path(r"C:\Users\Administrator\Auto_Punch Ai")
sys.path.insert(0, str(AUTO_PUNCH_DIR))

print("Testing imports...")
try:
    from flask import Flask
    print("✓ Flask imported")
except Exception as e:
    print(f"✗ Flask error: {e}")
    sys.exit(1)

try:
    from flask_cors import CORS
    print("✓ Flask-CORS imported")
except Exception as e:
    print(f"✗ Flask-CORS error: {e}")
    sys.exit(1)

try:
    from flask_socketio import SocketIO
    print("✓ Flask-SocketIO imported")
except Exception as e:
    print(f"✗ Flask-SocketIO error: {e}")
    sys.exit(1)

print("\nTesting Auto_Punch Ai imports...")
try:
    from natural_language_automation import NaturalLanguageAutomation
    print("✓ NaturalLanguageAutomation imported")
except Exception as e:
    print(f"⚠ NaturalLanguageAutomation error: {e}")

try:
    from auto_punch_automation_integration import AutoPunchAutomation
    print("✓ AutoPunchAutomation imported")
except Exception as e:
    print(f"⚠ AutoPunchAutomation error: {e}")

print("\nCreating simple Flask app...")
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Auto_Punch IDE Test Server Running!"

print("Starting server on port 5001...")
print("Open http://localhost:5001 in your browser")
socketio.run(app, host='0.0.0.0', port=5001, debug=True)

