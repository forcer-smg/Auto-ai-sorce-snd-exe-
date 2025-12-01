"""
Auto_Punch IDE - Server Configuration
Configured for Railway, cPanel, or Supabase deployment
"""
import os
from app import app, socketio

# Get port from environment variable (Railway, Heroku, etc.)
PORT = int(os.environ.get('PORT', 5001))
HOST = os.environ.get('HOST', '0.0.0.0')

# Get environment
ENV = os.environ.get('FLASK_ENV', 'production')

if __name__ == '__main__':
    print(f"Starting Auto_Punch IDE server on {HOST}:{PORT}")
    print(f"Environment: {ENV}")
    
    # Run with SocketIO support
    socketio.run(
        app,
        host=HOST,
        port=PORT,
        debug=(ENV == 'development'),
        allow_unsafe_werkzeug=True  # For production deployment
    )


