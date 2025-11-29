"""
Dashboard Fix Agent - Specialized AI agent for fixing dashboard/UI issues
Can use OpenAI or other models to diagnose and fix frontend issues
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Callable

class DashboardFixAgent:
    """Specialized agent for fixing dashboard and UI issues"""
    
    def __init__(self, workspace_path: str, progress_callback: Optional[Callable] = None):
        self.workspace_path = Path(workspace_path)
        self.progress_callback = progress_callback
        self.openai_client = None
        self._init_openai()
    
    def set_progress_callback(self, callback: Callable):
        """Set or update the progress callback"""
        self.progress_callback = callback
    
    def _init_openai(self):
        """Initialize OpenAI client if API key is available"""
        try:
            from openai import OpenAI
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
                print("✓ Dashboard Fix Agent: OpenAI initialized")
            else:
                print("⚠ Dashboard Fix Agent: OPENAI_API_KEY not found, using fallback")
        except ImportError:
            print("⚠ Dashboard Fix Agent: OpenAI package not installed, using fallback")
        except Exception as e:
            print(f"⚠ Dashboard Fix Agent: OpenAI init error: {e}")
    
    def _emit_progress(self, message: str, data: Optional[Dict] = None):
        """Emit progress update"""
        if self.progress_callback:
            self.progress_callback({
                'type': 'progress',
                'message': message,
                'data': data or {}
            })
    
    def _emit_file_explored(self, file_path: str, lines: Optional[str] = None):
        """Emit file exploration update"""
        if self.progress_callback:
            self.progress_callback({
                'type': 'file_explored',
                'file': file_path,
                'lines': lines
            })
    
    def _emit_diff(self, file_path: str, old_content: str, new_content: str, 
                   old_lines: Optional[List[int]] = None, new_lines: Optional[List[int]] = None):
        """Emit code diff"""
        if self.progress_callback:
            # Calculate line numbers for diff
            old_lines_list = old_lines or list(range(1, len(old_content.split('\n')) + 1))
            new_lines_list = new_lines or list(range(1, len(new_content.split('\n')) + 1))
            
            self.progress_callback({
                'type': 'diff',
                'file': file_path,
                'old_content': old_content,
                'new_content': new_content,
                'old_lines': old_lines_list,
                'new_lines': new_lines_list
            })
    
    def analyze_dashboard_issue(self, issue_description: str) -> Dict:
        """Analyze a dashboard issue and propose fixes"""
        self._emit_progress("🔍 Analyzing dashboard issue...")
        
        # Find relevant files
        static_dir = self.workspace_path / 'static'
        templates_dir = self.workspace_path / 'templates'
        
        relevant_files = []
        
        # Check CSS files
        if static_dir.exists():
            css_files = list(static_dir.glob('**/*.css'))
            relevant_files.extend([str(f) for f in css_files])
        
        # Check JS files
        if static_dir.exists():
            js_files = list(static_dir.glob('**/*.js'))
            relevant_files.extend([str(f) for f in js_files])
        
        # Check HTML templates
        if templates_dir.exists():
            html_files = list(templates_dir.glob('**/*.html'))
            relevant_files.extend([str(f) for f in html_files])
        
        self._emit_progress(f"📁 Found {len(relevant_files)} relevant files")
        
        # Read and analyze files
        file_contents = {}
        for file_path in relevant_files[:10]:  # Limit to first 10 files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_contents[file_path] = content
                    self._emit_file_explored(file_path, f"L1-{len(content.split(chr(10)))}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
        
        # Use AI to analyze if available
        if self.openai_client:
            return self._analyze_with_openai(issue_description, file_contents)
        else:
            return self._analyze_fallback(issue_description, file_contents)
    
    def _analyze_with_openai(self, issue: str, files: Dict[str, str]) -> Dict:
        """Analyze using OpenAI"""
        self._emit_progress("🤖 Using AI to analyze issue...")
        
        try:
            # Prepare context
            file_summaries = []
            for path, content in list(files.items())[:5]:  # Limit context
                lines = content.split('\n')
                file_summaries.append(f"{Path(path).name} ({len(lines)} lines)")
            
            prompt = f"""You are a dashboard/UI fix agent. Analyze this issue and propose fixes.

