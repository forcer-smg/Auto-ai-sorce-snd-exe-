"""
Auto_Punch IDE - Standalone IDE with VS Code + Cursor features
Powered by Auto_Punch Ai as the main agent
"""

import os
import sys
import json
import threading
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import webbrowser

# Add Auto_Punch Ai to path
AUTO_PUNCH_DIR = Path(r"C:\Users\Administrator\Auto_Punch Ai")
sys.path.insert(0, str(AUTO_PUNCH_DIR))

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

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
            'dashboard_fix_agent': dashboard_fix_agent  # Dashboard fix agent
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
workspace_root = os.path.expanduser("~")
current_workspace = None

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
    
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return jsonify({'success': True, 'path': file_path})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
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
- [NMAP: scan 192.168.1.1] or [NMAP: quick 192.168.1.0/24] or [NMAP: vuln target.com]
- [BURP: launch] or [BURP: status]

Or use direct commands:
- git status, git add ., git commit -m "message"
- nmap -sV target.com
- java -jar burpsuite_community.jar
"""
                
                control_info = """
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

[CODE GENERATION & EXECUTION - AUTOMATIC FILE CREATION]
IMPORTANT: When the user asks you to create code or files, you MUST:

1. CREATE FILES AUTOMATICALLY:
   Use this format to create files that will open in the IDE editor:
   [FILE: filename.py]
   ```python
   # Your code here
   print("Hello")
   ```

   OR simply use code blocks - the IDE will auto-detect and create files:
   ```python
   print("Hello World")
   ```

2. EXECUTE TERMINAL COMMANDS:
   Use ```bash or ```shell for terminal commands:
   ```bash
   python script.py
   ```

3. COMBINED WORKFLOW:
   [FILE: hello.py]
   ```python
   print("Hello, World!")
   ```
   
   Then run it:
   ```bash
   python hello.py
   ```

