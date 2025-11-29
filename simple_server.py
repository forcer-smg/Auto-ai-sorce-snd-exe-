"""Simple test server to verify Flask works"""
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Error loading template: {e}<br><br>Server is running on port 5001!"

@app.route('/test')
def test():
    return "Server is working!"

if __name__ == '__main__':
    print("\n" + "="*50)
    print("  Auto_Punch IDE - Simple Server")
    print("="*50)
    print("\nStarting server on http://localhost:5001")
    print("Open your browser and go to: http://localhost:5001")
    print("\nPress Ctrl+C to stop\n")
    
    try:
        app.run(host='0.0.0.0', port=5001, debug=True)
    except Exception as e:
        print(f"\nError starting server: {e}")
        input("\nPress Enter to exit...")

