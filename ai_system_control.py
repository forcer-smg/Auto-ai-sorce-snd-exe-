"""
AI System Control Module
Gives AI full control over the system
"""

import os
import sys
from pathlib import Path

class AISystemControl:
    """Gives AI full system control capabilities"""
    
    def __init__(self, automation, code_analyzer, todo_manager, git_operations, pc_controller):
        self.automation = automation
        self.code_analyzer = code_analyzer
        self.todo_manager = todo_manager
        self.git_operations = git_operations
        self.pc_controller = pc_controller
    
    def execute_command(self, command: str, working_dir: str = None):
        """Execute any terminal command"""
        if not self.automation or not self.automation.is_available():
            return {'success': False, 'error': 'Automation not available'}
        
        try:
            if working_dir:
                self.automation.set_working_directory(working_dir)
            result = self.automation.execute_terminal_command(command, realtime=False)
            return result
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def read_file(self, file_path: str):
        """Read any file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return {'success': True, 'content': f.read()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def write_file(self, file_path: str, content: str):
        """Write/create any file"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {'success': True, 'message': f'File written: {file_path}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_file(self, file_path: str):
        """Delete any file"""
        try:
            if os.path.exists(file_path):
                if os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                return {'success': True, 'message': f'Deleted: {file_path}'}
            return {'success': False, 'error': 'File not found'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_code(self, file_path: str):
        """Analyze code"""
        if not self.code_analyzer:
            return {'success': False, 'error': 'Code analyzer not available'}
        try:
            return self.code_analyzer.analyze_file(file_path)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def fix_code(self, file_path: str):
        """Fix code"""
        if not self.code_analyzer:
            return {'success': False, 'error': 'Code analyzer not available'}
        try:
            return self.code_analyzer.fix_file(file_path)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def system_info(self):
        """Get system information"""
        if not self.pc_controller:
            return {'success': False, 'error': 'PC controller not available'}
        try:
            return self.pc_controller.get_system_info()
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def git_status(self):
        """Get git status"""
        if not self.git_operations:
            return {'success': False, 'error': 'Git operations not available'}
        try:
            return self.git_operations.status()
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def git_commit(self, message: str):
        """Git commit"""
        if not self.git_operations:
            return {'success': False, 'error': 'Git operations not available'}
        try:
            return self.git_operations.commit(message)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def add_todo(self, content: str):
        """Add todo"""
        if not self.todo_manager:
            return {'success': False, 'error': 'Todo manager not available'}
        try:
            todo = self.todo_manager.add_todo(content)
            return {'success': True, 'todo': todo}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def list_todos(self, status: str = None):
        """List todos"""
        if not self.todo_manager:
            return {'success': False, 'error': 'Todo manager not available'}
        try:
            todos = self.todo_manager.list_todos(status=status)
            return {'success': True, 'todos': todos or []}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def git_command(self, action: str, **kwargs):
        """Execute Git command via Security Toolkit"""
        if not self.security_toolkit:
            return {'success': False, 'error': 'Security toolkit not available'}
        try:
            return self.security_toolkit.execute_command('git', action, **kwargs)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def nmap_scan(self, action: str, **kwargs):
        """Execute Nmap scan via Security Toolkit"""
        if not self.security_toolkit:
            return {'success': False, 'error': 'Security toolkit not available'}
        try:
            return self.security_toolkit.execute_command('nmap', action, **kwargs)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def burp_suite(self, action: str, **kwargs):
        """Execute Burp Suite command via Security Toolkit"""
        if not self.security_toolkit:
            return {'success': False, 'error': 'Security toolkit not available'}
        try:
            return self.security_toolkit.execute_command('burp', action, **kwargs)
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def toolkit_status(self):
        """Get security toolkit status"""
        if not self.security_toolkit:
            return {'success': False, 'error': 'Security toolkit not available'}
        try:
            return {'success': True, 'status': self.security_toolkit.get_status()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def browser_navigate(self, url: str):
        """Navigate browser preview to a URL."""
        try:
            import requests
            response = requests.post('http://localhost:5001/api/browser/navigate', 
                                   json={'url': url},
                                   timeout=5)
            return response.json()
        except Exception as e:
            return {'success': False, 'error': f'Browser navigation failed: {str(e)}'}
    
    def browser_screenshot(self):
        """Take a screenshot of the browser preview."""
        try:
            import requests
            response = requests.get('http://localhost:5001/api/browser/screenshot', timeout=5)
            return response.json()
        except Exception as e:
            return {'success': False, 'error': f'Browser screenshot failed: {str(e)}'}
    
    def browser_get_url(self):
        """Get the current URL of the browser preview."""
        try:
            import requests
            response = requests.get('http://localhost:5001/api/browser/url', timeout=5)
            return response.json()
        except Exception as e:
            return {'success': False, 'error': f'Get browser URL failed: {str(e)}'}
    
    def browser_execute_script(self, script: str):
        """Execute JavaScript in the browser preview."""
        try:
            import requests
            response = requests.post('http://localhost:5001/api/browser/execute',
                                   json={'script': script},
                                   timeout=5)
            return response.json()
        except Exception as e:
            return {'success': False, 'error': f'Browser script execution failed: {str(e)}'}