CRITICAL INSTRUCTIONS:
- When user asks for code, ALWAYS create it as a file using [FILE: path] format
- When user asks to run/execute something, use ```bash code blocks
- The IDE automatically detects code blocks and creates files
- Files are automatically opened in the Monaco Editor
- Terminal commands are automatically executed and output shown

Current workspace: """ + str(current_workspace or workspace_root)
            
            enhanced_message = message + control_info
            
            # Get AI response with streaming progress
            emit_progress(session_id, "💭 AI is thinking and generating response...")
            response_text = ""
            chunk_count = 0
            for chunk in hacxgpt.chat(enhanced_message):
                if chunk:
                    response_text += chunk
                    chunk_count += 1
                    if chunk_count % 100 == 0:  # Emit progress every 100 chunks
                        emit_progress(session_id, f"📝 Generated {chunk_count} chunks...")
                    if chunk_count > 10000:
                        break
            
            if response_text:
                print(f"[AI] HacxGPT responded with {len(response_text)} characters")
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
            
            git_commands = re.findall(git_pattern, response_text, re.IGNORECASE)
            nmap_commands = re.findall(nmap_pattern, response_text, re.IGNORECASE)
            burp_commands = re.findall(burp_pattern, response_text, re.IGNORECASE)
            browser_commands = re.findall(browser_pattern, response_text, re.IGNORECASE)
            
            print(f"[AI PARSING] Found: {len(commands_to_execute)} commands, {len(code_blocks)} terminal blocks, {len(file_operations)} file ops, {len(create_files)} creates, {len(write_files)} writes, {len(auto_detected_files)} auto-detected files")
            if auto_detected_files:
                print(f"[AI PARSING] Auto-detected files: {[f[0] for f in auto_detected_files]}")
            
            execution_results = []
            execution_log = []
            security_toolkit = auto_punch_components.get('security_toolkit')
            
            # Execute Git commands
            if git_commands and security_toolkit:
                emit_progress(session_id, f"🔧 Executing {len(git_commands)} Git command(s)...")
                for action, params in git_commands:
                    try:
                        print(f"[AI CONTROL] Executing Git: {action} {params or ''}")
                        emit_progress(session_id, f"🔧 Git {action}: {params or ''}")
                        execution_log.append(f"🔧 Git {action}: {params or ''}")
                        
                        # Parse params
                        kwargs = {}
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
                        
                        result = security_toolkit.execute_command('git', action, **kwargs)
                        if result.get('success'):
                            output = result.get('output', 'Success')
                            execution_results.append(f"✅ Git {action}: {output[:200]}")
                            execution_log.append(f"✅ Git {action} completed")
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
                        
                        # Resolve file path relative to workspace
                        if not os.path.isabs(file_path):
                            file_path = os.path.join(current_workspace or workspace_root, file_path)
                        
                        print(f"[AI CONTROL] Creating file: {file_path} (language: {language})")
                        print(f"[AI CONTROL] File content preview: {code_content[:100]}...")
                        emit_progress(session_id, f"📝 Creating: {os.path.basename(file_path)}")
                        execution_log.append(f"📝 Creating file: {file_path}")
                        
                        # Write file
                        try:
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(code_content)
                            print(f"[AI CONTROL] File written successfully: {file_path}")
                        except Exception as write_error:
                            print(f"[AI CONTROL] File write error: {write_error}")
                            raise
                        
                        files_created.append({'path': file_path, 'language': language})
                        execution_results.append(f"✅ File created: {file_path}")
                        execution_log.append(f"✅ File created successfully")
                        
                        # Emit to frontend to open file in editor
                        print(f"[AI CONTROL] Emitting open_file_in_editor event for: {file_path}")
                        socketio.emit('open_file_in_editor', {
                            'path': file_path,
                            'content': code_content,
                            'language': language
                        })
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
                        execution_log.append(f"🔧 Executing: {cmd_clean}")
                        
                        result = automation.execute_terminal_command(cmd_clean, realtime=False)
                        if result:
                            output = result.get('output', 'Executed')
                            if isinstance(output, list):
                                output = '\n'.join(str(line) for line in output)
                            execution_results.append(f"✅ Command '{cmd_clean}':\n{output}")
                            execution_log.append(f"✅ Result: {output[:100]}...")
                            
                            # Emit terminal output to frontend
                            socketio.emit('terminal_output', {'output': output})
                    except Exception as e:
                        error_msg = str(e)
                        execution_results.append(f"❌ Command '{cmd}' error: {error_msg}")
                        execution_log.append(f"❌ Error: {error_msg}")
            
            # Execute code blocks in terminal
            if code_blocks and automation and automation.is_available():
                emit_progress(session_id, f"💻 Executing {len(code_blocks)} code block(s) in terminal...")
                # Emit command to show terminal panel
                socketio.emit('show_terminal', {})
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
                        execution_log.append(f"💻 Executing code: {code_clean[:50]}...")
                        
                        # Show command in terminal (like Cursor AI)
                        socketio.emit('terminal_output', {'output': f'\n$ {code_clean}\n'})
                        
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
    """Execute terminal command with live output"""
    data = request.json
    command = data.get('command')
    working_dir = data.get('working_dir', current_workspace or workspace_root)
    
    if not command:
        return jsonify({'error': 'No command provided', 'output': 'Error: No command provided'}), 400
    
    # Try automation first
    if auto_punch_components.get('automation_enabled'):
        try:
            automation = auto_punch_components['automation']
            if working_dir:
                automation.set_working_directory(working_dir)
            
            # For batch files on Windows, ensure they run in integrated terminal (no new window)
            if os.name == 'nt' and (command.strip().endswith('.bat') or command.strip().endswith('.cmd')):
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
            # Fall through to subprocess fallback
    
    # Fallback: Use subprocess directly
    try:
        import subprocess
        import os
        
        # Set working directory
        if working_dir and os.path.exists(working_dir):
            os.chdir(working_dir)
        
        # Execute command
        if os.name == 'nt':  # Windows
            # For batch files, use cmd.exe /c to run in same process and capture output
            if command.strip().endswith('.bat') or command.strip().endswith('.cmd'):
                # Ensure batch file runs in same console, not new window
                if not command.strip().startswith('cmd'):
                    command = f'cmd /c "{command}"'
            
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=working_dir if working_dir else None,
                # Don't create new console window - capture output instead
                creationflags=0  # Remove CREATE_NEW_CONSOLE if it was set
            )
        else:  # Unix/Linux
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=working_dir if working_dir else None
            )
        
        output = result.stdout
        if result.stderr:
            output += '\n' + result.stderr
        
        return jsonify({
            'success': result.returncode == 0,
            'output': output or 'Command executed (no output)',
            'exit_code': result.returncode,
            'command': command
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'error': 'Command timed out',
            'output': 'Error: Command execution timed out after 30 seconds'
        }), 500
    except Exception as e:
        print(f"[TERMINAL ERROR] Subprocess error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': str(e),
            'output': f'Error executing command: {str(e)}'
        }), 500

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
        
        else:
            return jsonify({'error': f'Unknown action: {action}'}), 400
            
    except Exception as e:
        print(f"[ERROR] AI execute error: {e}")
        import traceback
        traceback.print_exc()
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

@socketio.on('connect')
def handle_connect():
    session_id = request.sid
    active_sessions[session_id] = {'connected': True}
    emit('connected', {'message': 'Connected to Auto_Punch IDE', 'session_id': session_id})

@socketio.on('disconnect')
def handle_disconnect():
    session_id = request.sid
    if session_id in active_sessions:
        del active_sessions[session_id]

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
    
    def open_browser():
        import time
        time.sleep(2)
        try:
            webbrowser.open(f'http://localhost:{port}')
            print("✓ Browser opened automatically")
        except:
            print("⚠ Could not open browser automatically")
            print(f"  Please navigate to: http://localhost:{port}")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    # Enable debug mode with detailed logging
    app.config['DEBUG'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    print("✓ Starting Flask server with debug mode...")
    print("✓ Watch this window for request logs and errors\n")
    
    socketio.run(app, host='0.0.0.0', port=port, debug=True, use_reloader=False, log_output=True)