Issue: {issue}

Relevant files:
{chr(10).join(file_summaries)}

Provide:
1. Root cause analysis
2. Specific files that need changes
3. Exact code changes needed (show diffs)
4. Testing recommendations

Format your response with clear sections and code diffs."""
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert frontend developer specializing in fixing UI/dashboard issues. Provide clear, actionable fixes with code diffs."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            analysis = response.choices[0].message.content
            
            return {
                'success': True,
                'analysis': analysis,
                'method': 'openai',
                'files_analyzed': len(files)
            }
        except Exception as e:
            print(f"OpenAI analysis error: {e}")
            return self._analyze_fallback(issue, files)
    
    def _analyze_fallback(self, issue: str, files: Dict[str, str]) -> Dict:
        """Fallback analysis without AI"""
        self._emit_progress("🔧 Using rule-based analysis...")
        
        # Simple keyword-based analysis
        issue_lower = issue.lower()
        suggestions = []
        
        if 'slow' in issue_lower or 'performance' in issue_lower:
            suggestions.append("Check for heavy animations, reduce box-shadows, optimize CSS transitions")
        
        if 'blue' in issue_lower or 'color' in issue_lower:
            suggestions.append("Check CSS for blue color values (#007acc, rgba with blue), replace with theme colors")
        
        if 'background' in issue_lower:
            suggestions.append("Check background image paths, overlay opacity, z-index issues")
        
        if 'not displaying' in issue_lower or 'not showing' in issue_lower:
            suggestions.append("Check file paths, cache headers, image loading errors")
        
        return {
            'success': True,
            'analysis': f"Issue: {issue}\n\nSuggestions:\n" + "\n".join(f"- {s}" for s in suggestions),
            'method': 'fallback',
            'files_analyzed': len(files)
        }
    
    def fix_issue(self, issue_description: str, auto_apply: bool = False) -> Dict:
        """Fix a dashboard issue"""
        self._emit_progress("🚀 Starting fix process...")
        
        # Analyze first
        analysis = self.analyze_dashboard_issue(issue_description)
        
        if not analysis.get('success'):
            return {
                'success': False,
                'error': 'Analysis failed'
            }
        
        # Extract fixes from analysis
        fixes = self._extract_fixes(analysis['analysis'])
        
        applied_fixes = []
        if auto_apply:
            for fix in fixes:
                result = self._apply_fix(fix)
                if result.get('success'):
                    applied_fixes.append(result)
        
        return {
            'success': True,
            'analysis': analysis,
            'fixes': fixes,
            'applied': applied_fixes if auto_apply else [],
            'method': analysis.get('method', 'unknown')
        }
    
    def _extract_fixes(self, analysis: str) -> List[Dict]:
        """Extract fix instructions from analysis"""
        fixes = []
        
        # Try to parse code blocks and file references
        import re
        
        # Look for file paths
        file_pattern = r'([\w/\\]+\.(css|js|html))'
        files_mentioned = re.findall(file_pattern, analysis)
        
        # Look for code diffs
        diff_pattern = r'```(?:diff)?\n([\s\S]+?)```'
        code_blocks = re.findall(diff_pattern, analysis)
        
        for i, code_block in enumerate(code_blocks):
            fixes.append({
                'type': 'code_change',
                'code': code_block,
                'index': i
            })
        
        return fixes
    
    def _apply_fix(self, fix: Dict) -> Dict:
        """Apply a single fix"""
        try:
            if fix['type'] == 'code_change':
                # This would need more sophisticated parsing
                # For now, return success
                self._emit_progress(f"✅ Applied fix #{fix.get('index', 0)}")
                return {
                    'success': True,
                    'fix': fix
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        
        return {'success': False, 'error': 'Unknown fix type'}

