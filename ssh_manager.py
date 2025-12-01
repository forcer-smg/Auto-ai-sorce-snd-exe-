"""
SSH Connection Manager for Auto_Punch IDE
Manages SSH connections, sessions, and remote terminal access
"""

import os
import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional
import subprocess
import threading

try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    print("⚠ paramiko not installed. SSH functionality will be limited. Install with: pip install paramiko")

class SSHManager:
    """Manages SSH connections"""
    
    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = os.path.join(os.path.dirname(__file__), 'ssh_connections.json')
        self.config_file = Path(config_file)
        self.connections = {}
        self.active_sessions = {}  # connection_id -> paramiko.SSHClient
        self.load_connections()
    
    def load_connections(self):
        """Load saved SSH connections from file"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.connections = data.get('connections', {})
            except Exception as e:
                print(f"Error loading SSH connections: {e}")
                self.connections = {}
        else:
            self.connections = {}
    
    def save_connections(self):
        """Save SSH connections to file"""
        try:
            data = {'connections': self.connections}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving SSH connections: {e}")
    
    def add_connection(self, name: str, host: str, port: int, username: str, 
                      auth_method: str, password: str = None, key_path: str = None, 
                      key_passphrase: str = None) -> Dict:
        """Add a new SSH connection"""
        connection_id = str(uuid.uuid4())
        
        connection = {
            'id': connection_id,
            'name': name,
            'host': host,
            'port': port,
            'username': username,
            'auth_method': auth_method,
            'password': password,  # In production, encrypt this
            'key_path': key_path,
            'key_passphrase': key_passphrase,  # In production, encrypt this
            'connected': False
        }
        
        self.connections[connection_id] = connection
        self.save_connections()
        
        return {'success': True, 'connection_id': connection_id, 'connection': connection}
    
    def list_connections(self) -> List[Dict]:
        """List all SSH connections"""
        connections_list = []
        for conn_id, conn in self.connections.items():
            # Don't send sensitive data in response
            safe_conn = conn.copy()
            if 'password' in safe_conn:
                safe_conn['password'] = '***' if safe_conn['password'] else None
            if 'key_passphrase' in safe_conn:
                safe_conn['key_passphrase'] = '***' if safe_conn['key_passphrase'] else None
            safe_conn['connected'] = conn_id in self.active_sessions
            connections_list.append(safe_conn)
        return connections_list
    
    def get_connection(self, connection_id: str) -> Optional[Dict]:
        """Get connection by ID"""
        return self.connections.get(connection_id)
    
    def connect(self, connection_id: str) -> Dict:
        """Connect to SSH server"""
        if not PARAMIKO_AVAILABLE:
            return {'success': False, 'error': 'paramiko library not installed. Install with: pip install paramiko'}
        
        connection = self.connections.get(connection_id)
        if not connection:
            return {'success': False, 'error': 'Connection not found'}
        
        if connection_id in self.active_sessions:
            return {'success': True, 'message': 'Already connected'}
        
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # Connect based on auth method
            if connection['auth_method'] == 'password':
                client.connect(
                    hostname=connection['host'],
                    port=connection['port'],
                    username=connection['username'],
                    password=connection.get('password'),
                    timeout=10
                )
            elif connection['auth_method'] == 'key':
                key_path = connection.get('key_path')
                key_passphrase = connection.get('key_passphrase')
                
                if not key_path or not os.path.exists(key_path):
                    return {'success': False, 'error': f'Private key file not found: {key_path}'}
                
                # Try to load key with different methods
                private_key = None
                key_errors = []
                
                # Try RSA key first
                try:
                    private_key = paramiko.RSAKey.from_private_key_file(
                        key_path, 
                        password=key_passphrase if key_passphrase else None
                    )
                except Exception as e:
                    key_errors.append(f"RSA: {str(e)}")
                
                # Try Ed25519 key
                if not private_key:
                    try:
                        private_key = paramiko.Ed25519Key.from_private_key_file(
                            key_path,
                            password=key_passphrase if key_passphrase else None
                        )
                    except Exception as e:
                        key_errors.append(f"Ed25519: {str(e)}")
                
                # Try ECDSA key
                if not private_key:
                    try:
                        private_key = paramiko.ECDSAKey.from_private_key_file(
                            key_path,
                            password=key_passphrase if key_passphrase else None
                        )
                    except Exception as e:
                        key_errors.append(f"ECDSA: {str(e)}")
                
                # Try DSA key (legacy)
                if not private_key:
                    try:
                        private_key = paramiko.DSSKey.from_private_key_file(
                            key_path,
                            password=key_passphrase if key_passphrase else None
                        )
                    except Exception as e:
                        key_errors.append(f"DSA: {str(e)}")
                
                # Try loading as OpenSSH format (auto-detect)
                if not private_key:
                    try:
                        # paramiko can auto-detect key type from OpenSSH format
                        private_key = paramiko.RSAKey.from_private_key_file(
                            key_path,
                            password=key_passphrase if key_passphrase else None
                        )
                    except:
                        try:
                            # Try with empty passphrase
                            private_key = paramiko.RSAKey.from_private_key_file(key_path, password='')
                        except:
                            pass
                
                if not private_key:
                    error_msg = f"Failed to load private key. Tried: {', '.join(key_errors)}"
                    if key_passphrase:
                        error_msg += "\nNote: If key is encrypted, ensure passphrase is correct."
                    return {'success': False, 'error': error_msg}
                
                client.connect(
                    hostname=connection['host'],
                    port=connection['port'],
                    username=connection['username'],
                    pkey=private_key,
                    timeout=10,
                    allow_agent=False,
                    look_for_keys=False
                )
            else:
                return {'success': False, 'error': 'Invalid auth method'}
            
            self.active_sessions[connection_id] = client
            connection['connected'] = True
            
            return {'success': True, 'message': 'Connected successfully'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def disconnect(self, connection_id: str) -> Dict:
        """Disconnect from SSH server"""
        if connection_id in self.active_sessions:
            try:
                self.active_sessions[connection_id].close()
            except:
                pass
            del self.active_sessions[connection_id]
        
        connection = self.connections.get(connection_id)
        if connection:
            connection['connected'] = False
        
        return {'success': True}
    
    def execute_command(self, connection_id: str, command: str) -> Dict:
        """Execute command on remote server"""
        if connection_id not in self.active_sessions:
            return {'success': False, 'error': 'Not connected'}
        
        try:
            client = self.active_sessions[connection_id]
            stdin, stdout, stderr = client.exec_command(command)
            
            output = stdout.read().decode('utf-8', errors='ignore')
            error = stderr.read().decode('utf-8', errors='ignore')
            exit_code = stdout.channel.recv_exit_status()
            
            return {
                'success': True,
                'output': output,
                'error': error,
                'exit_code': exit_code
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def delete_connection(self, connection_id: str) -> Dict:
        """Delete SSH connection"""
        # Disconnect if connected
        if connection_id in self.active_sessions:
            self.disconnect(connection_id)
        
        if connection_id in self.connections:
            del self.connections[connection_id]
            self.save_connections()
            return {'success': True}
        
        return {'success': False, 'error': 'Connection not found'}

