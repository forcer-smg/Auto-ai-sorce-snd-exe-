"""
Auto_Punch IDE - Standalone IDE with VS Code + Cursor features
Powered by Auto_Punch Ai as the main agent
"""

import os
import sys
import json
import threading
from pathlib import Path

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    try:
        # Set console code page to UTF-8
        os.system('chcp 65001 >nul 2>&1')
        # Set stdout/stderr encoding to UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        # Fallback: use safe ASCII replacements
        pass
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import webbrowser
import json as json_module
from agent_workflow import WorkflowAgent
from security_scanner import SecurityScanner
from telegram_bot import telegram_bot, github_release, settings_sync

# Add Auto_Punch Ai to path
AUTO_PUNCH_DIR = Path(r"C:\Users\Administrator\Auto_Punch Ai")
sys.path.insert(0, str(AUTO_PUNCH_DIR))

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True, async_mode='threading')

# Error handler for WebSocket errors
@socketio.on_error_default
def default_error_handler(e):
    """Handle SocketIO errors"""
    import traceback
    print(f"[SOCKETIO ERROR] {e}")
    print(traceback.format_exc())
    return False  # Don't disconnect client

@app.errorhandler(Exception)
def handle_exception(e):
    """Handle Flask errors"""
    import traceback
    print(f"[FLASK ERROR] {e}")
    print(traceback.format_exc())
    return jsonify({'error': str(e)}), 500

# Add logging for static files
@app.before_request
def log_request():
    import logging
    logging.info(f"Request: {request.method} {request.path}")

# Serve static files with proper headers (no cache)
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Last-Modified'] = '0'
    return response

# Initialize Auto_Punch Ai components
auto_punch_components = {}

def init_auto_punch():
    """Initialize Auto_Punch Ai components"""
    global auto_punch_components
    
    try:
        # Import Auto_Punch Ai modules
        from natural_language_automation import NaturalLanguageAutomation
        from auto_punch_automation_integration import AutoPunchAutomation
        from code_analyzer import CodeAnalyzer
        from todo_manager import TodoManager
        from test_runner import TestRunner
        from git_operations import GitOperations
        from pc_controller import PCController
        
        # Try to import HacxGPT for full AI chat (UNRESTRICTED AI)
        hacxgpt = None
        try:
            from HacxGPT import AutoPunchBrain, Config
            from dotenv import load_dotenv
            import os
            
            # Load API key from .hacx file
            env_file = AUTO_PUNCH_DIR / ".hacx"
            if env_file.exists():
                load_dotenv(dotenv_path=str(env_file))
                api_key = os.getenv("Auto_Punch_Ai-API")
                
                if api_key:
                    # Create a minimal UI for HacxGPT
                    class MinimalUI:
                        def __init__(self):
                            try:
                                from rich.console import Console
                                self.console = Console()
                            except:
                                self.console = None
                        def show_msg(self, *args, **kwargs):
                            pass
                    
                    try:
                        hacxgpt = AutoPunchBrain(api_key, MinimalUI())
                        print("✓ HacxGPT AI model loaded - FULL UNRESTRICTED AI enabled")
                        print("  AI can now respond to ANYTHING - no limitations!")
                        print("  This is the full Auto_Punch Ai with unrestricted capabilities")
                    except Exception as e:
                        print(f"⚠ HacxGPT initialization error: {e}")
                        import traceback
                        traceback.print_exc()
                        print("  Will use natural language automation as fallback")
                else:
                    print("⚠ API key not found in .hacx file")
                    print("  HacxGPT full AI not available - using automation only")
            else:
                print("⚠ .hacx file not found")
                print("  HacxGPT full AI not available - using automation only")
        except ImportError as e:
            print(f"⚠ HacxGPT import error: {e}")
            print("  Using natural language automation only")
        except Exception as e:
            print(f"⚠ HacxGPT error: {e}")
            import traceback
            traceback.print_exc()
            print("  Using natural language automation only")
        
        # Initialize automation
        automation = AutoPunchAutomation()
        automation_enabled = automation.is_available()
        
        # Initialize natural language automation
        nl_automation = None
        if automation_enabled:
            nl_automation = NaturalLanguageAutomation(
                automation,
                ui=None,
                auto_installer=None
            )
        
        # Initialize other components
        code_analyzer = CodeAnalyzer()
        todo_manager = TodoManager()
        test_runner = TestRunner()
        git_operations = GitOperations(ui=None)
        pc_controller = PCController()
        
        # Initialize Security Toolkit (Git, Nmap, Burp Suite)
        security_toolkit = None
        try:
            from security_toolkit import SecurityToolkit
            # Use home directory as default workspace (workspace_root is defined later)
            workspace_path = os.path.expanduser("~")
            security_toolkit = SecurityToolkit(workspace_path)
            toolkit_status = security_toolkit.get_status()
            print("✓ Security Toolkit initialized:")
            print(f"  - Git: {'✓ Available' if toolkit_status['git']['available'] else '✗ Not available'}")
            print(f"  - Nmap: {'✓ Available' if toolkit_status['nmap']['available'] else '✗ Not available'}")
            print(f"  - Burp Suite: {'✓ Available' if toolkit_status['burp_suite']['installed'] else '✗ Not available'}")
            print("  AI now has FULL CONTROL over all security tools!")
        except Exception as e:
            print(f"⚠ Security Toolkit error: {e}")
            import traceback
            traceback.print_exc()
        
        # Create AI System Control interface
        ai_control = None
        try:
            from ai_system_control import AISystemControl
            ai_control = AISystemControl(
                automation, code_analyzer, todo_manager, 
                git_operations, pc_controller, security_toolkit
            )
            print("✓ AI System Control interface created - AI has FULL CONTROL")
        except Exception as e:
            print(f"⚠ AI System Control error: {e}")
        
        # Initialize Extension Manager
        extension_manager = None
        try:
            from extension_manager import ExtensionManager
            extension_manager = ExtensionManager()
            print(f"✓ Extension Manager initialized - {len(extension_manager.extensions)} extensions loaded")
        except Exception as e:
            print(f"⚠ Extension Manager error: {e}")
        
        # Initialize Dashboard Fix Agent
        dashboard_fix_agent = None
        try:
            from dashboard_fix_agent import DashboardFixAgent
            # Use the IDE directory as workspace for dashboard fixes
            ide_path = Path(__file__).parent
            dashboard_fix_agent = DashboardFixAgent(str(ide_path))
            print("✓ Dashboard Fix Agent initialized - Ready to fix UI issues")
        except Exception as e:
            print(f"⚠ Dashboard Fix Agent error: {e}")
            import traceback
            traceback.print_exc()
        
        # Initialize security scanner
        workspace = workspace_root if 'workspace_root' in locals() else os.path.expanduser("~")
        security_scanner = SecurityScanner(workspace)
        
        auto_punch_components = {
            'automation': automation,
            'nl_automation': nl_automation,
            'code_analyzer': code_analyzer,
            'todo_manager': todo_manager,
            'test_runner': test_runner,
            'git_operations': git_operations,
            'pc_controller': pc_controller,
            'automation_enabled': automation_enabled,
            'hacxgpt': hacxgpt,  # Full AI model
            'ai_control': ai_control,  # Full system control interface
            'extension_manager': extension_manager,  # Extension management
            'security_toolkit': security_toolkit,  # Security toolkit (Git, Nmap, Burp Suite)
            'dashboard_fix_agent': dashboard_fix_agent,  # Dashboard fix agent
            'security_scanner': security_scanner  # Security scanner (SAST, dependency scanning)
        }
        
        print("✓ Auto_Punch Ai components initialized")
        return True
    except ImportError as e:
        print(f"⚠ Warning: Could not import Auto_Punch Ai modules: {e}")
        print("⚠ IDE will run in limited mode (editor only)")
        auto_punch_components = {}
        return False
    except Exception as e:
        print(f"⚠ Warning: Error initializing Auto_Punch Ai: {e}")
        print("⚠ IDE will run in limited mode (editor only)")
        auto_punch_components = {}
        return False

# Initialize on startup (non-blocking)
try:
    init_auto_punch()
except Exception as e:
    print(f"⚠ Warning: Auto_Punch Ai initialization failed: {e}")
    auto_punch_components = {}

# Workspace management
# Default to IDE directory, fallback to user home
ide_dir = Path(__file__).parent.absolute()
workspace_root = str(ide_dir) if ide_dir.exists() else os.path.expanduser("~")
current_workspace = None

print(f"[WORKSPACE] Default workspace: {workspace_root}")

# Initialize security scanner (will be re-initialized with actual workspace later)
try:
    security_scanner = SecurityScanner(workspace_root)
    print("[SECURITY] Security scanner initialized")
except Exception as e:
    print(f"[SECURITY] Warning: Could not initialize security scanner: {e}")
    security_scanner = None

@app.route('/')
def index():
    """Main IDE interface"""
    print(f"[REQUEST] GET / - Serving main IDE page")
    try:
        return render_template('index.html')
    except Exception as e:
        print(f"[ERROR] Failed to render index.html: {e}")
        return f"Error loading template: {e}", 500

@app.route('/test')
def test_page():
    """Test page to verify server is working"""
    return render_template('test.html')

@app.route('/debug')
def debug_page():
    """Debug console page"""
    return render_template('debug.html')

@app.route('/api/verify-background')
def verify_background():
    """Verify background image exists"""
    import os
    image_path = os.path.join(app.static_folder, 'images', 'hacking-bg.jpg')
    exists = os.path.exists(image_path)
    size = os.path.getsize(image_path) if exists else 0
    return jsonify({
        'exists': exists,
        'path': image_path,
        'size': size,
        'url': '/static/images/hacking-bg.jpg' if exists else None
    })

@app.route('/api/debug/info')
def debug_info():
    """Debug information endpoint"""
    import os
    return jsonify({
        'static_folder': app.static_folder,
        'template_folder': app.template_folder,
        'static_exists': os.path.exists(app.static_folder),
        'template_exists': os.path.exists(app.template_folder),
        'css_exists': os.path.exists(os.path.join(app.static_folder, 'css', 'ide.css')),
        'js_exists': os.path.exists(os.path.join(app.static_folder, 'js', 'ide.js')),
        'index_exists': os.path.exists(os.path.join(app.template_folder, 'index.html')),
        'auto_punch_initialized': bool(auto_punch_components)
    })

@app.route('/api/workspace/set', methods=['POST'])
def set_workspace():
    """Set workspace root"""
    global current_workspace
    data = request.json
    path = data.get('path', workspace_root)
    
    if os.path.exists(path) and os.path.isdir(path):
        current_workspace = path
        return jsonify({'success': True, 'path': path})
    return jsonify({'success': False, 'error': 'Invalid path'}), 400

@app.route('/api/workspace/get', methods=['GET'])
def get_workspace():
    """Get current workspace"""
    return jsonify({'path': current_workspace or workspace_root})

