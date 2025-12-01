"""
Security Scanner Integration - SAST, Dependency Scanning, Dynamic Testing
Integrates with AI to read outputs and propose/implement fixes
"""
import os
import json
import subprocess
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

class SecurityScanner:
    """Security scanner that integrates multiple SAST and dependency scanning tools"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.scan_results = []
        self.vulnerabilities = []
        
    def check_tool_available(self, tool_name: str) -> bool:
        """Check if a security tool is available"""
        try:
            if tool_name == 'semgrep':
                result = subprocess.run(['semgrep', '--version'], 
                                      capture_output=True, timeout=5)
                return result.returncode == 0
            elif tool_name == 'trivy':
                result = subprocess.run(['trivy', '--version'], 
                                      capture_output=True, timeout=5)
                return result.returncode == 0
            elif tool_name == 'osv-scanner':
                result = subprocess.run(['osv-scanner', '--version'], 
                                      capture_output=True, timeout=5)
                return result.returncode == 0
            elif tool_name == 'npm':
                result = subprocess.run(['npm', '--version'], 
                                      capture_output=True, timeout=5)
                return result.returncode == 0
            elif tool_name == 'pip':
                result = subprocess.run(['pip', '--version'], 
                                      capture_output=True, timeout=5)
                return result.returncode == 0
            return False
        except:
            return False
    
    def scan_with_semgrep(self, target_path: str = None) -> Dict[str, Any]:
        """Run Semgrep SAST scan"""
        if not self.check_tool_available('semgrep'):
            return {'available': False, 'error': 'Semgrep not installed'}
        
        target = target_path or str(self.workspace_root)
        results_file = self.workspace_root / 'semgrep_results.json'
        
        try:
            # Run Semgrep scan
            cmd = ['semgrep', '--config', 'auto', '--json', '-o', str(results_file), target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if results_file.exists():
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                findings = []
                for result_item in data.get('results', []):
                    findings.append({
                        'tool': 'semgrep',
                        'severity': result_item.get('extra', {}).get('severity', 'INFO'),
                        'rule_id': result_item.get('check_id', 'unknown'),
                        'message': result_item.get('message', ''),
                        'file': result_item.get('path', ''),
                        'line': result_item.get('start', {}).get('line', 0),
                        'code': result_item.get('extra', {}).get('lines', ''),
                        'type': 'sast'
                    })
                
                return {
                    'available': True,
                    'success': True,
                    'findings': findings,
                    'total': len(findings),
                    'output_file': str(results_file)
                }
            else:
                return {
                    'available': True,
                    'success': False,
                    'error': 'Semgrep scan completed but no results file found'
                }
        except subprocess.TimeoutExpired:
            return {'available': True, 'success': False, 'error': 'Semgrep scan timed out'}
        except Exception as e:
            return {'available': True, 'success': False, 'error': str(e)}
    
    def scan_with_trivy(self, target_path: str = None) -> Dict[str, Any]:
        """Run Trivy vulnerability scan"""
        if not self.check_tool_available('trivy'):
            return {'available': False, 'error': 'Trivy not installed'}
        
        target = target_path or str(self.workspace_root)
        results_file = self.workspace_root / 'trivy_results.json'
        
        try:
            # Run Trivy scan
            cmd = ['trivy', 'fs', '--format', 'json', '--output', str(results_file), target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if results_file.exists():
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                findings = []
                for result_item in data.get('Results', []):
                    for vuln in result_item.get('Vulnerabilities', []):
                        findings.append({
                            'tool': 'trivy',
                            'severity': vuln.get('Severity', 'UNKNOWN'),
                            'vulnerability_id': vuln.get('VulnerabilityID', ''),
                            'package': vuln.get('PkgName', ''),
                            'installed_version': vuln.get('InstalledVersion', ''),
                            'fixed_version': vuln.get('FixedVersion', ''),
                            'title': vuln.get('Title', ''),
                            'description': vuln.get('Description', ''),
                            'type': 'dependency_vulnerability'
                        })
                
                return {
                    'available': True,
                    'success': True,
                    'findings': findings,
                    'total': len(findings),
                    'output_file': str(results_file)
                }
            else:
                return {
                    'available': True,
                    'success': False,
                    'error': 'Trivy scan completed but no results file found'
                }
        except subprocess.TimeoutExpired:
            return {'available': True, 'success': False, 'error': 'Trivy scan timed out'}
        except Exception as e:
            return {'available': True, 'success': False, 'error': str(e)}
    
    def scan_with_osv_scanner(self, target_path: str = None) -> Dict[str, Any]:
        """Run OSV-Scanner for dependency vulnerabilities"""
        if not self.check_tool_available('osv-scanner'):
            return {'available': False, 'error': 'OSV-Scanner not installed'}
        
        target = target_path or str(self.workspace_root)
        results_file = self.workspace_root / 'osv_results.json'
        
        try:
            # Run OSV-Scanner
            cmd = ['osv-scanner', '--format', 'json', '--output', str(results_file), target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if results_file.exists():
                with open(results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                findings = []
                for result_item in data.get('results', []):
                    for vuln in result_item.get('vulnerabilities', []):
                        findings.append({
                            'tool': 'osv-scanner',
                            'severity': vuln.get('severity', {}).get('score', 'UNKNOWN'),
                            'vulnerability_id': vuln.get('id', ''),
                            'package': result_item.get('package', {}).get('name', ''),
                            'version': result_item.get('package', {}).get('version', ''),
                            'summary': vuln.get('summary', ''),
                            'details': vuln.get('details', ''),
                            'type': 'dependency_vulnerability'
                        })
                
                return {
                    'available': True,
                    'success': True,
                    'findings': findings,
                    'total': len(findings),
                    'output_file': str(results_file)
                }
            else:
                return {
                    'available': True,
                    'success': False,
                    'error': 'OSV-Scanner completed but no results file found'
                }
        except subprocess.TimeoutExpired:
            return {'available': True, 'success': False, 'error': 'OSV-Scanner scan timed out'}
        except Exception as e:
            return {'available': True, 'success': False, 'error': str(e)}
    
    def scan_npm_dependencies(self) -> Dict[str, Any]:
        """Scan npm dependencies for vulnerabilities"""
        if not self.check_tool_available('npm'):
            return {'available': False, 'error': 'npm not installed'}
        
        package_json = self.workspace_root / 'package.json'
        if not package_json.exists():
            return {'available': True, 'success': False, 'error': 'No package.json found'}
        
        try:
            # Run npm audit
            cmd = ['npm', 'audit', '--json']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.workspace_root), timeout=300)
            
            if result.returncode == 0 or result.stdout:
                data = json.loads(result.stdout)
                
                findings = []
                for vuln_id, vuln_data in data.get('vulnerabilities', {}).items():
                    findings.append({
                        'tool': 'npm-audit',
                        'severity': vuln_data.get('severity', 'moderate'),
                        'vulnerability_id': vuln_id,
                        'package': vuln_data.get('name', ''),
                        'title': vuln_data.get('title', ''),
                        'description': vuln_data.get('description', ''),
                        'recommendation': vuln_data.get('recommendation', ''),
                        'type': 'dependency_vulnerability'
                    })
                
                return {
                    'available': True,
                    'success': True,
                    'findings': findings,
                    'total': len(findings),
                    'summary': data.get('metadata', {})
                }
            else:
                return {
                    'available': True,
                    'success': False,
                    'error': 'npm audit failed'
                }
        except subprocess.TimeoutExpired:
            return {'available': True, 'success': False, 'error': 'npm audit timed out'}
        except Exception as e:
            return {'available': True, 'success': False, 'error': str(e)}
    
    def scan_pip_dependencies(self) -> Dict[str, Any]:
        """Scan Python dependencies for vulnerabilities"""
        if not self.check_tool_available('pip'):
            return {'available': False, 'error': 'pip not installed'}
        
        requirements_txt = self.workspace_root / 'requirements.txt'
        if not requirements_txt.exists():
            return {'available': True, 'success': False, 'error': 'No requirements.txt found'}
        
        try:
            # Use pip-audit if available, otherwise use safety
            # Try pip-audit first
            try:
                cmd = ['pip-audit', '--format', 'json', '--output', str(self.workspace_root / 'pip_audit_results.json')]
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.workspace_root), timeout=300)
                
                results_file = self.workspace_root / 'pip_audit_results.json'
                if results_file.exists():
                    with open(results_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    findings = []
                    for vuln in data.get('vulnerabilities', []):
                        findings.append({
                            'tool': 'pip-audit',
                            'severity': vuln.get('severity', 'UNKNOWN'),
                            'vulnerability_id': vuln.get('id', ''),
                            'package': vuln.get('name', ''),
                            'installed_version': vuln.get('installed_version', ''),
                            'fixed_version': vuln.get('fixed_version', ''),
                            'description': vuln.get('description', ''),
                            'type': 'dependency_vulnerability'
                        })
                    
                    return {
                        'available': True,
                        'success': True,
                        'findings': findings,
                        'total': len(findings)
                    }
            except:
                pass
            
            # Fallback: return info that pip-audit is needed
            return {
                'available': True,
                'success': False,
                'error': 'pip-audit not installed. Install with: pip install pip-audit'
            }
        except Exception as e:
            return {'available': True, 'success': False, 'error': str(e)}
    
    def run_full_scan(self, target_path: str = None) -> Dict[str, Any]:
        """Run all available security scans"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'target': target_path or str(self.workspace_root),
            'scans': {}
        }
        
        # Run SAST scans
        print("[SECURITY] Running Semgrep scan...")
        semgrep_result = self.scan_with_semgrep(target_path)
        results['scans']['semgrep'] = semgrep_result
        
        # Run dependency vulnerability scans
        print("[SECURITY] Running Trivy scan...")
        trivy_result = self.scan_with_trivy(target_path)
        results['scans']['trivy'] = trivy_result
        
        print("[SECURITY] Running OSV-Scanner...")
        osv_result = self.scan_with_osv_scanner(target_path)
        results['scans']['osv-scanner'] = osv_result
        
        # Run package manager scans
        print("[SECURITY] Running npm audit...")
        npm_result = self.scan_npm_dependencies()
        results['scans']['npm-audit'] = npm_result
        
        print("[SECURITY] Running pip audit...")
        pip_result = self.scan_pip_dependencies()
        results['scans']['pip-audit'] = pip_result
        
        # Aggregate all findings
        all_findings = []
        for scan_name, scan_result in results['scans'].items():
            if scan_result.get('success') and scan_result.get('findings'):
                all_findings.extend(scan_result['findings'])
        
        results['total_findings'] = len(all_findings)
        results['all_findings'] = all_findings
        
        # Save aggregated results
        results_file = self.workspace_root / 'security_scan_results.json'
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        return results
    
    def format_findings_for_ai(self, scan_results: Dict[str, Any]) -> str:
        """Format scan results for AI to read and propose fixes"""
        output = "# Security Scan Results\n\n"
        output += f"**Scan Date:** {scan_results.get('timestamp', 'Unknown')}\n"
        output += f"**Target:** {scan_results.get('target', 'Unknown')}\n"
        output += f"**Total Findings:** {scan_results.get('total_findings', 0)}\n\n"
        
        # Group by type
        sast_findings = []
        dependency_findings = []
        
        for finding in scan_results.get('all_findings', []):
            if finding.get('type') == 'sast':
                sast_findings.append(finding)
            elif finding.get('type') == 'dependency_vulnerability':
                dependency_findings.append(finding)
        
        if sast_findings:
            output += "## SAST Findings (Code Security Issues)\n\n"
            for i, finding in enumerate(sast_findings, 1):
                output += f"### Finding {i}\n"
                output += f"- **Tool:** {finding.get('tool', 'Unknown')}\n"
                output += f"- **Severity:** {finding.get('severity', 'Unknown')}\n"
                output += f"- **Rule:** {finding.get('rule_id', 'Unknown')}\n"
                output += f"- **File:** {finding.get('file', 'Unknown')}\n"
                output += f"- **Line:** {finding.get('line', 0)}\n"
                output += f"- **Message:** {finding.get('message', '')}\n"
                output += f"- **Code:**\n```\n{finding.get('code', '')}\n```\n\n"
        
        if dependency_findings:
            output += "## Dependency Vulnerabilities\n\n"
            for i, finding in enumerate(dependency_findings, 1):
                output += f"### Vulnerability {i}\n"
                output += f"- **Tool:** {finding.get('tool', 'Unknown')}\n"
                output += f"- **Severity:** {finding.get('severity', 'Unknown')}\n"
                output += f"- **Vulnerability ID:** {finding.get('vulnerability_id', 'Unknown')}\n"
                output += f"- **Package:** {finding.get('package', 'Unknown')}\n"
                if finding.get('installed_version'):
                    output += f"- **Installed Version:** {finding.get('installed_version')}\n"
                if finding.get('fixed_version'):
                    output += f"- **Fixed Version:** {finding.get('fixed_version')}\n"
                output += f"- **Title:** {finding.get('title', finding.get('summary', ''))}\n"
                output += f"- **Description:** {finding.get('description', finding.get('details', ''))}\n"
                if finding.get('recommendation'):
                    output += f"- **Recommendation:** {finding.get('recommendation')}\n"
                output += "\n"
        
        return output

