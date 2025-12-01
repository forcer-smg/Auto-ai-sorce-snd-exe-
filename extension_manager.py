"""
Extension Manager for Auto_Punch IDE
Manages installation, loading, and execution of extensions
"""

import os
import json
import shutil
import zipfile
import requests
from pathlib import Path
from typing import Dict, List, Optional

class ExtensionManager:
    """Manages IDE extensions"""
    
    def __init__(self, extensions_dir: str = None):
        if extensions_dir is None:
            extensions_dir = os.path.join(os.path.dirname(__file__), 'extensions')
        self.extensions_dir = Path(extensions_dir)
        self.extensions_dir.mkdir(exist_ok=True)
        self.extensions = {}
        self.load_extensions()
    
    def load_extensions(self):
        """Load all installed extensions"""
        self.extensions = {}
        if not self.extensions_dir.exists():
            return
        
        for ext_dir in self.extensions_dir.iterdir():
            if ext_dir.is_dir():
                manifest_path = ext_dir / 'package.json'
                if manifest_path.exists():
                    try:
                        with open(manifest_path, 'r', encoding='utf-8') as f:
                            manifest = json.load(f)
                            ext_id = manifest.get('name', ext_dir.name)
                            self.extensions[ext_id] = {
                                'id': ext_id,
                                'path': str(ext_dir),
                                'manifest': manifest,
                                'enabled': True
                            }
                    except Exception as e:
                        print(f"Error loading extension {ext_dir.name}: {e}")
    
    def list_extensions(self) -> List[Dict]:
        """List all installed extensions"""
        return list(self.extensions.values())
    
    def get_extension(self, extension_id: str) -> Optional[Dict]:
        """Get extension by ID"""
        return self.extensions.get(extension_id)
    
    def install_from_marketplace(self, extension_id: str, version: str = None) -> Dict:
        """Install extension from marketplace (VS Code compatible)"""
        try:
            # VS Code Marketplace API
            marketplace_url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
            
            # Parse extension ID (format: publisher.extension-name or just extension-name)
            if '.' in extension_id:
                publisher, ext_name = extension_id.split('.', 1)
            else:
                # Try to find by name only
                publisher = None
                ext_name = extension_id
            
            # Query extension
            if publisher:
                # Search by full ID
                payload = {
                    "filters": [{
                        "criteria": [
                            {"filterType": 7, "value": extension_id}
                        ]
                    }],
                    "flags": 0x200
                }
            else:
                # Search by name
                payload = {
                    "filters": [{
                        "criteria": [
                            {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                            {"filterType": 10, "value": ext_name}
                        ],
                        "pageNumber": 1,
                        "pageSize": 1
                    }],
                    "flags": 0x200
                }
            
            response = requests.post(
                marketplace_url,
                json=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                return {'success': False, 'error': f'Marketplace API error: {response.status_code}'}
            
            data = response.json()
            if not data.get('results') or not data['results'][0].get('extensions'):
                return {'success': False, 'error': 'Extension not found in marketplace'}
            
            extension_data = data['results'][0]['extensions'][0]
            versions = extension_data.get('versions', [])
            
            if not versions:
                return {'success': False, 'error': 'No versions available'}
            
            # Get latest or specified version
            target_version = versions[0] if not version else next(
                (v for v in versions if v.get('version') == version), versions[0]
            )
            
            # Download extension
            asset_uri = target_version.get('assetUri', '')
            if not asset_uri:
                return {'success': False, 'error': 'No download URL available'}
            
            download_url = asset_uri + '/Microsoft.VisualStudio.Services.VSIXPackage'
            
            # Use the proper extension ID from marketplace
            proper_id = extension_data.get('extensionId') or extension_id
            
            return self.install_from_url(download_url, proper_id)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    def install_from_url(self, url: str, extension_id: str = None, progress_callback=None) -> Dict:
        """Install extension from URL (VSIX file) with progress tracking"""
        try:
            # Download VSIX file with progress
            response = requests.get(url, timeout=60, stream=True)
            if response.status_code != 200:
                return {'success': False, 'error': f'Download failed: {response.status_code}'}
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            # Save to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.vsix') as tmp_file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        tmp_file.write(chunk)
                        downloaded += len(chunk)
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress, f'Downloading: {downloaded}/{total_size} bytes')
                tmp_path = tmp_file.name
            
            if progress_callback:
                progress_callback(100, 'Download complete, installing...')
            
            # Install from file
            result = self.install_from_file(tmp_path, extension_id)
            
            if progress_callback and result.get('success'):
                progress_callback(100, 'Installation complete!')
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def install_from_file(self, vsix_path: str, extension_id: str = None) -> Dict:
        """Install extension from VSIX file"""
        try:
            # Extract VSIX (it's a ZIP file) to temp directory first
            import tempfile
            temp_dir = Path(tempfile.mkdtemp())
            
            with zipfile.ZipFile(vsix_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Read manifest - check common locations
            manifest_path = None
            for possible_path in [
                temp_dir / 'extension' / 'package.json',
                temp_dir / 'package.json',
                temp_dir / list(temp_dir.iterdir())[0] / 'package.json' if list(temp_dir.iterdir()) else None
            ]:
                if possible_path and possible_path.exists():
                    manifest_path = possible_path
                    break
            
            if not manifest_path or not manifest_path.exists():
                # Cleanup
                shutil.rmtree(temp_dir)
                return {'success': False, 'error': 'Invalid extension: no package.json found'}
            
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            # Get proper extension ID from manifest
            publisher = manifest.get('publisher', '')
            name = manifest.get('name', '')
            ext_id = f"{publisher}.{name}" if publisher and name else (extension_id or name or 'unknown')
            
            # Final extension directory
            final_dir = self.extensions_dir / ext_id
            if final_dir.exists():
                shutil.rmtree(final_dir)
            
            # Move extension content to final location
            # Find the actual extension root (where package.json is)
            ext_root = manifest_path.parent
            
            # Create final directory
            final_dir.mkdir(parents=True, exist_ok=True)
            
            if ext_root == temp_dir:
                # package.json is at root, copy everything
                for item in temp_dir.iterdir():
                    if item.name != '__pycache__':
                        if item.is_dir():
                            shutil.copytree(str(item), str(final_dir / item.name), dirs_exist_ok=True)
                        else:
                            shutil.copy2(str(item), str(final_dir / item.name))
            else:
                # package.json is in a subdirectory, copy that subdirectory's contents
                for item in ext_root.iterdir():
                    if item.name != '__pycache__':
                        if item.is_dir():
                            shutil.copytree(str(item), str(final_dir / item.name), dirs_exist_ok=True)
                        else:
                            shutil.copy2(str(item), str(final_dir / item.name))
            
            # Cleanup temp directory
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            
            # Load extension
            self.extensions[ext_id] = {
                'id': ext_id,
                'path': str(final_dir),
                'manifest': manifest,
                'enabled': True
            }
            
            # Cleanup temp file
            if os.path.exists(vsix_path) and os.path.isfile(vsix_path):
                try:
                    os.remove(vsix_path)
                except:
                    pass
            
            return {
                'success': True,
                'extension': self.extensions[ext_id],
                'message': f'Extension {ext_id} installed successfully'
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    def uninstall_extension(self, extension_id: str) -> Dict:
        """Uninstall extension"""
        if extension_id not in self.extensions:
            return {'success': False, 'error': 'Extension not found'}
        
        try:
            ext_path = Path(self.extensions[extension_id]['path'])
            if ext_path.exists():
                shutil.rmtree(ext_path)
            
            del self.extensions[extension_id]
            return {'success': True, 'message': f'Extension {extension_id} uninstalled'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def enable_extension(self, extension_id: str) -> Dict:
        """Enable extension"""
        if extension_id not in self.extensions:
            return {'success': False, 'error': 'Extension not found'}
        
        self.extensions[extension_id]['enabled'] = True
        return {'success': True}
    
    def disable_extension(self, extension_id: str) -> Dict:
        """Disable extension"""
        if extension_id not in self.extensions:
            return {'success': False, 'error': 'Extension not found'}
        
        self.extensions[extension_id]['enabled'] = False
        return {'success': True}
    
    def search_marketplace(self, query: str, limit: int = 20) -> List[Dict]:
        """Search VS Code marketplace"""
        try:
            marketplace_url = "https://marketplace.visualstudio.com/_apis/public/gallery/extensionquery"
            
            payload = {
                "filters": [{
                    "criteria": [
                        {"filterType": 8, "value": "Microsoft.VisualStudio.Code"},
                        {"filterType": 10, "value": query}
                    ],
                    "pageNumber": 1,
                    "pageSize": limit,
                    "sortBy": 0,
                    "sortOrder": 0
                }],
                "flags": 0x200
            }
            
            response = requests.post(
                marketplace_url,
                json=payload,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                timeout=30
            )
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            extensions = []
            
            for result in data.get('results', []):
                for ext in result.get('extensions', []):
                    versions = ext.get('versions', [])
                    latest_version = versions[0] if versions else {}
                    files = latest_version.get('files', [])
                    icon_file = next((f for f in files if f.get('assetType') == 'Microsoft.VisualStudio.Services.Icons.Default'), {})
                    
                    # Get download count
                    stats = ext.get('statistics', [])
                    downloads = next((s.get('value', 0) for s in stats if s.get('statisticName') == 'install'), 0)
                    
                    extensions.append({
                        'id': ext.get('extensionId') or f"{ext.get('publisher', {}).get('publisherName', 'unknown')}.{ext.get('extensionName', 'unknown')}",
                        'name': ext.get('displayName', 'Unknown'),
                        'publisher': ext.get('publisher', {}).get('displayName', 'Unknown'),
                        'description': ext.get('shortDescription', 'No description'),
                        'version': latest_version.get('version', '1.0.0'),
                        'downloads': downloads,
                        'icon': icon_file.get('source', ''),
                        'rating': ext.get('rating', 0),
                        'ratingCount': ext.get('ratingCount', 0)
                    })
            
            return extensions
            
        except Exception as e:
            print(f"Marketplace search error: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def get_extension_contributions(self, extension_id: str) -> Dict:
        """Get extension contributions (commands, themes, etc.)"""
        if extension_id not in self.extensions:
            return {}
        
        manifest = self.extensions[extension_id]['manifest']
        return {
            'commands': manifest.get('contributes', {}).get('commands', []),
            'themes': manifest.get('contributes', {}).get('themes', []),
            'languages': manifest.get('contributes', {}).get('languages', []),
            'keybindings': manifest.get('contributes', {}).get('keybindings', []),
            'views': manifest.get('contributes', {}).get('views', {}),
        }