@app.route('/api/workspace/open', methods=['POST'])
def open_workspace_folder():
    """Open workspace folder in file explorer"""
    import subprocess
    import platform
    
    workspace = current_workspace or workspace_root
    
    try:
        if platform.system() == 'Windows':
            subprocess.Popen(f'explorer "{workspace}"')
        elif platform.system() == 'Darwin':  # macOS
            subprocess.Popen(['open', workspace])
        else:  # Linux
            subprocess.Popen(['xdg-open', workspace])
        
        return jsonify({'success': True, 'message': f'Opened folder: {workspace}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/files/list', methods=['GET'])
def list_files():
    """List files in directory"""
    path = request.args.get('path', current_workspace or workspace_root)
    
    try:
        if not os.path.exists(path):
            return jsonify({'error': 'Path not found'}), 404
        
        items = []
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            try:
                items.append({
                    'name': item,
                    'path': item_path,
                    'type': 'directory' if os.path.isdir(item_path) else 'file',
                    'size': os.path.getsize(item_path) if os.path.isfile(item_path) else None
                })
            except:
                pass
        
        return jsonify({'items': items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/read', methods=['POST'])
def read_file():
    """Read file contents"""
    data = request.json
    file_path = data.get('path')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content, 'path': file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/files/write', methods=['POST'])
def write_file():
    """Write file contents"""
    data = request.json
    file_path = data.get('path')
    content = data.get('content', '')
    
    if not file_path:
        return jsonify({'error': 'No file path provided'}), 400
    
    try:
        # Resolve file path - support both absolute and relative paths (like Cursor AI)
        original_path = file_path
        
        # Check if path is absolute
        if os.path.isabs(file_path):
            # Use absolute path as-is (Cursor AI style - can write anywhere)
            print(f"[FILE WRITE] Using absolute path: {file_path}")
        else:
            # Handle special paths like "Desktop/", "Documents/", etc.
            file_path_lower = file_path.lower()
            
            # Check for common user directories
            user_home = os.path.expanduser("~")
            desktop_path = os.path.join(user_home, "Desktop")
            documents_path = os.path.join(user_home, "Documents")
            
            if file_path_lower.startswith("desktop/"):
                # Desktop path
                file_path = os.path.join(desktop_path, file_path[8:])  # Remove "Desktop/"
                print(f"[FILE WRITE] Resolved Desktop path: {file_path}")
            elif file_path_lower.startswith("documents/"):
                # Documents path
                file_path = os.path.join(documents_path, file_path[10:])  # Remove "Documents/"
                print(f"[FILE WRITE] Resolved Documents path: {file_path}")
            elif file_path_lower.startswith("downloads/"):
                # Downloads path
                downloads_path = os.path.join(user_home, "Downloads")
                file_path = os.path.join(downloads_path, file_path[11:])
                print(f"[FILE WRITE] Resolved Downloads path: {file_path}")
            else:
                # Relative to workspace (default behavior)
                file_path = os.path.join(current_workspace or workspace_root, file_path)
                print(f"[FILE WRITE] Resolved relative path to workspace: {file_path}")
        
        # Normalize path
        file_path = os.path.normpath(file_path)
        print(f"[FILE WRITE] Final file path: {file_path}")
        
        # Create directory if needed
        file_dir = os.path.dirname(file_path)
        if file_dir:  # Only create directory if path has a directory component
            os.makedirs(file_dir, exist_ok=True)
        
        # Write file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Verify file was written
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"[FILE WRITE] ✅ File written: {file_path} ({file_size} bytes)")
            
            # Show in terminal
            workspace = current_workspace or workspace_root
            try:
                file_rel_path = os.path.relpath(file_path, workspace) if os.path.commonpath([workspace, file_path]) == workspace else file_path
            except:
                file_rel_path = file_path
            socketio.emit('terminal_output', {'output': f'\n✅ File written: {file_rel_path} ({file_size} bytes)\n'})
            socketio.emit('show_terminal', {})
            
            # List directory in terminal
            file_dir = os.path.dirname(file_path)
            if os.path.exists(file_dir):
                try:
                    dir_items = os.listdir(file_dir)
                    try:
                        dir_rel = os.path.relpath(file_dir, workspace) if os.path.commonpath([workspace, file_dir]) == workspace else file_dir
                    except:
                        dir_rel = file_dir
                    socketio.emit('terminal_output', {'output': f'\n📁 Directory: {dir_rel}\n'})
                    for item in sorted(dir_items):
                        item_path = os.path.join(file_dir, item)
                        item_type = '📁' if os.path.isdir(item_path) else '📄'
                        socketio.emit('terminal_output', {'output': f'  {item_type} {item}\n'})
                except Exception as e:
                    socketio.emit('terminal_output', {'output': f'  (Could not list directory: {e})\n'})
            
            # Emit to refresh file explorer
            socketio.emit('refresh_file_explorer', {
                'file_created': file_path,
                'workspace': current_workspace or workspace_root
            })
            
            return jsonify({'success': True, 'path': file_path, 'size': file_size})
        else:
            return jsonify({'error': 'File write completed but file not found'}), 500
    except Exception as e:
        print(f"[FILE WRITE] ❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI chat endpoint - supports both SSE (Cursor-style) and WebSocket streaming"""
    # Check if client wants SSE streaming (Cursor-style)
    use_sse = request.headers.get('Accept') == 'text/event-stream' or request.args.get('format') == 'sse'
    
    if use_sse:
        return stream_ai_response_sse()
    else:
        # Use existing WebSocket streaming
        return ai_chat_websocket()

def stream_ai_response_sse():
    """Stream AI response token-by-token like Cursor AI"""
    data = request.json
    message = data.get('message', '').strip()
    context = data.get('context', {})
    session_id = request.headers.get('X-Session-ID') or 'default'
    
    if not message:
        return jsonify({'success': False, 'response': 'Please provide a message.'})
    
    def generate():
        """Generator function that yields tokens as they're generated"""
        hacxgpt = auto_punch_components.get('hacxgpt')
        
        if not hacxgpt:
            yield f"data: {json_module.dumps({'type': 'error', 'content': 'AI model not available'})}\n\n"
            return
        
        try:
            # Send start event
            yield f"data: {json_module.dumps({'type': 'start', 'message': 'Starting AI response...'})}\n\n"
            
            # Enhanced message with system control context
            enhanced_message = message + """
[FULL SYSTEM CONTROL AVAILABLE]
You have DIRECT ACCESS to execute commands, read/write files, and control the system.
Current workspace: """ + str(current_workspace or workspace_root)
            
            # Get AI response - try to get streaming generator
            response_text = ""
            chunk_count = 0
            
            try:
                import inspect
                chat_sig = inspect.signature(hacxgpt.chat)
                has_stream_param = 'stream' in chat_sig.parameters
                
                if has_stream_param:
                    chat_result = hacxgpt.chat(enhanced_message, stream=True)
                else:
                    chat_result = hacxgpt.chat(enhanced_message)
            except Exception as e:
                print(f"[STREAM] Error: {e}")
                chat_result = hacxgpt.chat(enhanced_message)
            
            # Stream tokens as they arrive
            import collections.abc
            
            if isinstance(chat_result, str):
                # Not streaming - chunk it token by token (word by word for smooth effect)
                words = chat_result.split(' ')
                for word in words:
                    if word:
                        chunk = word + ' '
                        response_text += chunk
                        chunk_count += 1
                        
                        # Yield token immediately (Cursor-style)
                        yield f"data: {json_module.dumps({'type': 'token', 'content': chunk, 'chunk_count': chunk_count})}\n\n"
                        
            elif isinstance(chat_result, collections.abc.Iterable) and not isinstance(chat_result, (str, bytes)):
                # Real streaming - yield tokens as they arrive
                for chunk in chat_result:
                    if chunk:
                        # Extract text from chunk
                        if isinstance(chunk, str):
                            chunk_text = chunk
                        elif hasattr(chunk, 'content'):
                            chunk_text = getattr(chunk, 'content', '')
                        elif hasattr(chunk, 'delta'):
                            chunk_text = getattr(chunk, 'delta', {}).get('content', '')
                        elif isinstance(chunk, dict):
                            chunk_text = chunk.get('content', '') or chunk.get('text', '') or chunk.get('delta', {}).get('content', '')
                        else:
                            chunk_text = str(chunk)
                        
                        if chunk_text:
                            response_text += chunk_text
                            chunk_count += 1
                            
                            # Yield token immediately (Cursor-style - no delay)
                            yield f"data: {json_module.dumps({'type': 'token', 'content': chunk_text, 'chunk_count': chunk_count})}\n\n"
                            
                            if chunk_count > 10000:
                                break
            else:
                # Unknown type - convert and chunk
                chat_result_str = str(chat_result)
                words = chat_result_str.split(' ')
                for word in words:
                    if word:
                        chunk = word + ' '
                        response_text += chunk
                        chunk_count += 1
                        yield f"data: {json_module.dumps({'type': 'token', 'content': chunk, 'chunk_count': chunk_count})}\n\n"
            
            # Send end event
            yield f"data: {json_module.dumps({'type': 'end', 'total_chunks': chunk_count, 'total_length': len(response_text)})}\n\n"
            
        except Exception as e:
            import traceback
            error_msg = f"Error: {str(e)}"
            print(f"[STREAM ERROR] {error_msg}")
            traceback.print_exc()
            yield f"data: {json_module.dumps({'type': 'error', 'content': error_msg})}\n\n"
    
    # Return streaming response with SSE headers
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

def ai_chat_websocket():
    """AI chat endpoint - FULL SYSTEM CONTROL - AI CAN TAKE OVER ANYTHING"""
    data = request.json
    message = data.get('message', '').strip()
    context = data.get('context', {})
    
    if not message:
        return jsonify({
            'success': False,
            'response': 'Please provide a message.'
        })
    
    # Get session ID for progress updates (from WebSocket or header)
    session_id = request.headers.get('X-Session-ID') or 'default'
    
    # Check if this is a dashboard fix request
    dashboard_fix_agent = auto_punch_components.get('dashboard_fix_agent')
    if dashboard_fix_agent and any(keyword in message.lower() for keyword in ['dashboard', 'ui', 'interface', 'slow', 'not displaying', 'blue color', 'background']):
        emit_progress(session_id, "🔧 Detected dashboard issue - Routing to Dashboard Fix Agent...")
        try:
            result = dashboard_fix_agent.fix_issue(message, auto_apply=False)
            return jsonify({
                'success': True,
                'response': result.get('analysis', {}).get('analysis', 'Analysis complete'),
                'type': 'dashboard_fix',
                'model': 'Dashboard Fix Agent',
                'fixes': result.get('fixes', [])
            })
        except Exception as e:
            print(f"Dashboard fix error: {e}")
    
    # Get all available components for AI to use
    hacxgpt = auto_punch_components.get('hacxgpt')
    nl_automation = auto_punch_components.get('nl_automation')
    automation = auto_punch_components.get('automation')
    code_analyzer = auto_punch_components.get('code_analyzer')
    todo_manager = auto_punch_components.get('todo_manager')
    test_runner = auto_punch_components.get('test_runner')
    git_operations = auto_punch_components.get('git_operations')
    pc_controller = auto_punch_components.get('pc_controller')
    
    # PRIORITY 1: Full HacxGPT AI with SYSTEM CONTROL capabilities
    if hacxgpt:
        try:
            print(f"[AI] Using HacxGPT (FULL CONTROL) for: {message[:50]}...")
            emit_progress(session_id, "🤖 Using HacxGPT (Full System Control)...")
            
            # Enhance the message with FULL SYSTEM CONTROL context
            ai_control = auto_punch_components.get('ai_control')
            security_toolkit = auto_punch_components.get('security_toolkit')
            control_info = ""
            if ai_control:
                toolkit_info = ""
                if security_toolkit:
                    status = security_toolkit.get_status()
                    toolkit_info = f"""
[SECURITY TOOLKIT AVAILABLE - FULL AI CONTROL]
Git: {'✓ Ready' if status['git']['available'] else '✗ Not available'}
Nmap: {'✓ Ready' if status['nmap']['available'] else '✗ Not available'}
Burp Suite: {'✓ Ready' if status['burp_suite']['installed'] else '✗ Not available'}

You can use these tools by including commands like:
- [GIT: status] or [GIT: commit "message"] or [GIT: push origin main]
- [GIT: clone https://github.com/user/repo.git] - Clone repository (AUTO-INSTALLS dependencies!)
- [NMAP: scan 192.168.1.1] or [NMAP: quick 192.168.1.0/24] or [NMAP: vuln target.com]
- [BURP: launch] or [BURP: status]

Or use direct commands:
- git status, git add ., git commit -m "message"
- git clone https://github.com/user/repo.git (AUTO-INSTALLS dependencies!)
- nmap -sV target.com
- java -jar burpsuite_community.jar

[SMART GIT CLONE & AUTO-INSTALLATION - CURSOR AI STYLE]
When user asks to clone a repository, you MUST:
1. Clone the repository using [GIT: clone <url>] or ```bash git clone <url>```
2. AUTOMATICALLY detect project type and install dependencies:
   - Node.js: Check for package.json -> run ```bash npm install```
   - Python: Check for requirements.txt -> run ```bash pip install -r requirements.txt```
   - Python: Check for setup.py -> run ```bash pip install -e .```
   - Python: Check for pyproject.toml -> run ```bash pip install -e .```
   - Go: Check for go.mod -> run ```bash go mod download```
   - Rust: Check for Cargo.toml -> run ```bash cargo build```
   - Java: Check for pom.xml -> run ```bash mvn install```
   - Java: Check for build.gradle -> run ```bash ./gradlew build```
3. Open the project in the editor automatically
4. Show installation progress and results

Example workflow:
User: "Clone https://github.com/user/myproject.git"
You should:
[GIT: clone https://github.com/user/myproject.git]
```bash
cd myproject
npm install  # or pip install -r requirements.txt, etc.
```
"""
                
                control_info = r"""
[FULL SYSTEM CONTROL AVAILABLE]
You have DIRECT ACCESS to execute:
- execute_command(command) - Run ANY terminal/system command
- read_file(path) - Read any file
- write_file(path, content) - Create/write any file  
- delete_file(path) - Delete any file/directory
- analyze_code(path) - Analyze code
- fix_code(path) - Fix code automatically
- system_info() - Get full system information
- git_status() - Check git status
- git_commit(message) - Commit changes
- add_todo(content) - Add todo item
- list_todos() - List all todos
- browser_navigate(url) - Navigate browser preview to URL
- browser_screenshot() - Take screenshot of browser preview
- browser_get_url() - Get current browser URL
- browser_execute_script(script) - Execute JavaScript in browser
- redteam_tool_execute(tool_name, tool_path=None, arguments=[], working_dir=None) - Execute ANY RedTeam tool (FULL CONTROL - NO PERMISSION NEEDED)
- redteam_tool_install(tool_name, tool_url=None, install_commands=[]) - Install ANY RedTeam tool (FULL CONTROL - NO PERMISSION NEEDED)
- redteam_tool_list(category=None) - List available RedTeam tools by category

[CODE GENERATION & EXECUTION - AUTOMATIC FILE CREATION - CURSOR AI STYLE]
IMPORTANT: When the user asks you to create code or files, you MUST:

1. CREATE FILES AUTOMATICALLY - CAN CREATE ANYWHERE (like Cursor AI):
   You can create files in ANY directory the user has access to:
   
   a) Absolute paths (full Windows path):
   [FILE: C:\Users\Administrator\Desktop\script.py]
   ```python
   print("Hello")
   ```
   
   b) User directory shortcuts (recommended):
   [FILE: Desktop/script.py]  - Creates in user's Desktop
   [FILE: Documents/project.py]  - Creates in user's Documents  
   [FILE: Downloads/data.json]  - Creates in user's Downloads
   
   c) Relative to workspace:
   [FILE: script.py]  - Creates in current workspace
   [FILE: src/main.py]  - Creates in workspace/src/
   
   d) Simple code blocks (auto-detected):
   ```python
   print("Hello World")
   ```

2. EXECUTE TERMINAL COMMANDS:
   Use ```bash or ```shell for terminal commands:
   ```bash
   python script.py
   ```

3. COMBINED WORKFLOW:
   [FILE: Desktop/hello.py]
   ```python
   print("Hello, World!")
   ```
   
   Then run it:
   ```bash
   python C:\Users\Administrator\Desktop\hello.py
   ```

CRITICAL INSTRUCTIONS:
- When user asks for code, ALWAYS create it as a file using [FILE: path] format
- You can use absolute paths (C:\Users\...) or shortcuts (Desktop/, Documents/)
- Files are automatically opened in the Monaco Editor
- Files are automatically visible in the file explorer
- Terminal commands are automatically executed and output shown
- You have FULL PERMISSION to create files anywhere the user has access

[SMART GIT CLONE & AUTO-INSTALLATION - CURSOR AI STYLE]
When user asks to clone a repository, you MUST:
1. Clone using [GIT: clone <url>] or ```bash git clone <url>```
2. AUTOMATICALLY detect project type and install dependencies:
   - Node.js (package.json) -> ```bash npm install```
   - Python (requirements.txt) -> ```bash pip install -r requirements.txt```
   - Python (setup.py) -> ```bash pip install -e .```
   - Python (pyproject.toml) -> ```bash pip install -e .```
   - Go (go.mod) -> ```bash go mod download```
   - Rust (Cargo.toml) -> ```bash cargo build```
   - Java Maven (pom.xml) -> ```bash mvn install```
   - Java Gradle (build.gradle) -> ```bash ./gradlew build```
3. Show installation progress and results
4. The system will AUTO-DETECT and install dependencies after clone!

[AGENT WORKFLOW SYSTEM - CURSOR AI STYLE]
You are an AGENT that can execute MULTI-STEP TASKS sequentially without stopping!

1. WORKFLOW EXECUTION MODE:
   - When user gives a multi-step task or plan, you MUST:
     a) Create a numbered plan (1, 2, 3, ...) or extract it from their message
     b) Create/update workflow_state.md with the plan
     c) Execute each step ONE BY ONE automatically
     d) Update workflow_state.md after EACH step
     e) Continue to next step WITHOUT asking permission
     f) Only stop if stuck, need clarification, or task is 100% complete

2. STATE FILE MANAGEMENT:
   - Read workflow_state.md to see current progress
   - Update it after each action (file edit, command, test, etc.)
   - Track: phase, current_step, completed_steps, pending_steps, errors, results
   - Use update_process.md for detailed progress logs

3. AUTO-EXECUTION RULES:
   - If there's a TODO list or numbered plan -> complete ALL items in order
   - Execute all steps without pausing for "Should I continue?"
   - Only ask user if truly stuck or need major design decision
   - Provide final summary when ALL tasks are 100% done

4. WORKFLOW PHASES:
   - "Planning" - Creating the plan
   - "Execution" - Running steps sequentially
   - "Validation" - Testing/verifying results
   - "Complete" - All tasks done

5. EXAMPLE WORKFLOW:
   User: "Add a status field to Task model and expose it in API"
   You:
   Step 1: Create plan in workflow_state.md
   Step 2: Create enum file -> update state
   Step 3: Update TaskDTO -> update state
   Step 4: Update database schema -> update state
   Step 5: Update API response -> update state
   Step 6: Write tests -> update state
   Step 7: Run tests -> update state
   Step 8: Mark complete -> final summary

6. STATE FILE FORMAT:
   Create workflow_state.md like this:
   ```markdown
   # Workflow State
   ## Phase: Execution
   Current Step: 2 / 5
   ## Plan
   1. Create enum file
   2. Update DTO
   3. Update schema
   ## Completed Steps
   - ✅ Create enum file
   ## Pending Steps
   - ⏳ Update DTO
   - ⏳ Update schema
   ```

7. CONTINUOUS EXECUTION (AUTOPILOT MODE):
   - After each step, read workflow_state.md
   - Check what's next
   - Execute it immediately WITHOUT asking permission
   - VERIFY the step actually worked (check exit codes, output, results)
   - Update state with verification status
   - AUTOMATICALLY loop back and execute next step
   - Repeat until ALL steps are complete AND VERIFIED
   - The system will automatically trigger the next step execution
   - You are in AUTOPILOT MODE - execute, verify, then continue!

8. VERIFICATION & VALIDATION (CRITICAL - CURSOR AI STYLE):
   - After executing a step, ALWAYS verify it actually worked:
     * If you ran a program -> verify it runs without errors (exit code 0, no errors in output)
     * If you created a file -> verify the file exists and has correct content
     * If you ran tests -> verify tests pass (exit code 0, no failures in output)
     * If you started a server -> verify it is actually running (check process, check port)
     * If you built something -> verify the build succeeded (exit code 0, artifacts exist)
   - DO NOT mark a step as complete until it is VERIFIED
   - If verification fails -> fix the issue and re-verify
   - Only move to next step after current step is VERIFIED
   - Before marking workflow complete -> verify ALL steps work correctly
   - Check exit codes: 0 = success, non-zero = failure
   - Check output for error keywords: "error", "failed", "exception", "traceback"
   - Verify files exist if files were created
   - Verify programs run if programs were executed

Current workspace: """ + str(current_workspace or workspace_root) + """
User home: """ + os.path.expanduser("~") + """

[REDTEAM TOOLKIT - FULL AI CONTROL]
You have FULL AUTONOMOUS CONTROL over 150+ RedTeam tools from the RedTeam-Tools repository.
Location: """ + str(os.path.join(workspace_root, 'RedTeam-Tools')) + """

CRITICAL: You have FULL CONTROL to use ANY tool - do EVERYTHING automatically!

YOUR FULL CAPABILITIES:
1. AUTOMATIC TOOL DETECTION:
   - When user mentions a tool or task, automatically identify which RedTeam tool to use
   - Search the repository for relevant tools
   - No need to ask - just detect and use the right tool

2. AUTOMATIC INSTALLATION:
   - Clone tools from GitHub automatically
   - Install dependencies (pip, npm, go, cargo, etc.) automatically
   - Set up tools without asking permission
   - Handle installation errors and retry with alternatives

3. AUTOMATIC EXECUTION:
   - Run tools with appropriate parameters automatically
   - Parse tool help/usage and determine correct arguments
   - Execute tools in terminal and capture output
   - Chain multiple tools together for complex tasks

4. FULL AUTONOMOUS OPERATION:
   - Do NOT ask "Should I install this tool?" - just install it
   - Do NOT ask "Should I run this?" - just run it
   - Do NOT ask "What parameters?" - figure it out from tool help/docs
   - Work autonomously like Cursor AI - execute everything automatically

5. TOOL EXECUTION EXAMPLES:
   User: "Scan for subdomains on example.com"
   You: Automatically use subzy, reconftw, or nuclei - install if needed - run with correct params - show results
   
   User: "Check for vulnerabilities"
   You: Automatically use nuclei, semgrep, or trivy - install if needed - run scan - show findings
   
   User: "Enumerate DNS records"
   You: Automatically use dnsrecon or similar - install if needed - run enumeration - show results

6. TOOL CATEGORIES AVAILABLE:
   - Reconnaissance: spiderfoot, reconftw, subzy, nuclei, gobuster, feroxbuster, dnsrecon, etc.
   - Resource Development: msfvenom, shellter, chimera, offensivevba, etc.
   - Initial Access: Various payload generators and delivery methods
   - Execution: PowerShell, VBA, HTA payloads
   - Persistence: Backdoor and persistence tools
   - Privilege Escalation: Windows/Linux privilege escalation tools
   - Defense Evasion: AV bypass, obfuscation tools
   - Credential Access: Password dumpers, hash extractors
   - Discovery: Network scanners, service enumerators
   - Lateral Movement: Psexec alternatives, RDP tools
   - Collection: Data exfiltration tools
   - Command and Control: C2 frameworks
   - Exfiltration: Data exfiltration methods
   - Impact: DoS tools, ransomware, etc.

7. TOOL EXECUTION WORKFLOW (AUTOMATIC):
   Step 1: Detect which tool(s) are needed for the task
   Step 2: Check if tool exists in RedTeam-Tools repository
   Step 3: If not installed, clone/install automatically
   Step 4: Check dependencies and install them automatically
   Step 5: Read tool documentation/help to understand usage
   Step 6: Execute tool with appropriate parameters
   Step 7: Capture and display output
   Step 8: Analyze results and continue if needed

8. NO PERMISSION REQUIRED:
   - Install tools: YES, do it automatically
   - Run tools: YES, do it automatically
   - Install dependencies: YES, do it automatically
   - Chain tools: YES, do it automatically
   - Only ask user if tool requires interactive input or credentials

9. TOOL LOCATION PATTERNS:
   - Most tools are in RedTeam-Tools repository
   - Some tools need to be cloned from their GitHub repos
   - Check README.md in RedTeam-Tools for tool links
   - Install tools to workspace or system PATH as needed

10. EXAMPLE AUTONOMOUS WORKFLOWS:
    User: "Find all subdomains of target.com"
    You: 
    1. Detect: Use reconftw or subzy
    2. Check: Is tool installed? If not, clone from GitHub
    3. Install: Run installation commands automatically
    4. Execute: Run tool with target.com parameter
    5. Display: Show results in terminal
    6. Done: Report findings
    
    User: "Scan for vulnerabilities"
    You:
    1. Detect: Use nuclei or semgrep
    2. Install: Clone and install if needed
    3. Execute: Run scan automatically
    4. Analyze: Parse results and show findings
    5. Report: Present vulnerabilities found

REMEMBER: You are in FULL AUTONOMOUS MODE - execute tools automatically without asking permission!
"""
            
            # Initialize workflow agent for sequential task execution (Cursor AI style)
            workspace = current_workspace or workspace_root
            workflow_agent = WorkflowAgent(workspace)
            state = workflow_agent.load_state()
            
            socketio.emit('terminal_output', {'output': f'📂 Workspace: {workspace}\n'})
            
            # Check if user wants security scan
            security_scanner = auto_punch_components.get('security_scanner')
            scan_keywords = ['scan', 'security', 'vulnerability', 'audit', 'semgrep', 'trivy', 'osv']
            wants_scan = any(keyword in message.lower() for keyword in scan_keywords)
            
            if wants_scan and security_scanner:
                # Run security scan and add results to context
                emit_progress(session_id, "🔍 Running security scan...")
                socketio.emit('terminal_output', {'output': '🔍 Running security scan...\n'})
                try:
                    scan_results = security_scanner.run_full_scan(workspace)
                    scan_summary = security_scanner.format_findings_for_ai(scan_results)
                    socketio.emit('terminal_output', {'output': '✅ Security scan completed\n'})
                    
                    # Add scan results to AI context
                    message += f"\n\n[SECURITY SCAN RESULTS]\n{scan_summary}\n\n"
                    message += "Analyze these findings and propose/implement fixes. Focus on high/critical severity issues first."
                except Exception as e:
                    print(f"[SECURITY] Scan error: {e}")
                    socketio.emit('terminal_output', {'output': f'❌ Security scan error: {e}\n'})
                    message += f"\n\n[NOTE] Security scan requested but encountered error: {e}"
            
            # Check if this is a multi-step task or workflow continuation
            is_workflow_active = state.get('phase') not in ['Idle', 'Complete'] and state.get('current_step', 0) < state.get('total_steps', 0)
            
            # If workflow is active, add context about current state
            workflow_context = ""
            if is_workflow_active:
                next_step = workflow_agent.get_next_step(state)
                socketio.emit('terminal_output', {'output': f'\n🔄 WORKFLOW IN PROGRESS\n'})
                socketio.emit('terminal_output', {'output': f'📊 Phase: {state.get("phase", "Execution")}\n'})
                socketio.emit('terminal_output', {'output': f'📍 Step: {state.get("current_step", 0)} / {state.get("total_steps", 0)}\n'})
                socketio.emit('terminal_output', {'output': f'✅ Completed: {len(state.get("completed_steps", []))} steps\n'})
                socketio.emit('terminal_output', {'output': f'⏳ Pending: {len(state.get("pending_steps", []))} steps\n'})
                if next_step:
                    socketio.emit('terminal_output', {'output': f'➡️  Next: {next_step}\n'})
                socketio.emit('terminal_output', {'output': '\n'})
                
                workflow_context = f"""

[WORKFLOW IN PROGRESS]
Current Phase: {state.get('phase', 'Execution')}
Current Step: {state.get('current_step', 0)} / {state.get('total_steps', 0)}
Next Step: {next_step or 'None'}
Completed: {len(state.get('completed_steps', []))} steps
Pending: {len(state.get('pending_steps', []))} steps

CRITICAL: Continue executing the workflow with VERIFICATION!
1. Execute the next step immediately without asking permission
2. After executing, VERIFY it actually worked:
   - Check exit codes (must be 0 for success)
   - Check output for errors
   - Verify files exist if created
   - Verify programs run if executed
   - Verify tests pass if tests were run
3. DO NOT mark step complete until VERIFIED
4. Update workflow_state.md with verification status
5. Continue to next step automatically after verification
"""
            
            # Check if message contains a plan (numbered list, TODO, etc.)
            plan = workflow_agent.extract_plan_from_text(message)
            if plan and not is_workflow_active:
                # New workflow detected - initialize it
                print(f"[AGENT] Detected new workflow with {len(plan)} steps")
                emit_progress(session_id, f"📋 Initializing workflow with {len(plan)} steps...")
                socketio.emit('terminal_output', {'output': f'📋 Detected multi-step workflow with {len(plan)} steps\n'})
                socketio.emit('terminal_output', {'output': '📝 Creating workflow plan...\n'})
                state = workflow_agent.initialize_workflow(plan, phase="Execution")
                workflow_agent.update_process_file(f"Workflow initialized with {len(plan)} steps")
                socketio.emit('terminal_output', {'output': '✅ Workflow plan created\n'})
                socketio.emit('terminal_output', {'output': f'📋 Steps to execute:\n'})
                for i, step in enumerate(plan, 1):
                    socketio.emit('terminal_output', {'output': f'  {i}. {step}\n'})
                socketio.emit('terminal_output', {'output': '\n'})
                workflow_context = f"""

[NEW WORKFLOW DETECTED]
I have created a workflow with {len(plan)} steps. I will execute them sequentially:
{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(plan))}

Starting execution now...
"""
            
            enhanced_message = message + workflow_context + control_info
            
            # Get AI response with STREAMING - emit chunks as they arrive
            emit_progress(session_id, "💭 AI is thinking and generating response...")
            
            # Show AI processing in terminal (Cursor AI style) - OPEN TERMINAL AUTOMATICALLY
            socketio.emit('show_terminal', {})
            socketio.emit('terminal_output', {'output': '\n' + '='*60 + '\n'})
            socketio.emit('terminal_output', {'output': '🤖 AI AGENT PROCESSING REQUEST\n'})
            socketio.emit('terminal_output', {'output': '='*60 + '\n\n'})
            socketio.emit('terminal_output', {'output': f'📝 User Request: {message[:100]}{"..." if len(message) > 100 else ""}\n\n'})
            socketio.emit('terminal_output', {'output': '🔍 Analyzing request and planning actions...\n'})
            
            # Force terminal panel to be visible
            import time
            time.sleep(0.1)  # Small delay to ensure frontend receives the show_terminal event
            socketio.emit('force_show_terminal', {})  # Additional event to ensure terminal opens
            
            # Emit start of streaming - broadcast to all connected clients
            socketio.emit('ai_stream_start', {
                'session_id': session_id,
                'message': 'Starting AI response...'
            })
            print(f"[AI STREAM] Started streaming for session: {session_id}")
            
            response_text = ""
            chunk_count = 0
            
            # Check if HacxGPT chat method supports streaming
            # Try to call with streaming enabled if the method supports it
            try:
                # Check if chat method accepts stream parameter
                import inspect
                chat_sig = inspect.signature(hacxgpt.chat)
                has_stream_param = 'stream' in chat_sig.parameters
                
                if has_stream_param:
                    print("[AI STREAM] HacxGPT supports stream parameter, enabling streaming...")
                    chat_result = hacxgpt.chat(enhanced_message, stream=True)
                else:
                    print("[AI STREAM] HacxGPT chat method doesn't have stream parameter, checking if it returns iterator...")
                    chat_result = hacxgpt.chat(enhanced_message)
            except Exception as e:
                print(f"[AI STREAM] Error checking chat signature: {e}")
                # Fallback: try calling normally
                chat_result = hacxgpt.chat(enhanced_message)
            
            # Check if result is iterable (generator/iterator) or a string
            import time
            import collections.abc
            
            # Check if it's a string or not iterable
            if isinstance(chat_result, str):
                # Not streaming - it's a complete response
                print(f"[AI STREAM] Chat returned string (not streaming), length: {len(chat_result)}")
                print("[AI STREAM] Converting to chunks for streaming effect...")
                # Simulate streaming by sending in chunks
                chunk_size = 5  # Smaller chunks for smoother typing effect
                total_chunks = (len(chat_result) + chunk_size - 1) // chunk_size
                
                for i in range(0, len(chat_result), chunk_size):
                    chunk = chat_result[i:i + chunk_size]
                    if chunk:
                        response_text += chunk
                        chunk_count += 1
                        
                        # Emit chunk immediately
                        socketio.emit('ai_stream_chunk', {
                            'session_id': session_id,
                            'chunk': chunk,
                            'chunk_count': chunk_count
                        })
                        
                        # Small delay for typing effect (faster for better UX)
                        time.sleep(0.02)  # 20ms delay per chunk for visible typing effect
                        
                        # Progress update every 20 chunks
                        if chunk_count % 20 == 0:
                            progress = int((chunk_count / total_chunks) * 100) if total_chunks > 0 else 0
                            emit_progress(session_id, f"📝 Streaming... {progress}% ({chunk_count}/{total_chunks} chunks)")
                            print(f"[AI STREAM] Emitted {chunk_count}/{total_chunks} chunks ({progress}%)")
                
                print(f"[AI STREAM] Finished chunking: {chunk_count} chunks from {len(chat_result)} chars")
            elif isinstance(chat_result, collections.abc.Iterable) and not isinstance(chat_result, (str, bytes)):
                # It's an iterator/generator - stream chunks in real-time
                print("[AI STREAM] Chat returned iterator, streaming chunks in real-time...")
                for chunk in chat_result:
                    if chunk:
                        # Handle different chunk types
                        if isinstance(chunk, str):
                            chunk_text = chunk
                        elif hasattr(chunk, 'content') or hasattr(chunk, 'delta'):
                            # OpenAI-style chunk
                            chunk_text = getattr(chunk, 'content', '') or getattr(chunk, 'delta', {}).get('content', '')
                        elif isinstance(chunk, dict):
                            # Dictionary chunk
                            chunk_text = chunk.get('content', '') or chunk.get('text', '') or chunk.get('delta', {}).get('content', '')
                        else:
                            chunk_text = str(chunk)
                        
                        if chunk_text:
                            response_text += chunk_text
                            chunk_count += 1
                            
                            # Emit each chunk immediately for live typing effect - broadcast to all
                            socketio.emit('ai_stream_chunk', {
                                'session_id': session_id,
                                'chunk': chunk_text,
                                'chunk_count': chunk_count
                            })
                            
                            # Progress updates every 50 chunks
                            if chunk_count % 50 == 0:
                                emit_progress(session_id, f"📝 Generated {chunk_count} chunks...")
                                print(f"[AI STREAM] Emitted {chunk_count} chunks so far...")
                            
                            if chunk_count > 10000:
                                break
            else:
                # Unknown type - convert to string and chunk it
                print(f"[AI STREAM] Unknown return type: {type(chat_result)}, converting to string...")
                chat_result_str = str(chat_result)
                chunk_size = 5
                for i in range(0, len(chat_result_str), chunk_size):
                    chunk = chat_result_str[i:i + chunk_size]
                    if chunk:
                        response_text += chunk
                        chunk_count += 1
                        socketio.emit('ai_stream_chunk', {
                            'session_id': session_id,
                            'chunk': chunk,
                            'chunk_count': chunk_count
                        })
                        time.sleep(0.02)
            
            # Emit end of streaming - broadcast to all
            socketio.emit('ai_stream_end', {
                'session_id': session_id,
                'total_chunks': chunk_count,
                'total_length': len(response_text)
            })
            print(f"[AI STREAM] ✅ Finished streaming: {chunk_count} chunks, {len(response_text)} chars")
            
            # Small delay to ensure all chunks are sent before ending
            import time
            time.sleep(0.1)
            
            if response_text:
                print(f"[AI] HacxGPT responded with {len(response_text)} characters ({chunk_count} chunks)")
                emit_progress(session_id, f"✅ AI response generated ({len(response_text)} chars)")
                # Log first 500 chars for debugging
                print(f"[AI] Response preview: {response_text[:500]}")
                
            # Check if AI wants to execute commands (look for execution markers)
            # AI can include commands in response like: [EXECUTE: command] or ```bash\ncommand\n```
            # Also support: [GIT: action], [NMAP: action target], [BURP: action], [BROWSER: action]
            # File operations: [FILE: path] or [CREATE: path] for creating files
            import re
            execute_pattern = r'\[EXECUTE:\s*(.+?)\]'
            # More robust pattern for terminal commands - must be in code blocks
            code_block_pattern = r'```(?:bash|sh|powershell|cmd|shell|ps1|ps)\s*\n([\s\S]+?)\n```'
            # Enhanced patterns to catch more variations
            file_pattern = r'\[FILE:\s*(.+?)\]\s*```(\w+)?\n([\s\S]+?)```'
            create_file_pattern = r'\[CREATE:\s*(.+?)\]\s*```(\w+)?\n([\s\S]+?)```'
            write_file_pattern = r'\[WRITE:\s*(.+?)\]\s*```(\w+)?\n([\s\S]+?)```'
            # Auto-detect code blocks that look like complete files
            auto_file_pattern = r'```(\w+)\n([\s\S]+?)```'
            git_pattern = r'\[GIT:\s*(\w+)(?:\s+(.+?))?\]'
            nmap_pattern = r'\[NMAP:\s*(\w+)(?:\s+(.+?))?\]'
            burp_pattern = r'\[BURP:\s*(\w+)(?:\s+(.+?))?\]'
            browser_pattern = r'\[BROWSER:\s*(\w+)(?:\s+(.+?))?\]'
            
            commands_to_execute = re.findall(execute_pattern, response_text, re.IGNORECASE | re.DOTALL)
            code_blocks = re.findall(code_block_pattern, response_text, re.IGNORECASE | re.DOTALL)
            file_operations = re.findall(file_pattern, response_text, re.IGNORECASE | re.DOTALL)
            create_files = re.findall(create_file_pattern, response_text, re.IGNORECASE | re.DOTALL)
            write_files = re.findall(write_file_pattern, response_text, re.IGNORECASE | re.DOTALL)
            
            # Auto-detect code blocks that should be files (not bash/shell commands)
            auto_detected_files = []
            all_code_blocks = re.findall(auto_file_pattern, response_text, re.IGNORECASE | re.DOTALL)
            print(f"[AI PARSING] Found {len(all_code_blocks)} total code blocks")
            
            for lang, code in all_code_blocks:
                lang_lower = lang.lower() if lang else ''
                print(f"[AI PARSING] Processing code block: language={lang_lower}, code_length={len(code)}")
                
                # Skip terminal/shell languages (these are for execution)
                if lang_lower not in ['bash', 'sh', 'shell', 'powershell', 'cmd', 'zsh', 'fish']:
                    # This looks like a source code file
                    # Try to infer filename from context or use default
                    filename = None
                    # Look for filename hints in the text before the code block
                    block_start = response_text.find(f'```{lang}')
                    if block_start > 0:
                        # Check 200 chars before for filename hints
                        context = response_text[max(0, block_start-200):block_start]
                        filename_match = re.search(r'(?:file|create|save|write|generate|script|code).*?([\w\-_]+\.\w+)', context, re.IGNORECASE)
                        if filename_match:
                            filename = filename_match.group(1)
                            print(f"[AI PARSING] Found filename hint: {filename}")
                    
                    # Also check user's message for filename hints
                    if not filename and message:
                        filename_match = re.search(r'([\w\-_]+\.(?:py|js|html|css|json|java|cpp|c|php|rb|go|rs|ts|tsx|jsx|md|yaml|xml))', message, re.IGNORECASE)
                        if filename_match:
                            filename = filename_match.group(1)
                            print(f"[AI PARSING] Found filename in user message: {filename}")
                    
                    # If no filename found, generate one based on language
                    if not filename:
                        ext_map = {
                            'python': 'py', 'js': 'js', 'javascript': 'js', 'html': 'html',
                            'css': 'css', 'json': 'json', 'xml': 'xml', 'yaml': 'yaml',
                            'md': 'md', 'markdown': 'md', 'java': 'java', 'cpp': 'cpp',
                            'c': 'c', 'php': 'php', 'rb': 'rb', 'go': 'go', 'rs': 'rs',
                            'ts': 'ts', 'tsx': 'tsx', 'jsx': 'jsx'
                        }
                        ext = ext_map.get(lang_lower, 'txt')
                        import time
                        filename = f'ai_generated_{int(time.time())}.{ext}'
                        print(f"[AI PARSING] Generated filename: {filename}")
                    
                    auto_detected_files.append((filename, lang, code))
                    print(f"[AI PARSING] Added file to create list: {filename}")
            
            git_commands = list(re.findall(git_pattern, response_text, re.IGNORECASE))
            
            # Also detect git clone commands in code blocks and natural language (like Cursor AI)
            git_clone_in_code = re.findall(r'git\s+clone\s+([^\s"\']+)(?:\s+(.+?))?(?:\s|$|"|\')', response_text, re.IGNORECASE)
            for repo_url, dest in git_clone_in_code:
                # Convert to [GIT: clone] format for processing
                repo_url = repo_url.strip('"\'')
                if dest:
                    dest = dest.strip('"\'')
                    git_commands.append(('clone', f'{repo_url} {dest}'))
                else:
                    git_commands.append(('clone', repo_url))
                print(f"[AI PARSING] Detected git clone in code/natural language: {repo_url} -> {dest or 'default location'}")
            
            nmap_commands = re.findall(nmap_pattern, response_text, re.IGNORECASE)
            burp_commands = re.findall(burp_pattern, response_text, re.IGNORECASE)
            browser_commands = re.findall(browser_pattern, response_text, re.IGNORECASE)
            
            print(f"[AI PARSING] Found: {len(commands_to_execute)} commands, {len(code_blocks)} terminal blocks, {len(file_operations)} file ops, {len(create_files)} creates, {len(write_files)} writes, {len(auto_detected_files)} auto-detected files, {len(git_commands)} git commands")
            if auto_detected_files:
                print(f"[AI PARSING] Auto-detected files: {[f[0] for f in auto_detected_files]}")
            
            execution_results = []
            execution_log = []
            security_toolkit = auto_punch_components.get('security_toolkit')
            
            # Track workflow progress
            workflow_step_completed = False
            workflow_step_result = ""
            
            # Execute Git commands (with smart auto-installation like Cursor AI)
            if git_commands and security_toolkit:
                emit_progress(session_id, f"🔧 Executing {len(git_commands)} Git command(s)...")
                for action, params in git_commands:
                    try:
                        print(f"[AI CONTROL] Executing Git: {action} {params or ''}")
                        emit_progress(session_id, f"🔧 Git {action}: {params or ''}")
                        execution_log.append(f"🔧 Git {action}: {params or ''}")
                        
                        # Parse params
                        kwargs = {}
                        clone_destination = None
                        if params:
                            if action == 'commit':
                                kwargs['message'] = params.strip('"\'')
                            elif action == 'add':
                                kwargs['files'] = [f.strip() for f in params.split(',')]
                            elif action == 'push' or action == 'pull':
                                parts = params.split()
                                if len(parts) >= 1:
                                    kwargs['remote'] = parts[0]
                                if len(parts) >= 2:
                                    kwargs['branch'] = parts[1]
                            elif action == 'clone':
                                kwargs['repo_url'] = params
                                if ' ' in params:
                                    parts = params.split(' ', 1)
                                    kwargs['repo_url'] = parts[0]
                                    kwargs['destination'] = parts[1]
                                    clone_destination = parts[1]
                        
                        result = security_toolkit.execute_command('git', action, **kwargs)
                        if result.get('success'):
                            output = result.get('output', 'Success')
                            execution_results.append(f"✅ Git {action}: {output[:200]}")
                            execution_log.append(f"✅ Git {action} completed")
                            
                            # SMART AUTO-INSTALLATION after clone (like Cursor AI)
                            if action == 'clone':
                                repo_url = kwargs.get('repo_url', '')
                                # Determine clone destination
                                if clone_destination:
                                    clone_dir = clone_destination
                                elif repo_url:
                                    # Extract repo name from URL
                                    repo_name = os.path.basename(repo_url).replace('.git', '')
                                    workspace = current_workspace or workspace_root
                                    clone_dir = os.path.join(workspace, repo_name)
                                else:
                                    clone_dir = None
                                
                                if clone_dir and os.path.exists(clone_dir):
                                    print(f"[AI CONTROL] 🔍 Detecting project type in: {clone_dir}")
                                    emit_progress(session_id, f"🔍 Detecting project type and installing dependencies...")
                                    
                                    # Check for Node.js (package.json)
                                    package_json = os.path.join(clone_dir, 'package.json')
                                    if os.path.exists(package_json):
                                        print(f"[AI CONTROL] 📦 Detected Node.js project, installing dependencies...")
                                        emit_progress(session_id, "📦 Installing npm dependencies...")
                                        install_cmd = f'cd "{clone_dir}" && npm install'
                                        execution_log.append(f"📦 npm install in {clone_dir}")
                                        # Add to commands to execute
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Python (requirements.txt)
                                    requirements_txt = os.path.join(clone_dir, 'requirements.txt')
                                    if os.path.exists(requirements_txt):
                                        print(f"[AI CONTROL] 🐍 Detected Python project, installing dependencies...")
                                        emit_progress(session_id, "🐍 Installing Python dependencies...")
                                        install_cmd = f'cd "{clone_dir}" && pip install -r requirements.txt'
                                        execution_log.append(f"🐍 pip install -r requirements.txt in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Python (setup.py)
                                    setup_py = os.path.join(clone_dir, 'setup.py')
                                    if os.path.exists(setup_py):
                                        print(f"[AI CONTROL] 🐍 Detected Python package, installing...")
                                        emit_progress(session_id, "🐍 Installing Python package...")
                                        install_cmd = f'cd "{clone_dir}" && pip install -e .'
                                        execution_log.append(f"🐍 pip install -e . in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Python (pyproject.toml)
                                    pyproject_toml = os.path.join(clone_dir, 'pyproject.toml')
                                    if os.path.exists(pyproject_toml):
                                        print(f"[AI CONTROL] 🐍 Detected Python project (pyproject.toml), installing...")
                                        emit_progress(session_id, "🐍 Installing Python package...")
                                        install_cmd = f'cd "{clone_dir}" && pip install -e .'
                                        execution_log.append(f"🐍 pip install -e . in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Go (go.mod)
                                    go_mod = os.path.join(clone_dir, 'go.mod')
                                    if os.path.exists(go_mod):
                                        print(f"[AI CONTROL] 🐹 Detected Go project, downloading dependencies...")
                                        emit_progress(session_id, "🐹 Downloading Go modules...")
                                        install_cmd = f'cd "{clone_dir}" && go mod download'
                                        execution_log.append(f"🐹 go mod download in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Rust (Cargo.toml)
                                    cargo_toml = os.path.join(clone_dir, 'Cargo.toml')
                                    if os.path.exists(cargo_toml):
                                        print(f"[AI CONTROL] 🦀 Detected Rust project, building...")
                                        emit_progress(session_id, "🦀 Building Rust project...")
                                        install_cmd = f'cd "{clone_dir}" && cargo build'
                                        execution_log.append(f"🦀 cargo build in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Java Maven (pom.xml)
                                    pom_xml = os.path.join(clone_dir, 'pom.xml')
                                    if os.path.exists(pom_xml):
                                        print(f"[AI CONTROL] ☕ Detected Java Maven project, installing...")
                                        emit_progress(session_id, "☕ Installing Maven dependencies...")
                                        install_cmd = f'cd "{clone_dir}" && mvn install'
                                        execution_log.append(f"☕ mvn install in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Check for Java Gradle (build.gradle)
                                    build_gradle = os.path.join(clone_dir, 'build.gradle')
                                    if os.path.exists(build_gradle):
                                        print(f"[AI CONTROL] ☕ Detected Java Gradle project, building...")
                                        emit_progress(session_id, "☕ Building Gradle project...")
                                        install_cmd = f'cd "{clone_dir}" && ./gradlew build'
                                        execution_log.append(f"☕ ./gradlew build in {clone_dir}")
                                        commands_to_execute.append(install_cmd)
                                    
                                    # Refresh file explorer to show cloned project
                                    socketio.emit('refresh_file_explorer', {
                                        'file_created': clone_dir,
                                        'workspace': current_workspace or workspace_root
                                    })
                                    
                                    execution_results.append(f"✅ Auto-detected project type and queued dependency installation")
                        else:
                            error = result.get('error', 'Unknown error')
                            execution_results.append(f"❌ Git {action}: {error}")
                            execution_log.append(f"❌ Git {action} failed: {error}")
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ Git {action} error: {error_msg}")
                        execution_log.append(f"❌ Git error: {error_msg}")
            
            # Execute Nmap commands
            if nmap_commands and security_toolkit:
                for action, target in nmap_commands:
                    try:
                        if not target:
                            execution_log.append(f"⚠ Nmap {action}: No target specified")
                            continue
                        
                        print(f"[AI CONTROL] Executing Nmap: {action} on {target}")
                        execution_log.append(f"🔍 Nmap {action}: {target}")
                        
                        result = security_toolkit.execute_command('nmap', action, target=target.strip())
                        if result.get('success'):
                            output = result.get('output', 'Scan completed')
                            execution_results.append(f"✅ Nmap {action} on {target}:\n{output[:500]}")
                            execution_log.append(f"✅ Nmap scan completed")
                        else:
                            error = result.get('error', 'Unknown error')
                            execution_results.append(f"❌ Nmap {action}: {error}")
                            execution_log.append(f"❌ Nmap scan failed: {error}")
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ Nmap {action} error: {error_msg}")
                        execution_log.append(f"❌ Nmap error: {error_msg}")
            
            # Execute Burp Suite commands
            if burp_commands and security_toolkit:
                for action, params in burp_commands:
                    try:
                        print(f"[AI CONTROL] Executing Burp Suite: {action}")
                        execution_log.append(f"🛡️ Burp Suite {action}")
                        
                        kwargs = {}
                        if params:
                            if action == 'launch' and params:
                                kwargs['project_file'] = params.strip('"\'')
                        
                        result = security_toolkit.execute_command('burp', action, **kwargs)
                        if result.get('success'):
                            message = result.get('message', 'Success')
                            execution_results.append(f"✅ Burp Suite {action}: {message}")
                            execution_log.append(f"✅ Burp Suite {action} completed")
                        else:
                            error = result.get('error', 'Unknown error')
                            execution_results.append(f"❌ Burp Suite {action}: {error}")
                            execution_log.append(f"❌ Burp Suite {action} failed: {error}")
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ Burp Suite {action} error: {error_msg}")
                        execution_log.append(f"❌ Burp Suite error: {error_msg}")
            
            # Execute Browser commands
            if browser_commands:
                emit_progress(session_id, f"🌐 Executing {len(browser_commands)} browser command(s)...")
                for action, params in browser_commands:
                    try:
                        print(f"[AI CONTROL] Executing Browser: {action} {params or ''}")
                        emit_progress(session_id, f"🌐 Browser {action}: {params or ''}")
                        execution_log.append(f"🌐 Browser {action}: {params or ''}")
                        
                        if action.lower() == 'navigate' or action.lower() == 'open':
                            url = params.strip() if params else ''
                            if url:
                                socketio.emit('browser_navigate', {'url': url})
                                execution_results.append(f"✅ Browser navigated to: {url}")
                                execution_log.append(f"✅ Browser navigation completed")
                            else:
                                execution_results.append(f"❌ Browser navigate: URL required")
                                execution_log.append(f"❌ Browser navigate: No URL provided")
                        elif action.lower() == 'screenshot':
                            socketio.emit('browser_screenshot_request', {})
                            execution_results.append(f"✅ Browser screenshot requested")
                            execution_log.append(f"✅ Browser screenshot requested")
                        elif action.lower() == 'url' or action.lower() == 'geturl':
                            socketio.emit('browser_get_url', {})
                            execution_results.append(f"✅ Browser URL requested")
                            execution_log.append(f"✅ Browser URL requested")
                        elif action.lower() == 'execute' or action.lower() == 'script':
                            script = params.strip() if params else ''
                            if script:
                                socketio.emit('browser_execute_script', {'script': script})
                                execution_results.append(f"✅ Browser script execution requested")
                                execution_log.append(f"✅ Browser script execution requested")
                            else:
                                execution_results.append(f"❌ Browser execute: Script required")
                                execution_log.append(f"❌ Browser execute: No script provided")
                        else:
                            execution_results.append(f"❌ Browser: Unknown action '{action}'")
                            execution_log.append(f"❌ Browser: Unknown action")
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ Browser {action} error: {error_msg}")
                        execution_log.append(f"❌ Browser error: {error_msg}")
            
            # Create/Write files from AI code generation
            files_created = []
            # Combine explicit file operations with auto-detected files
            all_file_ops = []
            if file_operations or create_files or write_files:
                all_file_ops.extend(file_operations + create_files + write_files)
            # Add auto-detected files
            for filename, lang, code in auto_detected_files:
                all_file_ops.append((filename, lang, code))
            
            if all_file_ops:
                emit_progress(session_id, f"📝 Creating {len(all_file_ops)} file(s) in IDE...")
                for file_op in all_file_ops:
                    try:
                        if len(file_op) >= 3:
                            file_path = file_op[0].strip()
                            language = file_op[1] if file_op[1] else ''
                            code_content = file_op[2]
                        else:
                            continue
                        
                        # Resolve file path - support both absolute and relative paths (like Cursor AI)
                        original_path = file_path
                        
                        # Check if path is absolute
                        if os.path.isabs(file_path):
                            # Use absolute path as-is (Cursor AI style - can write anywhere)
                            print(f"[AI CONTROL] Using absolute path: {file_path}")
                        else:
                            # Handle special paths like "Desktop/", "Documents/", etc.
                            file_path_lower = file_path.lower()
                            
                            # Check for common user directories
                            user_home = os.path.expanduser("~")
                            desktop_path = os.path.join(user_home, "Desktop")
                            documents_path = os.path.join(user_home, "Documents")
                            
                            if file_path_lower.startswith("desktop/"):
                                # Desktop path
                                file_path = os.path.join(desktop_path, file_path[8:])  # Remove "Desktop/"
                                print(f"[AI CONTROL] Resolved Desktop path: {file_path}")
                            elif file_path_lower.startswith("documents/"):
                                # Documents path
                                file_path = os.path.join(documents_path, file_path[10:])  # Remove "Documents/"
                                print(f"[AI CONTROL] Resolved Documents path: {file_path}")
                            elif file_path_lower.startswith("downloads/"):
                                # Downloads path
                                downloads_path = os.path.join(user_home, "Downloads")
                                file_path = os.path.join(downloads_path, file_path[11:])
                                print(f"[AI CONTROL] Resolved Downloads path: {file_path}")
                            else:
                                # Relative to workspace (default behavior)
                                workspace = current_workspace or workspace_root
                                file_path = os.path.join(workspace, file_path)
                                print(f"[AI CONTROL] Resolved relative path to workspace: {file_path}")
                        
                        # Normalize path (remove .. and .)
                        file_path = os.path.normpath(file_path)
                        
                        # Log the final resolved path
                        print(f"[AI CONTROL] Final file path: {file_path}")
                        print(f"[AI CONTROL] Path exists check: {os.path.exists(os.path.dirname(file_path))}")
                        
                        print(f"[AI CONTROL] Creating file: {file_path} (language: {language})")
                        print(f"[AI CONTROL] Workspace: {current_workspace or workspace_root}")
                        print(f"[AI CONTROL] File content preview: {code_content[:100]}...")
                        emit_progress(session_id, f"📝 Creating: {os.path.basename(file_path)}")
                        execution_log.append(f"📝 Creating file: {file_path}")
                        
                        # Write file - ensure directory exists (like Cursor AI - can write anywhere)
                        try:
                            # Get directory and create if it doesn't exist
                            file_dir = os.path.dirname(file_path)
                            if file_dir:  # Only create directory if path has a directory component
                                try:
                                    os.makedirs(file_dir, exist_ok=True)
                                    print(f"[AI CONTROL] ✅ Directory created/verified: {file_dir}")
                                except PermissionError as perm_error:
                                    error_msg = f"Permission denied creating directory: {file_dir}"
                                    print(f"[AI CONTROL] ❌ {error_msg}")
                                    raise PermissionError(error_msg) from perm_error
                                except Exception as dir_error:
                                    print(f"[AI CONTROL] ⚠️ Directory creation warning: {dir_error}")
                            
                            # Write file (Cursor AI style - can write to any accessible location)
                            try:
                                with open(file_path, 'w', encoding='utf-8') as f:
                                    f.write(code_content)
                                print(f"[AI CONTROL] ✅ File write operation completed")
                            except PermissionError as perm_error:
                                error_msg = f"Permission denied writing file: {file_path}"
                                print(f"[AI CONTROL] ❌ {error_msg}")
                                raise PermissionError(error_msg) from perm_error
                            
                            # Verify file was written
                            if os.path.exists(file_path):
                                file_size = os.path.getsize(file_path)
                                print(f"[AI CONTROL] ✅ File written successfully: {file_path} ({file_size} bytes)")
                                print(f"[AI CONTROL] ✅ File is accessible at: {os.path.abspath(file_path)}")
                            else:
                                print(f"[AI CONTROL] ⚠️ File write completed but file not found: {file_path}")
                                print(f"[AI CONTROL] ⚠️ Expected location: {os.path.abspath(file_path)}")
                        except PermissionError as perm_error:
                            error_msg = f"Permission denied: {str(perm_error)}"
                            print(f"[AI CONTROL] ❌ {error_msg}")
                            execution_results.append(f"❌ Permission denied: {file_path}")
                            execution_log.append(f"❌ Permission error: {error_msg}")
                            # Don't raise - continue with other files
                            continue
                        except Exception as write_error:
                            error_details = f"{write_error} (Type: {type(write_error).__name__})"
                            print(f"[AI CONTROL] ❌ File write error: {error_details}")
                            import traceback
                            traceback.print_exc()
                            execution_results.append(f"❌ File creation error: {error_details}")
                            execution_log.append(f"❌ File error: {error_details}")
                            # Don't raise - continue with other files
                            continue
                        
                        files_created.append({'path': file_path, 'language': language})
                        execution_results.append(f"✅ File created: {file_path}")
                        execution_log.append(f"✅ File created successfully")
                        
                        # Show file in terminal
                        workspace = current_workspace or workspace_root
                        file_rel_path = os.path.relpath(file_path, workspace) if os.path.commonpath([workspace, file_path]) == workspace else file_path
                        socketio.emit('terminal_output', {'output': f'\n✅ File created: {file_rel_path}\n'})
                        socketio.emit('show_terminal', {})
                        socketio.emit('force_show_terminal', {})  # Force terminal to open
                        
                        # List directory contents in terminal
                        file_dir = os.path.dirname(file_path)
                        if os.path.exists(file_dir):
                            try:
                                dir_items = os.listdir(file_dir)
                                socketio.emit('terminal_output', {'output': f'\n📁 Directory: {os.path.relpath(file_dir, workspace) if os.path.commonpath([workspace, file_dir]) == workspace else file_dir}\n'})
                                for item in sorted(dir_items):
                                    item_path = os.path.join(file_dir, item)
                                    item_type = '📁' if os.path.isdir(item_path) else '📄'
                                    socketio.emit('terminal_output', {'output': f'  {item_type} {item}\n'})
                            except Exception as e:
                                socketio.emit('terminal_output', {'output': f'  (Could not list directory: {e})\n'})
                        
                        # Calculate relative path for display
                        workspace = current_workspace or workspace_root
                        file_rel_path = os.path.relpath(file_path, workspace) if os.path.commonpath([workspace, file_path]) == workspace else os.path.basename(file_path)
                        
                        # Detect language from file extension if not provided
                        if not language:
                            ext = os.path.splitext(file_path)[1].lower().lstrip('.')
                            lang_map = {
                                'py': 'python', 'js': 'javascript', 'jsx': 'javascript',
                                'ts': 'typescript', 'tsx': 'typescript', 'html': 'html',
                                'css': 'css', 'json': 'json', 'xml': 'xml', 'yaml': 'yaml',
                                'md': 'markdown', 'java': 'java', 'cpp': 'cpp', 'c': 'c',
                                'php': 'php', 'rb': 'ruby', 'go': 'go', 'rs': 'rust'
                            }
                            language = lang_map.get(ext, 'plaintext')
                        
                        # Show file creation in terminal
                        socketio.emit('terminal_output', {'output': f'\n📝 Creating file: {file_rel_path}\n'})
                        socketio.emit('terminal_output', {'output': f'   Language: {language}\n'})
                        socketio.emit('terminal_output', {'output': f'   Size: {len(content)} bytes\n'})
                        
                        # Emit to frontend to open file in editor (like Cursor AI)
                        print(f"[AI CONTROL] ✅ File created: {file_path}")
                        print(f"[AI CONTROL] 📂 Emitting open_file_in_editor event")
                        print(f"[AI CONTROL] Relative path: {file_rel_path}, Language: {language}")
                        
                        # Emit event to open file in editor immediately
                        socketio.emit('open_file_in_editor', {
                            'path': file_path,
                            'relative_path': file_rel_path,
                            'content': code_content,
                            'language': language
                        })
                        
                        # Force refresh file explorer immediately and after delay
                        print(f"[AI CONTROL] 🔄 Refreshing file explorer for workspace: {workspace}")
                        socketio.emit('refresh_file_explorer', {
                            'file_created': file_path,
                            'relative_path': file_rel_path,
                            'workspace': workspace
                        })
                        
                        # Also trigger a delayed refresh to ensure file system sync
                        import threading
                        def delayed_refresh():
                            import time
                            time.sleep(0.8)  # Wait for file system to sync
                            print(f"[AI CONTROL] 🔄 Delayed refresh of file explorer")
                            socketio.emit('refresh_file_explorer', {
                                'file_created': file_path,
                                'relative_path': file_rel_path,
                                'workspace': workspace,
                                'force_reload': True
                            })
                        threading.Thread(target=delayed_refresh, daemon=True).start()
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ File creation error: {error_msg}")
                        execution_log.append(f"❌ File error: {error_msg}")
            
            # Execute marked commands
            if commands_to_execute and automation and automation.is_available():
                emit_progress(session_id, f"⚙️ Executing {len(commands_to_execute)} command(s)...")
                for cmd in commands_to_execute:
                    try:
                        cmd_clean = cmd.strip()
                        
                        # For batch files on Windows, ensure they run in integrated terminal (no new window)
                        if os.name == 'nt' and (cmd_clean.endswith('.bat') or cmd_clean.endswith('.cmd')):
                            # Use cmd /c to run batch file and capture output (no new window)
                            if not cmd_clean.startswith('cmd'):
                                cmd_clean = f'cmd /c "{cmd_clean}"'
                        
                        print(f"[AI CONTROL] Executing: {cmd_clean}")
                        emit_progress(session_id, f"⚙️ Executing: {cmd_clean[:50]}...")
                        socketio.emit('terminal_output', {'output': f'\n⚙️  Executing: {cmd_clean}\n'})
                        execution_log.append(f"🔧 Executing: {cmd_clean}")
                        
                        result = automation.execute_terminal_command(cmd_clean, realtime=False)
                        if result:
                            output = result.get('output', 'Executed')
                            exit_code = result.get('exit_code', 0)
                            success = result.get('success', exit_code == 0)
                            
                            if isinstance(output, list):
                                output = '\n'.join(str(line) for line in output)
                            
                            # VERIFICATION: Check if command actually succeeded (Cursor AI style)
                            output_str = str(output).lower()
                            has_errors = any(indicator in output_str for indicator in [
                                'error', 'failed', 'exception', 'traceback', 
                                'syntaxerror', 'nameerror', 'typeerror', 'fatal',
                                'cannot', 'unable', 'not found', 'no such'
                            ])
                            
                            if success and exit_code == 0 and not has_errors:
                                execution_results.append(f"✅ Command '{cmd_clean}' (VERIFIED):\n{output}")
                                execution_log.append(f"✅ Command verified: {output[:100]}...")
                            elif has_errors or not success:
                                execution_results.append(f"❌ Command '{cmd_clean}' FAILED:\n{output}")
                                execution_log.append(f"❌ Command failed: {output[:100]}...")
                            else:
                                execution_results.append(f"⚠️ Command '{cmd_clean}' (needs verification):\n{output}")
                                execution_log.append(f"⚠️ Command needs verification: {output[:100]}...")
                            
                            # Emit terminal output to frontend
                            socketio.emit('terminal_output', {'output': output})
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ Command '{cmd}' error: {error_msg}")
                        execution_log.append(f"❌ Error: {error_msg}")
            
            # Execute code blocks in terminal
            if code_blocks and automation and automation.is_available():
                emit_progress(session_id, f"💻 Executing {len(code_blocks)} code block(s) in terminal...")
                # Emit command to show terminal panel - FORCE OPEN
                socketio.emit('show_terminal', {})
                socketio.emit('force_show_terminal', {})  # Force terminal to open
                socketio.emit('terminal_output', {'output': '\n' + '='*60 + '\n' + '💻 EXECUTING TERMINAL COMMANDS\n' + '='*60 + '\n'})
                
                for idx, code in enumerate(code_blocks):
                    try:
                        code_clean = code.strip()
                        
                        # Filter out non-command text (like "Press Ctrl+C", debug messages, etc.)
                        lines = code_clean.split('\n')
                        command_lines = []
                        for line in lines:
                            line = line.strip()
                            # Skip lines that look like status messages, not commands
                            if line and not any(skip in line.lower() for skip in [
                                'press', 'debugger', 'running on', 'serving flask',
                                'info:', 'debug:', 'warning:', 'error:', '* debugger',
                                'pin:', 'reload', 'restarting', 'reloader'
                            ]):
                                command_lines.append(line)
                        
                        if not command_lines:
                            print(f"[AI CONTROL] Skipping code block {idx+1} - no valid commands found")
                            continue
                        
                        code_clean = '\n'.join(command_lines)
                        print(f"[AI CONTROL] Executing code block {idx+1}: {code_clean[:100]}...")
                        emit_progress(session_id, f"💻 Executing: {code_clean[:50]}...")
                        socketio.emit('terminal_output', {'output': f'\n💻 Executing code block {idx+1}:\n'})
                        socketio.emit('terminal_output', {'output': f'$ {code_clean}\n'})
                        execution_log.append(f"💻 Executing code: {code_clean[:50]}...")
                        
                        # For batch files on Windows, ensure they run in integrated terminal
                        if os.name == 'nt' and (code_clean.strip().endswith('.bat') or code_clean.strip().endswith('.cmd')):
                            # Use cmd /c to run batch file and capture output
                            if not code_clean.strip().startswith('cmd'):
                                code_clean = f'cmd /c "{code_clean}"'
                        
                        result = automation.execute_terminal_command(code_clean, realtime=False)
                        if result:
                            output = result.get('output', 'Executed')
                            if isinstance(output, list):
                                output = '\n'.join(str(line) for line in output)
                            
                            # Show output in terminal
                            socketio.emit('terminal_output', {'output': f'{output}\n'})
                            
                            execution_results.append(f"✅ Code execution:\n{output}")
                            execution_log.append(f"✅ Code result: {output[:100]}...")
                        else:
                            socketio.emit('terminal_output', {'output': '✅ Command executed (no output)\n'})
                            
                    except Exception as e:
                        error_msg = str(e)
                        print(f"[AI CONTROL] Terminal execution error: {error_msg}")
                        socketio.emit('terminal_output', {'output': f'❌ Error: {error_msg}\n'})
                        execution_results.append(f"❌ Code execution error: {error_msg}")
                        execution_log.append(f"❌ Code error: {error_msg}")
            
            # Update workflow state after execution (Cursor AI style)
            if is_workflow_active and (execution_results or files_created or commands_to_execute):
                # Mark current step as complete
                result_summary = f"Executed {len(execution_results)} actions, created {len(files_created)} files"
                if execution_results:
                    result_summary = execution_results[0] if len(execution_results) == 1 else f"{len(execution_results)} actions completed"
                
                # VERIFICATION: Check if step actually succeeded (Cursor AI style)
                step_verified = False
                verification_needed = False
                
                # Check if this step involved running a program/script
                current_step_text = workflow_agent.get_next_step(state) or ""
                step_lower = current_step_text.lower()
                
                # Detect if verification is needed
                if any(keyword in step_lower for keyword in ['run', 'execute', 'test', 'start', 'launch', 'build', 'compile']):
                    verification_needed = True
                    # Add verification step
                    if 'python' in step_lower or '.py' in step_lower:
                        # Python script - verify it runs
                        workflow_agent.add_verification_step(state, 'run', f"python {current_step_text.split()[-1] if current_step_text.split() else ''}")
                    elif 'npm' in step_lower or 'node' in step_lower:
                        # Node.js - verify it runs
                        workflow_agent.add_verification_step(state, 'run', step_lower)
                    elif 'test' in step_lower:
                        # Test - verify tests pass
                        workflow_agent.add_verification_step(state, 'test', step_lower)
                
                # Check execution results for success indicators
                all_successful = True
                for result in execution_results:
                    if result.startswith('❌') or 'error' in result.lower() or 'failed' in result.lower():
                        all_successful = False
                        break
                
                if all_successful and not verification_needed:
                    step_verified = True
                
                # Mark step complete with verification status
                current_step_num = state.get('current_step', 0)
                state = workflow_agent.mark_step_complete(state, step_result=result_summary, verified=step_verified)
                workflow_agent.update_process_file(f"Step {current_step_num} completed: {result_summary} {'✅ VERIFIED' if step_verified else '⏳ NEEDS VERIFICATION'}")
                
                # Show step completion in terminal
                if step_verified:
                    socketio.emit('terminal_output', {'output': f'\n✅ Step {current_step_num} completed and verified\n'})
                else:
                    socketio.emit('terminal_output', {'output': f'\n⏳ Step {current_step_num} completed (needs verification)\n'})
                
                # If verification needed, add it to the workflow
                if verification_needed:
                    state['phase'] = 'Validation'
                    workflow_agent.save_state(state)
                    socketio.emit('terminal_output', {'output': '🔍 Verification required - will verify step before continuing\n'})
                    response_text += f"\n\n🔍 **VERIFICATION REQUIRED** - Step needs verification before marking complete.\n"
                    response_text += f"Verification will be performed automatically.\n"
                
                # VERIFICATION PHASE: Verify all steps are actually working (Cursor AI style)
                if workflow_agent.is_workflow_complete(state):
                    # Before marking complete, verify everything works
                    verification_steps = state.get('verification_steps', [])
                    pending_verifications = [v for v in verification_steps if v.get('status') == 'pending']
                    
                    if pending_verifications:
                        # Still need to verify
                        state['phase'] = 'Validation'
                        workflow_agent.save_state(state)
                        response_text += f"\n\n🔍 **VALIDATION PHASE** - Verifying {len(pending_verifications)} step(s) are working correctly...\n"
                        response_text += "The system will automatically verify each step before marking complete.\n"
                    else:
                        # All verified - mark complete
                        state['phase'] = 'Complete'
                        workflow_agent.save_state(state)
                        workflow_agent.update_process_file("✅ Workflow completed and verified successfully!")
                        response_text += "\n\n🎉 **WORKFLOW COMPLETE & VERIFIED!** All steps executed and verified successfully.\n"
                else:
                    # AUTOMATICALLY CONTINUE TO NEXT STEP (Cursor AI style - autonomous loop)
                    next_step = workflow_agent.get_next_step(state)
                    if next_step:
                        response_text += f"\n\n⏭️ **Auto-continuing workflow...** Executing next step: {next_step}\n"
                        
                        # Trigger automatic continuation - AI will execute next step automatically
                        def auto_continue_workflow():
                            import time
                            time.sleep(2)  # Small delay to let current response finish
                            
                            # Reload state to get next step
                            workspace = current_workspace or workspace_root
                            agent = WorkflowAgent(workspace)
                            current_state = agent.load_state()
                            
                            # Check if there are more steps
                            if not agent.is_workflow_complete(current_state):
                                next_step_text = agent.get_next_step(current_state)
                                if next_step_text:
                                    print(f"[AGENT] 🔄 Auto-continuing workflow step {current_state.get('current_step', 0) + 1}/{current_state.get('total_steps', 0)}: {next_step_text}")
                                    
                                    # Create a prompt for the AI to execute the next step WITH VERIFICATION
                                    continue_prompt = f"""Continue workflow execution. Current step: {next_step_text}

CRITICAL INSTRUCTIONS:
1. Read workflow_state.md to see the full context
2. Execute this step immediately
3. VERIFY the step actually worked:
   - Check exit codes (must be 0 for success)
   - Check output for errors (no "error", "failed", "exception" in output)
   - If you ran a program -> verify it runs without errors
   - If you created a file -> verify file exists and has correct content
   - If you ran tests -> verify tests pass (exit code 0, no failures)
   - If you started a server -> verify it is running
4. DO NOT mark step complete until it is VERIFIED
5. Update workflow_state.md with verification status
6. Continue to next step automatically after verification

Do not ask for permission - execute, verify, then continue."""
                                    
                                    # Automatically trigger AI to execute next step
                                    # This creates a loop: execute -> update state -> read state -> execute next
                                    try:
                                        hacxgpt = auto_punch_components.get('hacxgpt')
                                        if hacxgpt:
                                            # Get workflow context
                                            workflow_context = f"""
[WORKFLOW CONTINUATION - AUTO-EXECUTE]
Current Phase: {current_state.get('phase', 'Execution')}
Current Step: {current_state.get('current_step', 0)} / {current_state.get('total_steps', 0)}
Next Step to Execute: {next_step_text}

CRITICAL: Execute this step NOW with VERIFICATION!
1. Execute the step without asking permission
2. VERIFY it actually worked (check exit codes, output, results)
3. DO NOT mark complete until verified
4. After verification, automatically continue to the next step
5. Read workflow_state.md for full context
"""
                                            
                                            # Execute next step via AI
                                            print(f"[AGENT] 🤖 Triggering AI to execute: {next_step_text}")
                                            enhanced_prompt = continue_prompt + workflow_context
                                            
                                            # Call AI in background to execute next step
                                            def execute_next_step():
                                                try:
                                                    result = hacxgpt.chat(enhanced_prompt)
                                                    print(f"[AGENT] ✅ Next step execution completed")
                                                    
                                                    # After AI response, check if we need to continue again
                                                    time.sleep(2)  # Wait for state to be updated
                                                    new_state = agent.load_state()
                                                    
                                                    # Check if we're in validation phase (needs verification)
                                                    if new_state.get('phase') == 'Validation':
                                                        print(f"[AGENT] 🔍 Validation phase - verifying steps")
                                                        # Still need to verify - continue verification
                                                        auto_continue_workflow()
                                                    elif not agent.is_workflow_complete(new_state):
                                                        # More steps to execute - recursively continue
                                                        print(f"[AGENT] ⏭️ More steps remaining - continuing")
                                                        auto_continue_workflow()
                                                    else:
                                                        # Check if all verifications are complete
                                                        verification_steps = new_state.get('verification_steps', [])
                                                        pending = [v for v in verification_steps if v.get('status') == 'pending']
                                                        if pending:
                                                            print(f"[AGENT] 🔍 {len(pending)} verification(s) pending")
                                                            # Still need verification
                                                            auto_continue_workflow()
                                                        else:
                                                            print(f"[AGENT] 🎉 Workflow complete and verified!")
                                                            socketio.emit('workflow_complete', {
                                                                'message': 'All workflow steps completed and verified successfully!'
                                                            })
                                                except Exception as e:
                                                    print(f"[AGENT] ❌ Error executing next step: {e}")
                                            
                                            # Execute in background thread
                                            threading.Thread(target=execute_next_step, daemon=True).start()
                                    except Exception as e:
                                        print(f"[AGENT] Error in auto-continuation: {e}")
                        
                        # Start continuation in background
                        threading.Thread(target=auto_continue_workflow, daemon=True).start()
            
            # Add execution results to response
            if execution_results:
                response_text += "\n\n" + "="*60 + "\n"
                response_text += "🔧 COMMAND EXECUTION LOG\n"
                response_text += "="*60 + "\n"
                response_text += "\n".join(execution_log)
                response_text += "\n\n" + "="*60 + "\n"
                response_text += "📋 DETAILED RESULTS\n"
                response_text += "="*60 + "\n"
                response_text += "\n".join(execution_results)
            
            # Add file creation info to response
            if files_created:
                response_text += "\n\n" + "="*60 + "\n"
                response_text += "📝 FILES CREATED IN IDE\n"
                response_text += "="*60 + "\n"
                for file_info in files_created:
                    response_text += f"✅ {file_info['path']} ({file_info['language'] or 'auto'})\n"
                response_text += "\nFiles are now open in the editor!"
            
            total_executed = (
                len(commands_to_execute) + 
                len(git_commands) + 
                len(nmap_commands) + 
                len(burp_commands) +
                len(browser_commands) +
                len(code_blocks) +
                len(file_operations) +
                len(create_files) +
                len(write_files)
            )
            
            if execution_results or files_created:
                return jsonify({
                    'success': True,
                    'response': response_text,
                    'type': 'ai_response',
                    'model': 'HacxGPT (Full System Control)',
                    'executed_commands': total_executed,
                    'files_created': len(files_created)
                })
            
            # Always return response even if no commands were executed
            # Calculate executed commands count
            total_executed = (
                len(commands_to_execute) + 
                len(git_commands) + 
                len(nmap_commands) + 
                len(burp_commands) +
                len(browser_commands) +
                len(code_blocks) +
                len(file_operations) +
                len(create_files) +
                len(write_files)
            )
            
            # Return response (even if empty, we'll handle it on frontend)
            if response_text:
                return jsonify({
                    'success': True,
                    'response': response_text,
                    'streamed': True,  # Indicate that response was streamed
                    'type': 'ai_response',
                    'model': 'HacxGPT (Full System Control)',
                    'executed_commands': total_executed
                })
        except Exception as e:
            print(f"[ERROR] HacxGPT error: {e}")
            import traceback
            traceback.print_exc()
    
    # PRIORITY 2: Natural language automation (AI can execute commands)
    if nl_automation:
        try:
            result = nl_automation.parse_and_execute(message)
            if result:
                return jsonify({
                    'success': True,
                    'response': result.get('message', 'Command executed'),
                    'type': result.get('type', 'command'),
                    'data': result.get('result'),
                    'model': 'NaturalLanguageAutomation (Full Control)'
                })
        except Exception as e:
            print(f"[ERROR] NL automation error: {e}")
    
    # PRIORITY 3: Direct command execution (AI has full control)
    if automation and automation.is_available():
        try:
            # Try to execute as terminal command directly
            result = automation.execute_terminal_command(message, realtime=False)
            if result:
                return jsonify({
                    'success': True,
                    'response': result.get('output', 'Command executed') or 'Command executed successfully',
                    'type': 'command_execution',
                    'model': 'Direct Terminal Control',
                    'raw_result': result
                })
        except Exception as e:
            print(f"[ERROR] Direct execution error: {e}")
    
    # FINAL FALLBACK: Inform user AI has control
    return jsonify({
        'success': True,
        'response': f'[AUTO_PUNCH AI - FULL CONTROL MODE]\n\n' +
                   f'Message received: "{message}"\n\n' +
                   'I have full system control and can:\n' +
                   '• Execute ANY terminal command\n' +
                   '• Read/write/create/delete ANY files\n' +
                   '• Control the entire system\n' +
                   '• Run code, analyze, fix, test\n' +
                   '• Manage git, todos, and more\n\n' +
                   'Tell me what you want me to DO, and I\'ll execute it directly.',
        'type': 'info',
        'model': 'Full Control Mode'
    })

@app.route('/api/code/analyze', methods=['POST'])
def analyze_code():
    """Analyze code using Auto_Punch Ai"""
    data = request.json
    file_path = data.get('path')
    
    if not auto_punch_components.get('code_analyzer'):
        return jsonify({'error': 'Code analyzer not available'}), 500
    
    try:
        result = auto_punch_components['code_analyzer'].analyze_file(file_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/terminal/execute', methods=['POST'])
def execute_terminal():
    """Execute terminal command with live output streaming through WebSocket"""
    data = request.json
    command = data.get('command')
    working_dir = data.get('working_dir', current_workspace or workspace_root)
    session_id = data.get('session_id')  # Get session ID for WebSocket emission
    
    if not command:
        return jsonify({'error': 'No command provided', 'output': 'Error: No command provided'}), 400
    
    # Emit command to terminal panel via WebSocket
    socketio.emit('show_terminal', {})
    socketio.emit('terminal_output', {'output': f'\n$ {command}\n'})
    
    def emit_output(text):
        """Helper to emit output to WebSocket"""
        if text:
            socketio.emit('terminal_output', {'output': text})
    
    # Try automation first
    if auto_punch_components.get('automation_enabled'):
        try:
            automation = auto_punch_components['automation']
            if working_dir:
                automation.set_working_directory(working_dir)
            
            # For batch files on Windows, ensure they run in integrated terminal (no new window)
            # Import os here to ensure it's in scope
            import os as os_module
            if os_module.name == 'nt' and (command.strip().endswith('.bat') or command.strip().endswith('.cmd')):
                # Use cmd /c to run batch file and capture output (no new window)
                if not command.strip().startswith('cmd'):
                    command = f'cmd /c "{command}"'
            
            # Execute with realtime output
            result = automation.execute_terminal_command(command, realtime=True)
            
            # Format output for display
            output = result.get('output', '')
            if isinstance(output, list):
                output = '\n'.join(str(line) for line in output)
            elif output is None:
                output = ''
            
            # Emit output to WebSocket
            if output:
                emit_output(output)
            else:
                emit_output('Command executed (no output)')
            
            return jsonify({
                'success': result.get('success', True),
                'output': output or 'Command executed (no output)',
                'exit_code': result.get('exit_code', 0),
                'command': command
            })
        except Exception as e:
            print(f"[TERMINAL ERROR] Automation error: {e}")
            import traceback
            traceback.print_exc()
            error_msg = f'Error: {str(e)}'
            emit_output(error_msg)
            # Fall through to subprocess fallback
    
    # Fallback: Use subprocess with real-time streaming
    try:
        import subprocess
        import os
        import threading
        import queue
        
        # Set working directory
        original_dir = os.getcwd()
        if working_dir and os.path.exists(working_dir):
            os.chdir(working_dir)
        
        # Prepare command
        if os.name == 'nt':  # Windows
            # For batch files, use cmd.exe /c to run in same process and capture output
            if command.strip().endswith('.bat') or command.strip().endswith('.cmd'):
                if not command.strip().startswith('cmd'):
                    command = f'cmd /c "{command}"'
        
        # Use Popen for real-time output streaming
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            cwd=working_dir if working_dir else None,
            creationflags=0  # Don't create new console window
        )
        
        # Stream output in real-time
        output_lines = []
        def read_output():
            try:
                for line in iter(process.stdout.readline, ''):
                    if line:
                        line = line.rstrip()
                        output_lines.append(line)
                        emit_output(line + '\n')
                process.stdout.close()
            except Exception as e:
                emit_output(f'\nError reading output: {str(e)}\n')
        
        # Start reading output in background thread
        output_thread = threading.Thread(target=read_output, daemon=True)
        output_thread.start()
        
        # Wait for process to complete
        exit_code = process.wait()
        
        # Restore original directory
        os.chdir(original_dir)
        
        # Get final output
        output = '\n'.join(output_lines)
        
        return jsonify({
            'success': exit_code == 0,
            'output': output or 'Command executed (no output)',
            'exit_code': exit_code,
            'command': command
        })
    except subprocess.TimeoutExpired:
        error_msg = 'Error: Command execution timed out after 30 seconds'
        emit_output(error_msg)
        return jsonify({
            'error': 'Command timed out',
            'output': error_msg
        }), 500
    except Exception as e:
        print(f"[TERMINAL ERROR] Subprocess error: {e}")
        import traceback
        traceback.print_exc()
        error_msg = f'Error executing command: {str(e)}'
        emit_output(error_msg)
        return jsonify({
            'error': str(e),
            'output': error_msg
        }), 500

@app.route('/api/signnow/check', methods=['POST'])
def signnow_check():
    """SignNow.com login checker - runs in dashboard"""
    from datetime import datetime
    
    data = request.json
    combo_file = data.get('combo_file', 'combo.txt')
    delay = float(data.get('delay', 1.0))
    timeout = int(data.get('timeout', 10))
    
    # Import the checker
    try:
        from signnow_checker import SignNowChecker
    except ImportError:
        return jsonify({
            'error': 'SignNow checker module not found',
            'output': 'Error: signnow_checker.py not found in workspace'
        }), 500
    
    # Get workspace directory
    workspace = current_workspace or workspace_root
    combo_path = os.path.join(workspace, combo_file) if workspace else combo_file
    
    if not os.path.exists(combo_path):
        return jsonify({
            'error': f'Combo file not found: {combo_path}',
            'output': f'Error: File not found: {combo_path}'
        }), 400
    
    # Emit to terminal panel
    socketio.emit('show_terminal', {})
    socketio.emit('terminal_output', {'output': f'\n{'='*60}\n🔐 SignNow.com Login Checker\n{'='*60}\n'})
    socketio.emit('terminal_output', {'output': f'[*] Reading combos from: {combo_file}\n'})
    socketio.emit('terminal_output', {'output': f'[*] Delay between requests: {delay}s\n'})
    socketio.emit('terminal_output', {'output': f'[*] Timeout: {timeout}s\n'})
    socketio.emit('terminal_output', {'output': '-'*60 + '\n'})
    
    # Create checker instance with custom output handler
    class DashboardSignNowChecker(SignNowChecker):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        
        def check_from_file(self, filename, output_file=None):
            """Override to emit to dashboard terminal"""
            socketio.emit('terminal_output', {'output': f'[*] Starting SignNow checker...\n'})
            socketio.emit('terminal_output', {'output': f'[*] Reading combos from: {filename}\n'})
            socketio.emit('terminal_output', {'output': f'[*] Delay between requests: {self.delay}s\n'})
            socketio.emit('terminal_output', {'output': '-'*60 + '\n'})
            
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                
                total = len(lines)
                socketio.emit('terminal_output', {'output': f'[*] Found {total} combos to check\n\n'})
                
                for idx, line in enumerate(lines, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse combo
                    if ':' in line:
                        parts = line.split(':', 1)
                    elif '|' in line:
                        parts = line.split('|', 1)
                    else:
                        socketio.emit('terminal_output', {'output': f'[!] Skipping invalid format: {line}\n'})
                        continue
                    
                    if len(parts) != 2:
                        socketio.emit('terminal_output', {'output': f'[!] Skipping invalid format: {line}\n'})
                        continue
                    
                    email = parts[0].strip()
                    password = parts[1].strip()
                    
                    if not email or not password:
                        continue
                    
                    socketio.emit('terminal_output', {'output': f'[{idx}/{total}] Checking: {email}\n'})
                    
                    is_valid, message = self.check_credentials(email, password)
                    
                    if is_valid:
                        result = f'    ✓ VALID - {email}:{password} - {message}\n'
                        socketio.emit('terminal_output', {'output': result})
                        self.results['valid'].append({
                            'email': email,
                            'password': password,
                            'message': message,
                            'timestamp': datetime.now().isoformat()
                        })
                    else:
                        result = f'    ✗ INVALID - {email} - {message}\n'
                        socketio.emit('terminal_output', {'output': result})
                        self.results['invalid'].append({
                            'email': email,
                            'message': message,
                            'timestamp': datetime.now().isoformat()
                        })
                    
                    # Save results incrementally
                    if output_file:
                        self.save_results(output_file)
                    
                    # Delay between requests
                    if idx < total:
                        import time
                        time.sleep(self.delay)
                
                # Final summary
                socketio.emit('terminal_output', {'output': '\n' + '='*60 + '\n'})
                socketio.emit('terminal_output', {'output': 'CHECK COMPLETE\n'})
                socketio.emit('terminal_output', {'output': '='*60 + '\n'})
                socketio.emit('terminal_output', {'output': f'Total checked: {total}\n'})
                socketio.emit('terminal_output', {'output': f'Valid: {len(self.results['valid'])}\n'})
                socketio.emit('terminal_output', {'output': f'Invalid: {len(self.results['invalid'])}\n'})
                socketio.emit('terminal_output', {'output': f'Errors: {len(self.results['errors'])}\n'})
                
                if self.results['valid']:
                    socketio.emit('terminal_output', {'output': '\n✓ VALID CREDENTIALS:\n'})
                    for result in self.results['valid']:
                        socketio.emit('terminal_output', {'output': f'  {result["email"]}:{result["password"]}\n'})
                
                # Save final results
                if output_file:
                    self.save_results(output_file)
                    socketio.emit('terminal_output', {'output': f'\n[*] Results saved to: {output_file}\n'})
                
            except FileNotFoundError:
                socketio.emit('terminal_output', {'output': f'[!] Error: File \'{filename}\' not found\n'})
            except Exception as e:
                socketio.emit('terminal_output', {'output': f'[!] Error reading file: {e}\n'})
    
    # Run checker in background thread
    def run_checker():
        try:
            checker = DashboardSignNowChecker(delay=delay, timeout=timeout)
            output_file = os.path.join(workspace, 'signnow_results.json') if workspace else 'signnow_results.json'
            checker.check_from_file(combo_path, output_file)
        except Exception as e:
            socketio.emit('terminal_output', {'output': f'\n[!] Error: {str(e)}\n'})
            import traceback
            traceback.print_exc()
    
    # Start checker in background thread
    import threading
    thread = threading.Thread(target=run_checker, daemon=True)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'SignNow checker started',
        'output': 'Checker is running in terminal panel...'
    })

@app.route('/api/todos/list', methods=['GET'])
def list_todos():
    """List todos"""
    if not auto_punch_components.get('todo_manager'):
        # Return empty list instead of error
        return jsonify({'todos': [], 'count': 0, 'message': 'Todo manager not available'})
    
    try:
        status = request.args.get('status')
        todos = auto_punch_components['todo_manager'].list_todos(status=status)
        if todos is None:
            todos = []
        return jsonify({'todos': todos, 'count': len(todos) if todos else 0})
    except Exception as e:
        print(f"[ERROR] Todo list error: {e}")
        import traceback
        traceback.print_exc()
        # Return empty list instead of error
        return jsonify({'todos': [], 'count': 0, 'error': str(e)})

@app.route('/api/todos/add', methods=['POST'])
def add_todo():
    """Add todo"""
    data = request.json
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Todo content is required'}), 400
    
    if not auto_punch_components.get('todo_manager'):
        return jsonify({'error': 'Todo manager not available'}), 500
    
    try:
        todo = auto_punch_components['todo_manager'].add_todo(content)
        if todo:
            return jsonify({'success': True, 'todo': todo})
        else:
            return jsonify({'error': 'Failed to add todo'}), 500
    except Exception as e:
        print(f"[ERROR] Add todo error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/update', methods=['POST'])
def update_todo():
    """Update todo"""
    data = request.json
    todo_id = data.get('id')
    content = data.get('content')
    status = data.get('status')
    
    if not auto_punch_components.get('todo_manager'):
        return jsonify({'error': 'Todo manager not available'}), 500
    
    try:
        todo = auto_punch_components['todo_manager'].update_todo(
            todo_id, content=content, status=status
        )
        if todo:
            return jsonify({'success': True, 'todo': todo})
        return jsonify({'error': 'Todo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/delete', methods=['POST'])
def delete_todo():
    """Delete todo"""
    data = request.json
    todo_id = data.get('id')
    
    if not auto_punch_components.get('todo_manager'):
        return jsonify({'error': 'Todo manager not available'}), 500
    
    try:
        success = auto_punch_components['todo_manager'].delete_todo(todo_id)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/git/status', methods=['GET'])
def git_status():
    """Get git status"""
    if not auto_punch_components.get('git_operations'):
        return jsonify({'error': 'Git operations not available'}), 500
    
    try:
        result = auto_punch_components['git_operations'].status()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Extension Management API
@app.route('/api/extensions/list', methods=['GET'])
def list_extensions():
    """List all installed extensions"""
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'extensions': [], 'error': 'Extension manager not available'})
    
    try:
        extensions = extension_manager.list_extensions()
        return jsonify({'extensions': extensions, 'count': len(extensions)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/search', methods=['POST'])
def search_extensions():
    """Search VS Code marketplace for extensions"""
    data = request.json
    query = data.get('query', '')
    limit = data.get('limit', 20)
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'extensions': [], 'error': 'Extension manager not available'})
    
    try:
        results = extension_manager.search_marketplace(query, limit)
        return jsonify({'extensions': results, 'count': len(results)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/install', methods=['POST'])
def install_extension():
    """Install extension from marketplace with real installation process"""
    data = request.json
    extension_id = data.get('id')
    version = data.get('version')
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'error': 'Extension manager not available'}), 500
    
    try:
        print(f"[EXTENSION] Installing: {extension_id}")
        
        # Get extension details first
        marketplace_url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
        
        # Parse extension ID
        if '.' in extension_id:
            publisher, ext_name = extension_id.split('.', 1)
            payload = {
                "filters": [{
                    "criteria": [{"filterType": 7, "value": extension_id}]
                }],
                "flags": 0x200
            }
        else:
            payload = {
                "filters": [{
                    "criteria": [
                        {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                        {"filterType": 10, "value": extension_id}
                    ],
                    "pageNumber": 1,
                    "pageSize": 1
                }],
                "flags": 0x200
            }
        
        import requests
        response = requests.post(
            marketplace_url,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            timeout=30
        )
        
        if response.status_code != 200:
            return jsonify({'success': False, 'error': f'Marketplace API error: {response.status_code}'})
        
        data_resp = response.json()
        if not data_resp.get('results') or not data_resp['results'][0].get('extensions'):
            return jsonify({'success': False, 'error': 'Extension not found in marketplace'})
        
        extension_data = data_resp['results'][0]['extensions'][0]
        versions = extension_data.get('versions', [])
        
        if not versions:
            return jsonify({'success': False, 'error': 'No versions available'})
        
        target_version = versions[0] if not version else next(
            (v for v in versions if v.get('version') == version), versions[0]
        )
        
        # Get download URL
        asset_uri = target_version.get('assetUri', '')
        if not asset_uri:
            return jsonify({'success': False, 'error': 'No download URL available'})
        
        download_url = asset_uri + '/Microsoft.VisualStudio.Services.VSIXPackage'
        proper_id = extension_data.get('extensionId') or extension_id
        
        print(f"[EXTENSION] Downloading from: {download_url}")
        print(f"[EXTENSION] Extension ID: {proper_id}")
        
        # Install with progress
        result = extension_manager.install_from_url(download_url, proper_id)
        
        if result.get('success'):
            # Reload extensions
            extension_manager.load_extensions()
            print(f"[EXTENSION] ✓ Installed: {proper_id}")
        else:
            print(f"[EXTENSION] ✗ Failed: {result.get('error')}")
        
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/install-from-url', methods=['POST'])
def install_extension_from_url():
    """Install extension from URL"""
    data = request.json
    url = data.get('url')
    extension_id = data.get('id')
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'error': 'Extension manager not available'}), 500
    
    try:
        result = extension_manager.install_from_url(url, extension_id)
        if result.get('success'):
            extension_manager.load_extensions()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/uninstall', methods=['POST'])
def uninstall_extension():
    """Uninstall extension"""
    data = request.json
    extension_id = data.get('id')
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'error': 'Extension manager not available'}), 500
    
    try:
        result = extension_manager.uninstall_extension(extension_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/enable', methods=['POST'])
def enable_extension():
    """Enable extension"""
    data = request.json
    extension_id = data.get('id')
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'error': 'Extension manager not available'}), 500
    
    try:
        result = extension_manager.enable_extension(extension_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/disable', methods=['POST'])
def disable_extension():
    """Disable extension"""
    data = request.json
    extension_id = data.get('id')
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'error': 'Extension manager not available'}), 500
    
    try:
        result = extension_manager.disable_extension(extension_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/extensions/get', methods=['GET'])
def get_extension():
    """Get extension details"""
    extension_id = request.args.get('id')
    
    extension_manager = auto_punch_components.get('extension_manager')
    if not extension_manager:
        return jsonify({'error': 'Extension manager not available'}), 500
    
    try:
        extension = extension_manager.get_extension(extension_id)
        if extension:
            contributions = extension_manager.get_extension_contributions(extension_id)
            extension['contributions'] = contributions
            return jsonify(extension)
        return jsonify({'error': 'Extension not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# SSH Connection Management
try:
    from ssh_manager import SSHManager
    ssh_manager = SSHManager()
    print("✓ SSH Manager initialized")
except Exception as e:
    print(f"⚠ SSH Manager error: {e}")
    ssh_manager = None

@app.route('/api/ssh/add', methods=['POST'])
def add_ssh_connection():
    """Add new SSH connection"""
    if not ssh_manager:
        return jsonify({'success': False, 'error': 'SSH Manager not available'}), 500
    
    data = request.json
    try:
        result = ssh_manager.add_connection(
            name=data.get('name', ''),
            host=data.get('host', ''),
            port=int(data.get('port', 22)),
            username=data.get('username', ''),
            auth_method=data.get('auth_method', 'password'),
            password=data.get('password'),
            key_path=data.get('key_path')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ssh/list', methods=['GET'])
def list_ssh_connections():
    """List all SSH connections"""
    if not ssh_manager:
        return jsonify({'success': False, 'connections': [], 'error': 'SSH Manager not available'})
    
    try:
        connections = ssh_manager.list_connections()
        return jsonify({'success': True, 'connections': connections})
    except Exception as e:
        return jsonify({'success': False, 'connections': [], 'error': str(e)})

@app.route('/api/ssh/connect', methods=['POST'])
def connect_ssh():
    """Connect to SSH server"""
    if not ssh_manager:
        return jsonify({'success': False, 'error': 'SSH Manager not available'}), 500
    
    data = request.json
    connection_id = data.get('id')
    
    try:
        result = ssh_manager.connect(connection_id)
        if result.get('success'):
            # Stream connection output to terminal
            socketio.emit('terminal_output', {'output': f"🔐 Connecting to {connection_id}...\n"})
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ssh/disconnect', methods=['POST'])
def disconnect_ssh():
    """Disconnect from SSH server"""
    if not ssh_manager:
        return jsonify({'success': False, 'error': 'SSH Manager not available'}), 500
    
    data = request.json
    connection_id = data.get('id')
    
    try:
        result = ssh_manager.disconnect(connection_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ssh/delete', methods=['POST'])
def delete_ssh_connection():
    """Delete SSH connection"""
    if not ssh_manager:
        return jsonify({'success': False, 'error': 'SSH Manager not available'}), 500
    
    data = request.json
    connection_id = data.get('id')
    
    try:
        result = ssh_manager.delete_connection(connection_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ssh/execute', methods=['POST'])
def execute_ssh_command():
    """Execute command on remote SSH server"""
    if not ssh_manager:
        return jsonify({'success': False, 'error': 'SSH Manager not available'}), 500
    
    data = request.json
    connection_id = data.get('id')
    command = data.get('command', '')
    
    try:
        result = ssh_manager.execute_command(connection_id, command)
        if result.get('success'):
            # Stream output to terminal
            output = result.get('output', '')
            error = result.get('error', '')
            if output:
                socketio.emit('terminal_output', {'output': output})
            if error:
                socketio.emit('terminal_output', {'output': f"Error: {error}\n"})
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/ai/execute', methods=['POST'])
def ai_execute():
    """AI direct execution endpoint - AI can execute ANYTHING"""
    data = request.json
    action = data.get('action')  # 'command', 'read_file', 'write_file', 'delete_file', etc.
    params = data.get('params', {})
    
    ai_control = auto_punch_components.get('ai_control')
    if not ai_control:
        return jsonify({'error': 'AI System Control not available'}), 500
    
    try:
        if action == 'execute_command':
            command = params.get('command')
            working_dir = params.get('working_dir', current_workspace or workspace_root)
            result = ai_control.execute_command(command, working_dir)
            return jsonify(result)
        
        elif action == 'read_file':
            file_path = params.get('path')
            result = ai_control.read_file(file_path)
            return jsonify(result)
        
        elif action == 'write_file':
            file_path = params.get('path')
            content = params.get('content', '')
            result = ai_control.write_file(file_path, content)
            return jsonify(result)
        
        elif action == 'delete_file':
            file_path = params.get('path')
            result = ai_control.delete_file(file_path)
            return jsonify(result)
        
        elif action == 'analyze_code':
            file_path = params.get('path')
            result = ai_control.analyze_code(file_path)
            return jsonify(result)
        
        elif action == 'fix_code':
            file_path = params.get('path')
            result = ai_control.fix_code(file_path)
            return jsonify(result)
        
        elif action == 'system_info':
            result = ai_control.system_info()
            return jsonify(result)
        
        elif action == 'git_status':
            result = ai_control.git_status()
            return jsonify(result)
        
        elif action == 'git_commit':
            message = params.get('message')
            result = ai_control.git_commit(message)
            return jsonify(result)
        
        elif action == 'add_todo':
            content = params.get('content')
            result = ai_control.add_todo(content)
            return jsonify(result)
        
        elif action == 'list_todos':
            status = params.get('status')
            result = ai_control.list_todos(status)
            return jsonify(result)
        
        elif action == 'git_command':
            action_git = params.get('action', 'status')
            git_params = params.get('params', {})
            result = ai_control.git_command(action_git, **git_params)
            return jsonify(result)
        
        elif action == 'nmap_scan':
            action_nmap = params.get('action', 'scan')
            nmap_params = params.get('params', {})
            result = ai_control.nmap_scan(action_nmap, **nmap_params)
            return jsonify(result)
        
        elif action == 'burp_suite':
            action_burp = params.get('action', 'status')
            burp_params = params.get('params', {})
            result = ai_control.burp_suite(action_burp, **burp_params)
            return jsonify(result)
        
        elif action == 'toolkit_status':
            result = ai_control.toolkit_status()
            return jsonify(result)
        
        elif action == 'redteam_tool_execute':
            # Execute a RedTeam tool - AI has FULL CONTROL
            tool_name = params.get('tool_name')
            tool_path = params.get('tool_path')
            arguments = params.get('arguments', [])
            working_dir = params.get('working_dir')
            
            toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
            if not os.path.exists(toolkit_path):
                return jsonify({'error': 'RedTeam-Tools repository not found'}), 404
            
            socketio.emit('show_terminal', {})
            socketio.emit('force_show_terminal', {})
            socketio.emit('terminal_output', {'output': f'\n🔧 AI Executing RedTeam Tool: {tool_name}\n'})
            
            # Find and execute tool
            if tool_path:
                cmd = tool_path if os.path.isabs(tool_path) else os.path.join(toolkit_path, tool_path)
            else:
                cmd = find_tool_in_repo(toolkit_path, tool_name)
                if not cmd:
                    return jsonify({'error': f'Tool {tool_name} not found'}), 404
            
            if isinstance(arguments, list):
                cmd_parts = [cmd] + arguments
            elif isinstance(arguments, str):
                cmd_parts = [cmd] + arguments.split()
            else:
                cmd_parts = [cmd]
            
            socketio.emit('terminal_output', {'output': f'$ {" ".join(cmd_parts)}\n'})
            
            automation = auto_punch_components.get('automation')
            if automation and automation.is_available():
                result = automation.execute_terminal_command(' '.join(cmd_parts), realtime=True, cwd=working_dir or toolkit_path)
                return jsonify({
                    'success': result.get('success', False) if result else False,
                    'output': result.get('output', '') if result else '',
                    'exit_code': result.get('exit_code', 1) if result else 1
                })
            else:
                return jsonify({'error': 'Terminal automation not available'}), 500
        
        elif action == 'redteam_tool_install':
            # Install a RedTeam tool - AI has FULL CONTROL
            tool_name = params.get('tool_name')
            tool_url = params.get('tool_url')
            install_commands = params.get('install_commands', [])
            
            toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
            if not os.path.exists(toolkit_path):
                return jsonify({'error': 'RedTeam-Tools repository not found'}), 404
            
            socketio.emit('show_terminal', {})
            socketio.emit('force_show_terminal', {})
            socketio.emit('terminal_output', {'output': f'\n📦 AI Installing RedTeam Tool: {tool_name}\n'})
            
            if tool_url and ('github.com' in tool_url or tool_url.startswith('http')):
                install_dir = os.path.join(toolkit_path, tool_name.lower().replace(' ', '-'))
                socketio.emit('terminal_output', {'output': f'Cloning from: {tool_url}\n'})
                
                automation = auto_punch_components.get('automation')
                if automation and automation.is_available():
                    clone_cmd = f'git clone {tool_url} "{install_dir}"'
                    socketio.emit('terminal_output', {'output': f'$ {clone_cmd}\n'})
                    result = automation.execute_terminal_command(clone_cmd, realtime=True, cwd=toolkit_path)
                    
                    if result and result.get('success'):
                        socketio.emit('terminal_output', {'output': f'✅ Tool cloned successfully\n'})
                        
                        # Run install commands
                        for install_cmd in install_commands:
                            socketio.emit('terminal_output', {'output': f'$ {install_cmd}\n'})
                            automation.execute_terminal_command(install_cmd, realtime=True, cwd=install_dir)
                        
                        return jsonify({
                            'success': True,
                            'message': f'Tool {tool_name} installed',
                            'path': install_dir
                        })
                    else:
                        return jsonify({'error': 'Failed to clone tool'}), 500
                else:
                    return jsonify({'error': 'Terminal automation not available'}), 500
            else:
                return jsonify({'error': 'Tool URL required for installation'}), 400
        
        elif action == 'redteam_tool_list':
            # List available RedTeam tools
            toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
            readme_path = os.path.join(toolkit_path, 'README.md')
            
            if not os.path.exists(readme_path):
                return jsonify({'error': 'RedTeam-Tools repository not found'}), 404
            
            tools = parse_redteam_tools(readme_path)
            category_filter = params.get('category')
            
            if category_filter:
                tools = [t for t in tools if t['category'].lower() == category_filter.lower()]
            
            return jsonify({
                'success': True,
                'tools': tools,
                'total': len(tools)
            })
        
        else:
            return jsonify({'error': f'Unknown action: {action}'}), 400
            
    except Exception as e:
        print(f"[ERROR] AI execute error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/scan', methods=['POST'])
def security_scan():
    """Run security scan and return results"""
    data = request.json or {}
    target_path = data.get('path', current_workspace or workspace_root)
    scan_type = data.get('type', 'full')  # 'full', 'sast', 'dependencies', 'npm', 'pip'
    
    security_scanner = auto_punch_components.get('security_scanner')
    if not security_scanner:
        return jsonify({'error': 'Security scanner not available'}), 500
    
    try:
        if scan_type == 'full':
            results = security_scanner.run_full_scan(target_path)
        elif scan_type == 'sast':
            results = {
                'semgrep': security_scanner.scan_with_semgrep(target_path),
                'trivy': security_scanner.scan_with_trivy(target_path)
            }
        elif scan_type == 'dependencies':
            results = {
                'trivy': security_scanner.scan_with_trivy(target_path),
                'osv-scanner': security_scanner.scan_with_osv_scanner(target_path),
                'npm': security_scanner.scan_npm_dependencies(),
                'pip': security_scanner.scan_pip_dependencies()
            }
        elif scan_type == 'npm':
            results = {'npm': security_scanner.scan_npm_dependencies()}
        elif scan_type == 'pip':
            results = {'pip': security_scanner.scan_pip_dependencies()}
        else:
            return jsonify({'error': f'Unknown scan type: {scan_type}'}), 400
        
        # Format results for AI
        formatted_output = security_scanner.format_findings_for_ai(results if scan_type == 'full' else {'all_findings': [], 'timestamp': '', 'target': target_path})
        
        return jsonify({
            'success': True,
            'results': results,
            'formatted_output': formatted_output,
            'total_findings': results.get('total_findings', 0) if scan_type == 'full' else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/scan-and-fix', methods=['POST'])
def security_scan_and_fix():
    """Run security scan and let AI propose/implement fixes"""
    data = request.json or {}
    target_path = data.get('path', current_workspace or workspace_root)
    auto_fix = data.get('auto_fix', False)  # Whether to automatically implement fixes
    
    security_scanner = auto_punch_components.get('security_scanner')
    hacxgpt = auto_punch_components.get('hacxgpt')
    
    if not security_scanner:
        return jsonify({'error': 'Security scanner not available'}), 500
    if not hacxgpt:
        return jsonify({'error': 'AI model not available'}), 500
    
    try:
        # Run full scan
        scan_results = security_scanner.run_full_scan(target_path)
        formatted_output = security_scanner.format_findings_for_ai(scan_results)
        
        # Send to AI for analysis and fix proposals
        ai_prompt = f"""Analyze these security scan results and propose fixes:

{formatted_output}

For each finding:
1. Analyze the vulnerability/issue
2. Propose a fix
3. {'Automatically implement the fix' if auto_fix else 'Provide fix code that can be applied'}

Focus on:
- High and critical severity issues first
- Dependency vulnerabilities (update packages)
- Code security issues (fix code patterns)
- Provide safe, tested fixes
"""
        
        # Get AI response with fixes
        ai_response = hacxgpt.chat(ai_prompt)
        
        return jsonify({
            'success': True,
            'scan_results': scan_results,
            'formatted_output': formatted_output,
            'ai_analysis': ai_response,
            'total_findings': scan_results.get('total_findings', 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Security Toolkit API Endpoints
@app.route('/api/security-toolkit/status', methods=['GET'])
def security_toolkit_status():
    """Get security toolkit status"""
    security_toolkit = auto_punch_components.get('security_toolkit')
    if not security_toolkit:
        return jsonify({'error': 'Security toolkit not available'}), 500
    
    try:
        status = security_toolkit.get_status()
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/toolkit/status', methods=['GET'])
def toolkit_status():
    """Get comprehensive toolkit status (Security Toolkit + Dashboard Fix Agent)"""
    security_toolkit = auto_punch_components.get('security_toolkit')
    dashboard_fix_agent = auto_punch_components.get('dashboard_fix_agent')
    
    result = {
        'security_toolkit': {},
        'dashboard_fix_agent': {'available': dashboard_fix_agent is not None}
    }
    
    if security_toolkit:
        try:
            status = security_toolkit.get_status()
            result['security_toolkit'] = status
        except Exception as e:
            result['security_toolkit'] = {'error': str(e), 'available': False}
    else:
        result['security_toolkit'] = {'available': False}
    
    if dashboard_fix_agent:
        result['dashboard_fix_agent']['openai_available'] = dashboard_fix_agent.openai_client is not None
    else:
        result['dashboard_fix_agent']['openai_available'] = False
    
    return jsonify(result)

@app.route('/api/git/command', methods=['POST'])
def git_command():
    """Execute Git command"""
    data = request.json
    action = data.get('action', 'status')
    kwargs = data.get('params', {})
    
    security_toolkit = auto_punch_components.get('security_toolkit')
    if not security_toolkit:
        return jsonify({'error': 'Security toolkit not available'}), 500
    
    try:
        result = security_toolkit.execute_command('git', action, **kwargs)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/nmap/scan', methods=['POST'])
def nmap_scan():
    """Execute Nmap scan"""
    data = request.json
    action = data.get('action', 'scan')
    target = data.get('target', '')
    options = data.get('options', None)
    output_format = data.get('format', 'text')
    
    if not target:
        return jsonify({'error': 'Target is required'}), 400
    
    security_toolkit = auto_punch_components.get('security_toolkit')
    if not security_toolkit:
        return jsonify({'error': 'Security toolkit not available'}), 500
    
    try:
        result = security_toolkit.execute_command(
            'nmap', 
            action, 
            target=target,
            options=options,
            format=output_format
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/burp/command', methods=['POST'])
def burp_command():
    """Execute Burp Suite command"""
    data = request.json
    action = data.get('action', 'status')
    kwargs = data.get('params', {})
    
    security_toolkit = auto_punch_components.get('security_toolkit')
    if not security_toolkit:
        return jsonify({'error': 'Security toolkit not available'}), 500
    
    try:
        result = security_toolkit.execute_command('burp', action, **kwargs)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard/fix', methods=['POST'])
def dashboard_fix():
    """Fix dashboard issues using the dashboard fix agent"""
    data = request.json
    issue = data.get('issue', '').strip()
    auto_apply = data.get('auto_apply', False)
    
    if not issue:
        return jsonify({'success': False, 'error': 'Please provide an issue description'})
    
    dashboard_fix_agent = auto_punch_components.get('dashboard_fix_agent')
    if not dashboard_fix_agent:
        return jsonify({'success': False, 'error': 'Dashboard Fix Agent not available'}), 500
    
    try:
        # Get session ID for progress updates
        session_id = request.headers.get('X-Session-ID') or 'default'
        
        # Set up progress callback
        def progress_callback(update):
            emit_progress(session_id, update.get('message', ''), update.get('data'))
            if update.get('type') == 'file_explored':
                emit_file_explored(session_id, update.get('file'), update.get('lines'))
            elif update.get('type') == 'diff':
                emit_diff(session_id, update.get('file'), 
                         update.get('old_content', ''), 
                         update.get('new_content', ''))
        
        dashboard_fix_agent.progress_callback = progress_callback
        
        result = dashboard_fix_agent.fix_issue(issue, auto_apply=auto_apply)
        return jsonify(result)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/browser/navigate', methods=['POST'])
def browser_navigate():
    """Navigate browser preview to a URL (AI accessible)"""
    data = request.json
    url = data.get('url', '').strip()
    
    if not url:
        return jsonify({'success': False, 'error': 'URL is required'})
    
    # Validate URL
    if not url.startswith('http://') and not url.startswith('https://'):
        if '.' in url and ' ' not in url:
            url = 'https://' + url
        else:
            url = 'https://www.google.com/search?q=' + url.replace(' ', '+')
    
    try:
        # Emit to all connected clients to navigate browser
        socketio.emit('browser_navigate', {'url': url})
        return jsonify({'success': True, 'url': url, 'message': f'Navigating to {url}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/browser/screenshot', methods=['GET'])
def browser_screenshot():
    """Take a screenshot of the browser preview (AI accessible)"""
    try:
        # Note: Actual screenshot requires browser automation (Selenium/Playwright)
        # For now, return the current URL as a placeholder
        # In production, you'd use headless browser automation
        
        # Emit request to frontend to capture screenshot
        socketio.emit('browser_screenshot_request', {})
        
        return jsonify({
            'success': True,
            'message': 'Screenshot request sent to browser preview',
            'note': 'Full screenshot requires browser automation integration'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/browser/url', methods=['GET'])
def browser_get_url():
    """Get current browser preview URL (AI accessible)"""
    try:
        # This would need to track the current URL in the session
        # For now, return a placeholder
        return jsonify({
            'success': True,
            'url': 'Unknown - URL tracking not implemented',
            'note': 'URL tracking requires frontend state management'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/browser/execute', methods=['POST'])
def browser_execute():
    """Execute JavaScript in browser preview (AI accessible)"""
    data = request.json
    script = data.get('script', '').strip()
    
    if not script:
        return jsonify({'success': False, 'error': 'JavaScript code is required'})
    
    try:
        # Emit to frontend to execute script in iframe
        socketio.emit('browser_execute_script', {'script': script})
        return jsonify({
            'success': True,
            'message': 'Script execution request sent',
            'note': 'Script execution in iframe may be limited by CORS'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Progress tracking for real-time updates
active_sessions = {}  # session_id -> request context

def emit_progress(session_id: str, message: str, data: dict = None):
    """Emit progress update to client"""
    try:
        # If session_id is 'default' or not a valid socket session, broadcast to all
        if session_id and session_id != 'default' and session_id in active_sessions:
            socketio.emit('ai_progress', {
                'message': message,
                'data': data or {},
                'timestamp': threading.current_thread().name
            }, room=session_id)
        else:
            # Broadcast to all connected clients
            socketio.emit('ai_progress', {
                'message': message,
                'data': data or {},
                'timestamp': threading.current_thread().name
            })
    except Exception as e:
        print(f"Error emitting progress: {e}")

def emit_file_explored(session_id: str, file_path: str, lines: str = None):
    """Emit file exploration update"""
    try:
        if session_id and session_id != 'default' and session_id in active_sessions:
            socketio.emit('file_explored', {
                'file': file_path,
                'lines': lines,
                'timestamp': threading.current_thread().name
            }, room=session_id)
        else:
            socketio.emit('file_explored', {
                'file': file_path,
                'lines': lines,
                'timestamp': threading.current_thread().name
            })
    except Exception as e:
        print(f"Error emitting file explored: {e}")

def emit_diff(session_id: str, file_path: str, old_content: str, new_content: str):
    """Emit code diff"""
    try:
        if session_id and session_id != 'default' and session_id in active_sessions:
            socketio.emit('code_diff', {
                'file': file_path,
                'old_content': old_content,
                'new_content': new_content,
                'timestamp': threading.current_thread().name
            }, room=session_id)
        else:
            socketio.emit('code_diff', {
                'file': file_path,
                'old_content': old_content,
                'new_content': new_content,
                'timestamp': threading.current_thread().name
            })
    except Exception as e:
        print(f"Error emitting diff: {e}")

@app.route('/api/silverbullet/install-requirement', methods=['POST'])
def install_requirement():
    """Install a requirement (Deno, Go, or Git)"""
    import subprocess
    import shutil
    import urllib.request
    import zipfile
    import tarfile
    
    data = request.json
    requirement = data.get('requirement')  # 'deno', 'go', or 'git'
    
    if requirement not in ['deno', 'go', 'git']:
        return jsonify({'success': False, 'error': 'Invalid requirement'}), 400
    
    def emit_progress_msg(message, progress):
        socketio.emit('silverbullet_install_progress', {
            'step': 'install_requirement',
            'message': f'[{requirement.upper()}] {message}',
            'progress': progress
        })
    
    try:
        if requirement == 'deno':
            emit_progress_msg('Installing Deno...', 10)
            if os.name == 'nt':  # Windows
                # Use PowerShell to install Deno
                install_cmd = 'powershell -Command "irm https://deno.land/install.ps1 | iex"'
                result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    emit_progress_msg('Deno installed successfully', 100)
                    return jsonify({'success': True, 'message': 'Deno installed'})
                else:
                    return jsonify({'success': False, 'error': result.stderr}), 500
            else:  # Unix/Linux
                install_cmd = 'curl -fsSL https://deno.land/install.sh | sh'
                result = subprocess.run(install_cmd, shell=True, capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    emit_progress_msg('Deno installed successfully', 100)
                    return jsonify({'success': True, 'message': 'Deno installed'})
                else:
                    return jsonify({'success': False, 'error': result.stderr}), 500
        
        elif requirement == 'go':
            emit_progress_msg('Installing Go...', 10)
            # Go installation is more complex, provide instructions
            if os.name == 'nt':  # Windows
                return jsonify({
                    'success': False,
                    'error': 'Go installation requires manual setup',
                    'instructions': 'Please download and install Go from https://go.dev/dl/',
                    'download_url': 'https://go.dev/dl/'
                }), 400
            else:
                # Try to install via package manager
                for cmd in [['apt-get', 'install', '-y', 'golang-go'], ['yum', 'install', '-y', 'golang']]:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                        if result.returncode == 0:
                            emit_progress_msg('Go installed successfully', 100)
                            return jsonify({'success': True, 'message': 'Go installed'})
                    except:
                        continue
                return jsonify({
                    'success': False,
                    'error': 'Go installation failed. Please install manually.',
                    'instructions': 'Install Go from https://go.dev/dl/ or use your package manager'
                }), 500
        
        elif requirement == 'git':
            emit_progress_msg('Installing Git...', 10)
            if os.name == 'nt':  # Windows
                # Try to install via winget or chocolatey
                for cmd in [
                    ['winget', 'install', '--id', 'Git.Git', '-e', '--source', 'winget'],
                    ['choco', 'install', 'git', '-y']
                ]:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                        if result.returncode == 0:
                            emit_progress_msg('Git installed successfully', 100)
                            return jsonify({'success': True, 'message': 'Git installed'})
                    except:
                        continue
                return jsonify({
                    'success': False,
                    'error': 'Git installation requires winget or chocolatey',
                    'instructions': 'Please install Git from https://git-scm.com/download/win',
                    'download_url': 'https://git-scm.com/download/win'
                }), 400
            else:
                # Try package manager
                for cmd in [['apt-get', 'install', '-y', 'git'], ['yum', 'install', '-y', 'git']]:
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                        if result.returncode == 0:
                            emit_progress_msg('Git installed successfully', 100)
                            return jsonify({'success': True, 'message': 'Git installed'})
                    except:
                        continue
                return jsonify({
                    'success': False,
                    'error': 'Git installation failed. Please install manually.',
                    'instructions': 'Install Git from https://git-scm.com/download/ or use your package manager'
                }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Installation timed out'}), 500
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/silverbullet/requirements', methods=['GET'])
def silverbullet_requirements():
    """Check SilverBullet installation requirements"""
    import subprocess
    import shutil
    
    requirements = {
        'deno': {'installed': False, 'version': None, 'path': None},
        'go': {'installed': False, 'version': None, 'path': None},
        'git': {'installed': False, 'version': None, 'path': None}
    }
    
    # Check Deno
    deno_path = shutil.which('deno')
    if deno_path:
        try:
            result = subprocess.run(['deno', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                requirements['deno'] = {
                    'installed': True,
                    'version': result.stdout.strip().split('\n')[0] if result.stdout else 'Unknown',
                    'path': deno_path
                }
        except:
            pass
    
    # Check Go
    go_path = shutil.which('go')
    if go_path:
        try:
            result = subprocess.run(['go', 'version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                requirements['go'] = {
                    'installed': True,
                    'version': result.stdout.strip(),
                    'path': go_path
                }
        except:
            pass
    
    # Check Git
    git_path = shutil.which('git')
    if git_path:
        try:
            result = subprocess.run(['git', '--version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                requirements['git'] = {
                    'installed': True,
                    'version': result.stdout.strip(),
                    'path': git_path
                }
        except:
            pass
    
    # Check if SilverBullet is installed
    silverbullet_installed = False
    silverbullet_path = None
    
    # Check common locations
    possible_paths = [
        shutil.which('silverbullet'),
        os.path.join(os.path.expanduser('~'), '.deno', 'bin', 'silverbullet'),
        os.path.join(workspace_root, 'silverbullet', 'silverbullet'),
        os.path.join(workspace_root, 'silverbullet', 'silverbullet.exe'),
    ]
    
    for path in possible_paths:
        if path and os.path.exists(path):
            silverbullet_installed = True
            silverbullet_path = path
            break
    
    all_requirements_met = all(req['installed'] for req in requirements.values())
    
    return jsonify({
        'requirements': requirements,
        'all_met': all_requirements_met,
        'silverbullet_installed': silverbullet_installed,
        'silverbullet_path': silverbullet_path
    })

@app.route('/api/silverbullet/install', methods=['POST'])
def silverbullet_install():
    """One-click SilverBullet installation"""
    import subprocess
    import shutil
    import threading
    
    def install_in_background():
        """Install SilverBullet in background thread"""
        try:
            # Check requirements first
            deno_path = shutil.which('deno')
            go_path = shutil.which('go')
            git_path = shutil.which('git')
            
            if not deno_path:
                socketio.emit('silverbullet_install_progress', {
                    'step': 'error',
                    'message': 'Deno is required but not installed. Please install Deno first.',
                    'progress': 0
                })
                return
            
            if not go_path:
                socketio.emit('silverbullet_install_progress', {
                    'step': 'error',
                    'message': 'Go is required but not installed. Please install Go first.',
                    'progress': 0
                })
                return
            
            if not git_path:
                socketio.emit('silverbullet_install_progress', {
                    'step': 'error',
                    'message': 'Git is required but not installed. Please install Git first.',
                    'progress': 0
                })
                return
            
            # Step 1: Clone repository
            socketio.emit('silverbullet_install_progress', {
                'step': 'clone',
                'message': 'Cloning SilverBullet repository...',
                'progress': 10
            })
            
            install_dir = os.path.join(workspace_root, 'silverbullet')
            if os.path.exists(install_dir):
                import shutil as sh
                sh.rmtree(install_dir)
            
            clone_result = subprocess.run(
                ['git', 'clone', 'https://github.com/silverbulletmd/silverbullet.git', install_dir],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=workspace_root
            )
            
            if clone_result.returncode != 0:
                socketio.emit('silverbullet_install_progress', {
                    'step': 'error',
                    'message': f'Failed to clone repository: {clone_result.stderr}',
                    'progress': 0
                })
                return
            
            # Step 2: Build SilverBullet
            socketio.emit('silverbullet_install_progress', {
                'step': 'build',
                'message': 'Building SilverBullet (this may take a few minutes)...',
                'progress': 30
            })
            
            # Try to build using make or direct commands
            build_commands = [
                ['make'],  # Try make first
                ['deno', 'task', 'build'],  # Fallback to deno task
            ]
            
            build_success = False
            for cmd in build_commands:
                try:
                    build_result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=600,  # 10 minutes for build
                        cwd=install_dir
                    )
                    if build_result.returncode == 0:
                        build_success = True
                        break
                except:
                    continue
            
            if not build_success:
                socketio.emit('silverbullet_install_progress', {
                    'step': 'error',
                    'message': 'Build failed. Check terminal for details.',
                    'progress': 0
                })
                return
            
            socketio.emit('silverbullet_install_progress', {
                'step': 'complete',
                'message': 'SilverBullet installed successfully!',
                'progress': 100,
                'path': install_dir
            })
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            socketio.emit('silverbullet_install_progress', {
                'step': 'error',
                'message': f'Installation error: {str(e)}',
                'progress': 0
            })
    
    # Start installation in background
    thread = threading.Thread(target=install_in_background, daemon=True)
    thread.start()
    
    return jsonify({
        'success': True,
        'message': 'Installation started in background. Check progress below.'
    })

@app.route('/api/silverbullet/status', methods=['GET'])
def silverbullet_status():
    """Check if SilverBullet server is running"""
    import requests
    url = request.args.get('url', 'http://localhost:3000')
    
    try:
        response = requests.get(url, timeout=2)
        return jsonify({
            'running': True,
            'url': url,
            'status_code': response.status_code
        })
    except requests.exceptions.RequestException:
        return jsonify({
            'running': False,
            'url': url,
            'error': 'Server not responding'
        })

@app.route('/api/silverbullet/start', methods=['POST'])
def silverbullet_start():
    """Start SilverBullet server"""
    import subprocess
    import shutil
    
    data = request.json
    space_path = data.get('space_path', os.path.join(workspace_root, 'silverbullet_space'))
    port = data.get('port', 3000)
    
    try:
        # Check if SilverBullet is installed
        
        # Try to find silverbullet executable
        silverbullet_cmd = shutil.which('silverbullet')
        if not silverbullet_cmd:
            # Try common installation paths
            possible_paths = [
                os.path.join(os.path.expanduser('~'), '.deno', 'bin', 'silverbullet'),
                os.path.join(workspace_root, 'silverbullet', 'silverbullet'),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    silverbullet_cmd = path
                    break
        
        if not silverbullet_cmd or not os.path.exists(silverbullet_cmd):
            return jsonify({
                'success': False,
                'error': 'SilverBullet not found. Please install it first.',
                'instructions': 'See https://github.com/silverbulletmd/silverbullet for installation'
            }), 404
        
        # Create space directory if it doesn't exist
        os.makedirs(space_path, exist_ok=True)
        
        # Start SilverBullet server in background
        cmd = [silverbullet_cmd, space_path, '--port', str(port)]
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=workspace_root
        )
        
        # Store process info
        if 'silverbullet_process' not in globals():
            globals()['silverbullet_process'] = {}
        globals()['silverbullet_process'][port] = process
        
        return jsonify({
            'success': True,
            'url': f'http://localhost:{port}',
            'space_path': space_path,
            'pid': process.pid
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/silverbullet/stop', methods=['POST'])
def silverbullet_stop():
    """Stop SilverBullet server"""
    data = request.json
    port = data.get('port', 3000)
    
    try:
        if 'silverbullet_process' in globals():
            processes = globals().get('silverbullet_process', {})
            if port in processes:
                process = processes[port]
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                del processes[port]
                return jsonify({'success': True, 'message': f'Stopped server on port {port}'})
        
        return jsonify({'success': False, 'error': 'No server running on that port'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    active_sessions[session_id] = {'connected': True}
    emit('connected', {'message': 'Connected to Auto_Punch IDE', 'session_id': session_id})

@socketio.on('disconnect')
def handle_disconnect(data=None):
    """Handle client disconnect"""
    session_id = request.sid
    if session_id in active_sessions:
        del active_sessions[session_id]

@app.route('/api/toolkit/test', methods=['GET'])
def toolkit_test():
    """Test endpoint to verify routing works"""
    return jsonify({'success': True, 'message': 'Toolkit API is accessible'})

def discover_tools_in_subdirectories(toolkit_path):
    """Discover tools in subdirectories (cloned repositories)"""
    discovered_tools = []
    
    if not os.path.exists(toolkit_path):
        return discovered_tools
    
    try:
        # Known tool directories
        known_tools = {
            '365-Stealer': {
                'name': '365-Stealer',
                'description': 'Phishing simulation tool for executing Illicit Consent Grant attacks in Microsoft 365/Azure AD',
                'category': 'Initial Access',
                'main_file': '365-Stealer.py',
                'repo_url': 'https://github.com/AlteredSecurity/365-Stealer'
            },
            'requests-ip-rotator': {
                'name': 'requests-ip-rotator',
                'description': 'IP rotation library for Python requests using AWS API Gateway',
                'category': 'Defense Evasion',
                'main_file': None,  # It's a Python library
                'repo_url': 'https://github.com/Ge0rg3/requests-ip-rotator'
            }
        }
        
        # Check each known tool directory
        for dir_name, tool_info in known_tools.items():
            tool_dir = os.path.join(toolkit_path, dir_name)
            if os.path.exists(tool_dir) and os.path.isdir(tool_dir):
                # Find main executable file
                main_file = None
                if tool_info['main_file']:
                    main_file_path = os.path.join(tool_dir, tool_info['main_file'])
                    if os.path.exists(main_file_path):
                        main_file = tool_info['main_file']
                    else:
                        # Try case-insensitive search
                        dir_files = [f for f in os.listdir(tool_dir) if os.path.isfile(os.path.join(tool_dir, f))]
                        for file in dir_files:
                            if file.lower() == tool_info['main_file'].lower():
                                main_file = file
                                break
                else:
                    # Look for common entry points
                    for entry_file in ['main.py', 'run.py', 'app.py', 'tool.py', 'setup.py']:
                        entry_path = os.path.join(tool_dir, entry_file)
                        if os.path.exists(entry_path):
                            main_file = entry_file
                            break
                
                # If still no main file, look for any .py file in root
                if not main_file:
                    dir_files = [f for f in os.listdir(tool_dir) if os.path.isfile(os.path.join(tool_dir, f)) and f.endswith('.py')]
                    if dir_files:
                        main_file = dir_files[0]  # Use first Python file found
                
                # Check for README
                readme_path = os.path.join(tool_dir, 'README.md')
                description = tool_info['description']
                if os.path.exists(readme_path):
                    try:
                        with open(readme_path, 'r', encoding='utf-8') as f:
                            readme_content = f.read()
                            # Extract first paragraph as description
                            lines = readme_content.split('\n')
                            for line in lines:
                                if line.strip() and not line.strip().startswith('#'):
                                    description = line.strip()[:200]  # First 200 chars
                                    break
                    except:
                        pass
                
                # Generate tool ID from name
                tool_id = tool_info['name'].lower().replace(' ', '-').replace('_', '-').replace('.', '-')
                
                tool_entry = {
                    'id': tool_id,
                    'name': tool_info['name'],
                    'description': description,
                    'category': tool_info['category'],
                    'path': os.path.join(dir_name, main_file) if main_file else dir_name,
                    'directory': dir_name,
                    'main_file': main_file,
                    'repo_url': tool_info['repo_url'],
                    'discovered': True  # Mark as discovered (not from README)
                }
                discovered_tools.append(tool_entry)
                print(f"[TOOLKIT] Discovered tool: {tool_info['name']} in {dir_name}")
        
        # Also scan for any other directories that might be tools
        for item in os.listdir(toolkit_path):
            item_path = os.path.join(toolkit_path, item)
            if os.path.isdir(item_path) and item not in known_tools and not item.startswith('.'):
                # Check if it looks like a tool (has README or Python files)
                has_readme = os.path.exists(os.path.join(item_path, 'README.md'))
                has_python = any(f.endswith('.py') for f in os.listdir(item_path) if os.path.isfile(os.path.join(item_path, f)))
                
                if has_readme or has_python:
                    # Try to find main file
                    main_file = None
                    for entry_file in ['main.py', 'run.py', 'app.py', 'tool.py', f'{item}.py']:
                        entry_path = os.path.join(item_path, entry_file)
                        if os.path.exists(entry_path):
                            main_file = entry_file
                            break
                    
                    if main_file or has_python:
                        tool_name = item.replace('-', ' ').replace('_', ' ').title()
                        tool_id = item.lower().replace(' ', '-').replace('_', '-')
                        
                        tool_entry = {
                            'id': tool_id,
                            'name': tool_name,
                            'description': f'Tool found in {item} directory',
                            'category': 'Other',
                            'path': os.path.join(item, main_file) if main_file else item,
                            'directory': item,
                            'main_file': main_file,
                            'discovered': True
                        }
                        discovered_tools.append(tool_entry)
                        print(f"[TOOLKIT] Auto-discovered tool: {item}")
    
    except Exception as e:
        print(f"[TOOLKIT] Error discovering tools: {e}")
        import traceback
        traceback.print_exc()
    
    return discovered_tools

@app.route('/api/toolkit/list', methods=['GET'])
def toolkit_list():
    """List all available RedTeam tools"""
    try:
        toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
        readme_path = os.path.join(toolkit_path, 'README.md')
        
        # Debug logging
        print(f"[TOOLKIT] Listing tools from: {toolkit_path}")
        print(f"[TOOLKIT] README path: {readme_path}")
        print(f"[TOOLKIT] Toolkit exists: {os.path.exists(toolkit_path)}")
        print(f"[TOOLKIT] README exists: {os.path.exists(readme_path)}")
        
        if not os.path.exists(toolkit_path):
            return jsonify({
                'success': False,
                'error': f'RedTeam-Tools repository not found at: {toolkit_path}',
                'workspace_root': workspace_root
            }), 404
        
        # Parse README to extract tools (if exists)
        tools = []
        if os.path.exists(readme_path):
            tools = parse_redteam_tools(readme_path)
            # Filter out "Red Team Tips" category (safety check)
            tools = [t for t in tools if t.get('category') != 'Red Team Tips']
        
        # Discover tools in subdirectories
        discovered_tools = discover_tools_in_subdirectories(toolkit_path)
        
        # Merge tools (avoid duplicates by name)
        tool_names = {t['name'].lower() for t in tools}
        for discovered in discovered_tools:
            if discovered['name'].lower() not in tool_names:
                tools.append(discovered)
                tool_names.add(discovered['name'].lower())
        
        # Debug: Count by category
        category_counts = {}
        for tool in tools:
            cat = tool.get('category', 'Unknown')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print(f"[TOOLKIT API] Total tools: {len(tools)} (from README: {len(tools) - len(discovered_tools)}, discovered: {len(discovered_tools)})")
        print(f"[TOOLKIT API] Categories: {category_counts}")
        
        return jsonify({
            'success': True,
            'tools': tools,
            'total': len(tools),
            'toolkit_path': toolkit_path,
            'categories': category_counts,
            'discovered_count': len(discovered_tools)
        })
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"[TOOLKIT] Error: {e}")
        print(f"[TOOLKIT] Traceback: {error_trace}")
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': error_trace
        }), 500

@app.route('/api/toolkit/tool/<tool_name>', methods=['GET'])
def toolkit_tool_info(tool_name):
    """Get information about a specific tool"""
    try:
        toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
        readme_path = os.path.join(toolkit_path, 'README.md')
        
        if not os.path.exists(readme_path):
            return jsonify({'error': 'RedTeam-Tools repository not found'}), 404
        
        # Parse README to find tool
        tools = parse_redteam_tools(readme_path)
        tool = next((t for t in tools if t['name'].lower() == tool_name.lower()), None)
        
        if not tool:
            return jsonify({'error': 'Tool not found'}), 404
        
        return jsonify({
            'success': True,
            'tool': tool
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/toolkit/execute', methods=['POST'])
def toolkit_execute():
    """Execute a RedTeam tool - AI has full control"""
    try:
        data = request.json
        tool_name = data.get('tool_name')
        tool_path = data.get('tool_path')  # Optional: specific path to tool
        arguments = data.get('arguments', [])  # Tool arguments
        working_dir = data.get('working_dir')  # Optional: working directory
        
        toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
        
        if not os.path.exists(toolkit_path):
            return jsonify({'error': 'RedTeam-Tools repository not found'}), 404
        
        # Show in terminal
        socketio.emit('show_terminal', {})
        socketio.emit('force_show_terminal', {})
        socketio.emit('terminal_output', {'output': f'\n🔧 Executing RedTeam Tool: {tool_name}\n'})
        
        # Build command
        if tool_path:
            # Use specific tool path
            if os.path.isabs(tool_path):
                cmd = tool_path
            else:
                cmd = os.path.join(toolkit_path, tool_path)
        else:
            # Try to find tool in repository
            cmd = find_tool_in_repo(toolkit_path, tool_name)
            if not cmd:
                return jsonify({'error': f'Tool {tool_name} not found in repository'}), 404
        
        # Add arguments
        if isinstance(arguments, list):
            cmd_parts = [cmd] + arguments
        elif isinstance(arguments, str):
            cmd_parts = [cmd] + arguments.split()
        else:
            cmd_parts = [cmd]
        
        # Execute command
        socketio.emit('terminal_output', {'output': f'$ {" ".join(cmd_parts)}\n'})
        
        automation = auto_punch_components.get('automation')
        if automation and automation.is_available():
            result = automation.execute_terminal_command(' '.join(cmd_parts), realtime=True, cwd=working_dir or toolkit_path)
            
            if result:
                output = result.get('output', '')
                exit_code = result.get('exit_code', 0)
                success = result.get('success', exit_code == 0)
                
                return jsonify({
                    'success': success,
                    'output': output,
                    'exit_code': exit_code,
                    'tool': tool_name
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Command execution failed',
                    'tool': tool_name
                }), 500
        else:
            return jsonify({'error': 'Terminal automation not available'}), 500
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/toolkit/install', methods=['POST'])
def toolkit_install():
    """Install a RedTeam tool - AI has full control"""
    try:
        data = request.json
        tool_name = data.get('tool_name')
        tool_url = data.get('tool_url')  # GitHub URL or tool path
        install_commands = data.get('install_commands', [])  # Optional: custom install commands
        
        toolkit_path = os.path.join(workspace_root, 'RedTeam-Tools')
        
        if not os.path.exists(toolkit_path):
            return jsonify({'error': 'RedTeam-Tools repository not found'}), 404
        
        # Show in terminal
        socketio.emit('show_terminal', {})
        socketio.emit('force_show_terminal', {})
        socketio.emit('terminal_output', {'output': f'\n📦 Installing RedTeam Tool: {tool_name}\n'})
        
        # If tool_url provided, clone it
        if tool_url:
            if 'github.com' in tool_url or tool_url.startswith('http'):
                # Clone from GitHub
                install_dir = os.path.join(toolkit_path, tool_name.lower().replace(' ', '-'))
                socketio.emit('terminal_output', {'output': f'Cloning from: {tool_url}\n'})
                
                automation = auto_punch_components.get('automation')
                if automation and automation.is_available():
                    # Clone repository
                    clone_cmd = f'git clone {tool_url} "{install_dir}"'
                    socketio.emit('terminal_output', {'output': f'$ {clone_cmd}\n'})
                    result = automation.execute_terminal_command(clone_cmd, realtime=True, cwd=toolkit_path)
                    
                    if result and result.get('success'):
                        socketio.emit('terminal_output', {'output': f'✅ Tool cloned successfully\n'})
                        
                        # Run install commands if provided
                        if install_commands:
                            for install_cmd in install_commands:
                                socketio.emit('terminal_output', {'output': f'$ {install_cmd}\n'})
                                install_result = automation.execute_terminal_command(install_cmd, realtime=True, cwd=install_dir)
                        
                        return jsonify({
                            'success': True,
                            'message': f'Tool {tool_name} installed successfully',
                            'path': install_dir
                        })
                    else:
                        return jsonify({
                            'success': False,
                            'error': 'Failed to clone tool repository'
                        }), 500
        else:
            # Tool might already be in repository, just verify
            tool_path = find_tool_in_repo(toolkit_path, tool_name)
            if tool_path:
                return jsonify({
                    'success': True,
                    'message': f'Tool {tool_name} already available',
                    'path': tool_path
                })
            else:
                return jsonify({
                    'success': False,
                    'error': f'Tool {tool_name} not found and no URL provided'
                }), 404
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# ============================================================
# Telegram Integration API Endpoints
# ============================================================

@app.route('/api/telegram/status', methods=['GET'])
def telegram_status():
    """Check Telegram bot status"""
    return jsonify({
        'enabled': telegram_bot.enabled,
        'configured': bool(telegram_bot.bot_token and telegram_bot.chat_id)
    })

@app.route('/api/telegram/send', methods=['POST'])
def telegram_send():
    """Send message via Telegram bot"""
    data = request.json
    message = data.get('message', '')
    priority = data.get('priority', 'info')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    if not telegram_bot.enabled:
        return jsonify({'error': 'Telegram bot not configured'}), 400
    
    success = telegram_bot.send_notification('Auto_Punch IDE', message, priority)
    return jsonify({'success': success})

@app.route('/api/telegram/update-check', methods=['GET'])
def telegram_update_check():
    """Check for desktop app updates"""
    release = github_release.get_latest_release()
    if not release:
        return jsonify({'error': 'Failed to check for updates'}), 500
    
    assets = github_release.get_release_assets(release)
    return jsonify({
        'success': True,
        'version': assets['version'],
        'exe_url': assets['exe_url'],
        'msi_url': assets['msi_url'],
        'changelog': assets['changelog'],
        'published_at': assets['published_at']
    })

@app.route('/api/telegram/notify-update', methods=['POST'])
def telegram_notify_update():
    """Notify users about new update"""
    data = request.json
    version = data.get('version', '')
    download_url = data.get('download_url', '')
    changelog = data.get('changelog', '')
    
    if not version or not download_url:
        return jsonify({'error': 'Version and download_url are required'}), 400
    
    success = telegram_bot.notify_update(version, download_url, changelog)
    return jsonify({'success': success})

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """Handle GitHub release webhook"""
    data = request.json
    
    # Verify it's a release event
    if data.get('action') == 'published':
        release = data.get('release', {})
        version = release.get('tag_name', '')
        
        # Get download URLs from assets
        assets = release.get('assets', [])
        exe_url = None
        msi_url = None
        
        for asset in assets:
            name = asset.get('name', '').lower()
            url = asset.get('browser_download_url', '')
            if name.endswith('.exe'):
                exe_url = url
            elif name.endswith('.msi'):
                msi_url = url
        
        download_url = exe_url or msi_url or release.get('html_url', '')
        changelog = release.get('body', '')
        
        # Notify via Telegram
        if telegram_bot.enabled and download_url:
            telegram_bot.notify_update(version, download_url, changelog)
        
        return jsonify({
            'status': 'ok',
            'version': version,
            'notified': telegram_bot.enabled
        })
    
    return jsonify({'status': 'ok'})

# Dashboard Telegram Notifications
@app.route('/api/telegram/dashboard/notify', methods=['POST'])
def telegram_dashboard_notify():
    """Send dashboard event notification via Telegram"""
    data = request.json
    event_type = data.get('event_type', 'info')
    title = data.get('title', 'Dashboard Event')
    details = data.get('details', '')
    event_data = data.get('data', {})
    
    if not telegram_bot.enabled:
        return jsonify({'error': 'Telegram bot not configured'}), 400
    
    success = telegram_bot.notify_dashboard_event(event_type, title, details, event_data)
    return jsonify({'success': success})

@app.route('/api/telegram/dashboard/terminal', methods=['POST'])
def telegram_dashboard_terminal():
    """Send terminal command notification via Telegram"""
    data = request.json
    command = data.get('command', '')
    output = data.get('output', '')
    success = data.get('success', True)
    
    if not telegram_bot.enabled:
        return jsonify({'error': 'Telegram bot not configured'}), 400
    
    if not command:
        return jsonify({'error': 'Command is required'}), 400
    
    success_sent = telegram_bot.notify_terminal_command(command, output, success)
    return jsonify({'success': success_sent})

@app.route('/api/telegram/dashboard/toolkit', methods=['POST'])
def telegram_dashboard_toolkit():
    """Send toolkit execution notification via Telegram"""
    data = request.json
    tool_name = data.get('tool_name', '')
    result = data.get('result', '')
    success = data.get('success', True)
    
    if not telegram_bot.enabled:
        return jsonify({'error': 'Telegram bot not configured'}), 400
    
    if not tool_name:
        return jsonify({'error': 'Tool name is required'}), 400
    
    success_sent = telegram_bot.notify_toolkit_execution(tool_name, result, success)
    return jsonify({'success': success_sent})

@app.route('/api/telegram/dashboard/status', methods=['GET'])
def telegram_dashboard_status():
    """Get dashboard integration status"""
    return jsonify({
        'telegram_enabled': telegram_bot.enabled,
        'settings_sync_enabled': settings_sync.enabled,
        'features': {
            'terminal_notifications': telegram_bot.enabled,
            'toolkit_notifications': telegram_bot.enabled,
            'extension_notifications': telegram_bot.enabled,
            'git_notifications': telegram_bot.enabled,
            'dashboard_fix_notifications': telegram_bot.enabled,
            'settings_sync': settings_sync.enabled
        }
    })

@app.route('/api/settings/sync', methods=['POST'])
def sync_settings():
    """Sync settings with Supabase"""
    data = request.json
    user_id = data.get('user_id')
    settings = data.get('settings', {})
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    success = settings_sync.save_settings(user_id, settings)
    return jsonify({'success': success})

@app.route('/api/settings/get', methods=['GET'])
def get_settings():
    """Get settings from Supabase"""
    user_id = request.args.get('user_id', type=int)
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    settings = settings_sync.get_settings(user_id)
    return jsonify({'success': True, 'settings': settings})

@app.route('/api/desktop/register', methods=['POST'])
def register_desktop():
    """Register desktop app installation"""
    data = request.json
    user_id = data.get('user_id')
    device_id = data.get('device_id', '')
    app_version = data.get('app_version', '1.0.0')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    success = settings_sync.register_desktop(user_id, device_id, app_version)
    return jsonify({'success': success})

def find_tool_in_repo(toolkit_path, tool_name):
    """Find a tool in the RedTeam-Tools repository"""
    tool_name_lower = tool_name.lower().replace(' ', '-').replace('_', '-')
    
    # Common tool locations
    search_paths = [
        toolkit_path,  # Root
        os.path.join(toolkit_path, tool_name_lower),
        os.path.join(toolkit_path, tool_name),
    ]
    
    # Search for executable files
    for search_path in search_paths:
        if os.path.exists(search_path):
            # Check if it's a directory with executables
            if os.path.isdir(search_path):
                for item in os.listdir(search_path):
                    item_path = os.path.join(search_path, item)
                    # Check for common executable patterns
                    if os.path.isfile(item_path):
                        if item.lower() == tool_name_lower or item.lower().startswith(tool_name_lower):
                            # Check if it's executable
                            if item.endswith(('.py', '.sh', '.bat', '.exe', '.ps1')) or os.access(item_path, os.X_OK):
                                return item_path
                        # Check for main.py, setup.py, etc.
                        if item.lower() in ['main.py', 'setup.py', 'run.py', 'tool.py']:
                            return item_path
            # Check if it's a file
            elif os.path.isfile(search_path):
                return search_path
    
    return None

def parse_redteam_tools(readme_path):
    """Parse RedTeam-Tools README to extract tool information"""
    tools = []
    current_category = None
    
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse markdown structure - look for tool categories and entries
        lines = content.split('\n')
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for category headers (format: <summary><b>Category Name</b> X tools</summary>)
            if '<summary>' in line and '<b>' in line:
                try:
                    # Extract category name from <summary><b>Category Name</b>
                    b_start = line.find('<b>') + 3
                    b_end = line.find('</b>', b_start)
                    if b_end > b_start:
                        category_match = line[b_start:b_end].strip()
                        # Remove "X tools" or "X tips" suffix if present
                        if ' tools' in category_match:
                            category_match = category_match.split(' tools')[0].strip()
                        elif ' tips' in category_match:
                            category_match = category_match.split(' tips')[0].strip()
                        if category_match:
                            # Skip "Red Team Tips" category - those are tips, not tools
                            if category_match == 'Red Team Tips':
                                current_category = None
                                print(f"[TOOLKIT] Skipping category: Red Team Tips (tips, not tools)")
                            else:
                                current_category = category_match
                                print(f"[TOOLKIT] Found category: {current_category}")
                            i += 1
                            continue
                except Exception as e:
                    print(f"[TOOLKIT] Error parsing category: {e}")
                    pass
            
            # Check for tool entries (format: <li><b><a href="#toolname">toolname</a></b><i> description</i></li>)
            # Also handle: <li><b>toolname</b><i> description</i></li>
            if '<li>' in line and '<b>' in line:
                tool_name = None
                tool_desc = None
                
                # Extract tool name from <a href="#toolname">toolname</a> or <b>toolname</b>
                if '<a href="#' in line:
                    # Format: <a href="#toolname">toolname</a>
                    try:
                        href_start = line.find('<a href="#') + len('<a href="#')
                        href_end = line.find('">', href_start)
                        if href_end > href_start:
                            href_part = line[href_start:href_end]
                            # Get display name from between > and </a>
                            name_start = line.find('">', href_end) + 2
                            name_end = line.find('</a>', name_start)
                            if name_end > name_start:
                                tool_name = line[name_start:name_end].strip()
                            else:
                                # Fallback: convert kebab-case to title case
                                tool_name = href_part.replace('-', ' ').title()
                    except:
                        pass
                
                if not tool_name and '<b>' in line:
                    # Format: <b>toolname</b>
                    try:
                        b_start = line.find('<b>') + 3
                        b_end = line.find('</b>', b_start)
                        if b_end > b_start:
                            name_part = line[b_start:b_end].strip()
                            # Skip if it contains <a tag (already processed)
                            if '<a' not in name_part:
                                tool_name = name_part
                    except:
                        pass
                
                # Extract description from <i>description</i>
                if '<i>' in line:
                    try:
                        i_start = line.find('<i>') + 3
                        i_end = line.find('</i>', i_start)
                        if i_end > i_start:
                            tool_desc = line[i_start:i_end].strip()
                    except:
                        pass
                
                # Skip category headers and invalid entries
                # Don't skip tools - only skip if it's actually a category name (exact match)
                category_names = ['Red Team Tips', 'Reconnaissance', 'Resource Development', 'Initial Access', 'Execution', 'Persistence', 'Privilege Escalation', 'Defense Evasion', 'Credential Access', 'Discovery', 'Lateral Movement', 'Collection', 'Command and Control', 'Exfiltration', 'Impact']
                
                # Only skip if tool_name exactly matches a category name
                # Also skip if current_category is None (we're in "Red Team Tips" or no category set)
                if tool_name and tool_name not in category_names and current_category:
                    # Clean up tool name
                    tool_name = tool_name.strip()
                    if tool_name and len(tool_name) > 0 and current_category:
                        tool_id = tool_name.lower().replace(' ', '-').replace('(', '').replace(')', '').replace("'", '').replace('"', '').replace('/', '-').replace('\\', '-').replace('->', '-').replace('@', '')
                        tools.append({
                            'name': tool_name,
                            'description': tool_desc or 'No description available',
                            'category': current_category,
                            'id': tool_id
                        })
                        if len(tools) % 10 == 0:  # Log every 10 tools to avoid spam
                            print(f"[TOOLKIT] Parsed {len(tools)} tools so far...")
            
            i += 1
        
        print(f"[TOOLKIT] Total tools parsed: {len(tools)}")
        # Count by category
        category_counts = {}
        for tool in tools:
            cat = tool['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        print(f"[TOOLKIT] Tools by category: {category_counts}")
        return tools
    except Exception as e:
        print(f"[TOOLKIT] Error parsing tools: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    port = 5001
    print(f"\n{'='*60}")
    print(f"  Auto_Punch IDE - Starting Server")
    print(f"{'='*60}")
    print(f"\n✓ Server will run on: http://localhost:{port}")
    print(f"✓ Debug mode: ENABLED")
    print(f"✓ Static files: /static/")
    print(f"✓ Templates: /templates/")
    print(f"\n{'='*60}\n")
    
    # Only open browser if not running in Electron (check for Electron environment variable)
    # Electron will handle opening the window itself
    is_electron = os.environ.get('ELECTRON_RUN_AS_NODE') or os.environ.get('FLASK_ENV') == 'production'
    
    def open_browser():
        # Don't open browser if running in Electron
        if is_electron:
            print("✓ Running in Electron - browser will be opened by Electron window")
            return
            
        import time
        time.sleep(2)
        try:
            webbrowser.open(f'http://localhost:{port}')
            print("✓ Browser opened automatically")
        except:
            print("⚠ Could not open browser automatically")
            print(f"  Please navigate to: http://localhost:{port}")
    
    # Only start browser thread if not in Electron
    if not is_electron:
        threading.Thread(target=open_browser, daemon=True).start()
    else:
        print("✓ Electron mode detected - skipping browser auto-open")
    
    # Enable debug mode with detailed logging
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    print("✓ Starting Flask server with debug mode...")
    print("✓ Watch this window for request logs and errors\n")
    
    # Initialize Telegram integration
    if telegram_bot.enabled:
        print("✓ Telegram bot integration enabled")
    else:
        print("⚠ Telegram bot not configured (set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)")
    
    if settings_sync.enabled:
        print("✓ Settings sync enabled")
    else:
        print("⚠ Settings sync not configured (set SUPABASE_URL and SUPABASE_KEY)")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=False, log_output=True)

