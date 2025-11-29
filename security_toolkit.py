"""
Security Toolkit Integration for Auto_Punch IDE
Provides full AI control over: Git, Nmap, Burp Suite Community Edition
"""

import subprocess
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import platform


class GitOperations:
    """Enhanced Git operations with full AI control"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.git_available = self._check_git_installed()
    
    def _check_git_installed(self) -> bool:
        """Check if Git is installed"""
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def execute_git_command(self, command: str, args: List[str] = None) -> Dict[str, Any]:
        """Execute any Git command with full control"""
        if not self.git_available:
            return {
                'success': False,
                'error': 'Git is not installed or not in PATH'
            }
        
        args = args or []
        full_command = ['git', command] + args
        
        try:
            result = subprocess.run(
                full_command,
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr if result.returncode != 0 else None,
                'exit_code': result.returncode,
                'command': ' '.join(full_command)
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Git command timed out after 60 seconds'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def status(self) -> Dict[str, Any]:
        """Get Git status"""
        return self.execute_git_command('status', ['--porcelain'])
    
    def add(self, files: List[str] = None) -> Dict[str, Any]:
        """Stage files for commit"""
        args = files if files else ['.']
        return self.execute_git_command('add', args)
    
    def commit(self, message: str, files: List[str] = None) -> Dict[str, Any]:
        """Commit changes"""
        if files:
            self.add(files)
        return self.execute_git_command('commit', ['-m', message])
    
    def push(self, remote: str = 'origin', branch: str = None) -> Dict[str, Any]:
        """Push to remote"""
        args = [remote]
        if branch:
            args.append(branch)
        return self.execute_git_command('push', args)
    
    def pull(self, remote: str = 'origin', branch: str = None) -> Dict[str, Any]:
        """Pull from remote"""
        args = []
        if remote and branch:
            args.extend([remote, branch])
        return self.execute_git_command('pull', args)
    
    def clone(self, repo_url: str, destination: str = None) -> Dict[str, Any]:
        """Clone a repository"""
        args = [repo_url]
        if destination:
            args.append(destination)
        return self.execute_git_command('clone', args)
    
    def branch(self, action: str = 'list', name: str = None) -> Dict[str, Any]:
        """Branch operations"""
        if action == 'list':
            return self.execute_git_command('branch', ['-a'])
        elif action == 'create' and name:
            return self.execute_git_command('checkout', ['-b', name])
        elif action == 'delete' and name:
            return self.execute_git_command('branch', ['-d', name])
        elif action == 'switch' and name:
            return self.execute_git_command('checkout', [name])
        else:
            return {'success': False, 'error': 'Invalid branch action'}
    
    def log(self, limit: int = 10, format: str = 'oneline') -> Dict[str, Any]:
        """Get commit log"""
        args = [f'-{limit}']
        if format == 'oneline':
            args.append('--oneline')
        return self.execute_git_command('log', args)
    
    def diff(self, file: str = None) -> Dict[str, Any]:
        """Get diff"""
        args = []
        if file:
            args.append(file)
        return self.execute_git_command('diff', args)


class NmapScanner:
    """Nmap integration with full AI control"""
    
    def __init__(self):
        self.nmap_available = self._check_nmap_installed()
        self.nmap_path = self._find_nmap_path()
    
    def _check_nmap_installed(self) -> bool:
        """Check if Nmap is installed"""
        try:
            result = subprocess.run(
                ['nmap', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def _find_nmap_path(self) -> Optional[str]:
        """Find Nmap installation path"""
        if self.nmap_available:
            return 'nmap'
        
        # Common Windows installation paths
        if platform.system() == 'Windows':
            common_paths = [
                r'C:\Program Files (x86)\Nmap\nmap.exe',
                r'C:\Program Files\Nmap\nmap.exe',
                r'C:\Nmap\nmap.exe',
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        return None
    
    def scan(self, target: str, options: List[str] = None, output_format: str = 'text') -> Dict[str, Any]:
        """
        Execute Nmap scan with full control
        
        Args:
            target: IP address, hostname, or CIDR range
            options: List of Nmap options (e.g., ['-sS', '-p', '80,443', '-A'])
            output_format: 'text', 'json', or 'xml'
        """
        if not self.nmap_available and not self.nmap_path:
            return {
                'success': False,
                'error': 'Nmap is not installed. Please install Nmap first.'
            }
        
        options = options or ['-sV']  # Default: version detection
        
        # Build command
        cmd = [self.nmap_path or 'nmap', target] + options
        
        # Add output format
        if output_format == 'json':
            cmd.extend(['-oJ', '-'])
        elif output_format == 'xml':
            cmd.extend(['-oX', '-'])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for scans
            )
            
            return {
                'success': result.returncode == 0 or result.returncode == 1,  # Nmap returns 1 for some scans
                'output': result.stdout,
                'error': result.stderr if result.stderr else None,
                'exit_code': result.returncode,
                'command': ' '.join(cmd),
                'format': output_format
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Nmap scan timed out after 5 minutes'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def quick_scan(self, target: str) -> Dict[str, Any]:
        """Quick scan (top 1000 ports)"""
        return self.scan(target, ['-F'])
    
    def full_scan(self, target: str) -> Dict[str, Any]:
        """Full scan (all ports)"""
        return self.scan(target, ['-p-'])
    
    def stealth_scan(self, target: str) -> Dict[str, Any]:
        """Stealth SYN scan"""
        return self.scan(target, ['-sS', '-p', '1-1000'])
    
    def version_scan(self, target: str, ports: str = None) -> Dict[str, Any]:
        """Version detection scan"""
        options = ['-sV']
        if ports:
            options.extend(['-p', ports])
        return self.scan(target, options)
    
    def os_detection(self, target: str) -> Dict[str, Any]:
        """OS detection scan"""
        return self.scan(target, ['-O'])
    
    def vulnerability_scan(self, target: str) -> Dict[str, Any]:
        """Vulnerability scan with NSE scripts"""
        return self.scan(target, ['-sV', '--script', 'vuln'])


class BurpSuiteIntegration:
    """Burp Suite Community Edition integration"""
    
    def __init__(self):
        self.burp_available = self._check_burp_installed()
        self.burp_path = self._find_burp_path()
        self.burp_api_url = None  # For future API integration
    
    def _check_burp_installed(self) -> bool:
        """Check if Burp Suite is installed"""
        return self._find_burp_path() is not None
    
    def _find_burp_path(self) -> Optional[str]:
        """Find Burp Suite installation path"""
        if platform.system() == 'Windows':
            common_paths = [
                r'C:\Program Files\BurpSuiteCommunity\burpsuite_community.jar',
                r'C:\Program Files (x86)\BurpSuiteCommunity\burpsuite_community.jar',
                r'C:\BurpSuiteCommunity\burpsuite_community.jar',
                os.path.expanduser(r'~\AppData\Local\Programs\BurpSuiteCommunity\burpsuite_community.jar'),
            ]
            for path in common_paths:
                if os.path.exists(path):
                    return path
        
        # Check if Java is available
        try:
            subprocess.run(['java', '-version'], capture_output=True, timeout=5)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        
        return None
    
    def launch(self, project_file: str = None, headless: bool = False) -> Dict[str, Any]:
        """
        Launch Burp Suite Community Edition
        
        Args:
            project_file: Optional project file to load
            headless: Run in headless mode (requires Burp Suite Pro with API)
        """
        if not self.burp_available:
            return {
                'success': False,
                'error': 'Burp Suite Community Edition is not installed. Please install it first.'
            }
        
        if not self.burp_path:
            return {
                'success': False,
                'error': 'Burp Suite installation not found'
            }
        
        # Check Java
        try:
            java_check = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if java_check.returncode != 0:
                return {
                    'success': False,
                    'error': 'Java is required to run Burp Suite. Please install Java first.'
                }
        except FileNotFoundError:
            return {
                'success': False,
                'error': 'Java is not installed. Please install Java to run Burp Suite.'
            }
        
        # Build command
        cmd = ['java', '-jar', self.burp_path]
        
        if project_file and os.path.exists(project_file):
            cmd.extend(['--project-file', project_file])
        
        try:
            if headless:
                # Headless mode (requires Burp Suite Pro API)
                return {
                    'success': False,
                    'error': 'Headless mode requires Burp Suite Professional with API access. Community Edition runs in GUI mode only.'
                }
            else:
                # Launch in GUI mode (non-blocking)
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == 'Windows' else 0
                )
                
                return {
                    'success': True,
                    'message': 'Burp Suite Community Edition launched successfully',
                    'pid': process.pid,
                    'command': ' '.join(cmd)
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def check_installation(self) -> Dict[str, Any]:
        """Check Burp Suite installation status"""
        return {
            'installed': self.burp_available,
            'path': self.burp_path,
            'java_available': self._check_java(),
            'message': 'Burp Suite Community Edition is ready' if self.burp_available else 'Burp Suite not found'
        }
    
    def _check_java(self) -> bool:
        """Check if Java is installed"""
        try:
            result = subprocess.run(
                ['java', '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False


class SecurityToolkit:
    """Main security toolkit interface for AI control"""
    
    def __init__(self, workspace_path: Optional[str] = None):
        self.workspace_path = workspace_path or os.getcwd()
        self.git = GitOperations(workspace_path)
        self.nmap = NmapScanner()
        self.burp = BurpSuiteIntegration()
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of all tools"""
        return {
            'git': {
                'available': self.git.git_available,
                'workspace': self.workspace_path
            },
            'nmap': {
                'available': self.nmap.nmap_available,
                'path': self.nmap.nmap_path
            },
            'burp_suite': self.burp.check_installation()
        }
    
    def execute_command(self, tool: str, action: str, **kwargs) -> Dict[str, Any]:
        """
        Unified command interface for all tools
        
        Args:
            tool: 'git', 'nmap', or 'burp'
            action: Tool-specific action
            **kwargs: Tool-specific parameters
        """
        if tool == 'git':
            return self._execute_git(action, **kwargs)
        elif tool == 'nmap':
            return self._execute_nmap(action, **kwargs)
        elif tool == 'burp':
            return self._execute_burp(action, **kwargs)
        else:
            return {
                'success': False,
                'error': f'Unknown tool: {tool}'
            }
    
    def _execute_git(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute Git command"""
        if action == 'status':
            return self.git.status()
        elif action == 'add':
            return self.git.add(kwargs.get('files'))
        elif action == 'commit':
            return self.git.commit(kwargs.get('message', ''), kwargs.get('files'))
        elif action == 'push':
            return self.git.push(kwargs.get('remote', 'origin'), kwargs.get('branch'))
        elif action == 'pull':
            return self.git.pull(kwargs.get('remote', 'origin'), kwargs.get('branch'))
        elif action == 'clone':
            return self.git.clone(kwargs.get('repo_url', ''), kwargs.get('destination'))
        elif action == 'branch':
            return self.git.branch(kwargs.get('action', 'list'), kwargs.get('name'))
        elif action == 'log':
            return self.git.log(kwargs.get('limit', 10), kwargs.get('format', 'oneline'))
        elif action == 'diff':
            return self.git.diff(kwargs.get('file'))
        elif action == 'command':
            # Direct command execution
            return self.git.execute_git_command(
                kwargs.get('command', ''),
                kwargs.get('args', [])
            )
        else:
            return {'success': False, 'error': f'Unknown Git action: {action}'}
    
    def _execute_nmap(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute Nmap command"""
        target = kwargs.get('target', '')
        if not target:
            return {'success': False, 'error': 'Target is required for Nmap scans'}
        
        if action == 'scan':
            return self.nmap.scan(
                target,
                kwargs.get('options'),
                kwargs.get('format', 'text')
            )
        elif action == 'quick':
            return self.nmap.quick_scan(target)
        elif action == 'full':
            return self.nmap.full_scan(target)
        elif action == 'stealth':
            return self.nmap.stealth_scan(target)
        elif action == 'version':
            return self.nmap.version_scan(target, kwargs.get('ports'))
        elif action == 'os':
            return self.nmap.os_detection(target)
        elif action == 'vuln':
            return self.nmap.vulnerability_scan(target)
        else:
            return {'success': False, 'error': f'Unknown Nmap action: {action}'}
    
    def _execute_burp(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute Burp Suite command"""
        if action == 'launch':
            return self.burp.launch(
                kwargs.get('project_file'),
                kwargs.get('headless', False)
            )
        elif action == 'status':
            return self.burp.check_installation()
        else:
            return {'success': False, 'error': f'Unknown Burp action: {action}'}

