"""
Agent Workflow System - Cursor AI Style
Handles multi-step task execution with state tracking
"""
import os
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any

class WorkflowAgent:
    """Agent that executes multi-step tasks sequentially like Cursor AI"""
    
    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root)
        self.state_file = self.workspace_root / "workflow_state.md"
        self.process_file = self.workspace_root / "update_process.md"
        self.current_phase = "Idle"
        self.current_step = 0
        self.total_steps = 0
        self.completed_steps = []
        self.pending_steps = []
        self.errors = []
        self.results = []
        
    def load_state(self) -> Dict[str, Any]:
        """Load workflow state from state file"""
        if not self.state_file.exists():
            return {
                "phase": "Idle",
                "current_step": 0,
                "total_steps": 0,
                "completed_steps": [],
                "pending_steps": [],
                "errors": [],
                "results": [],
                "plan": []
            }
        
        try:
            content = self.state_file.read_text(encoding='utf-8')
            state = self._parse_state_markdown(content)
            return state
        except Exception as e:
            print(f"[AGENT] Error loading state: {e}")
            return self._default_state()
    
    def _parse_state_markdown(self, content: str) -> Dict[str, Any]:
        """Parse state from markdown format"""
        state = self._default_state()
        
        # Extract phase
        phase_match = re.search(r'## Phase:\s*(.+)', content)
        if phase_match:
            state["phase"] = phase_match.group(1).strip()
        
        # Extract current step
        step_match = re.search(r'Current Step:\s*(\d+)', content)
        if step_match:
            state["current_step"] = int(step_match.group(1))
        
        # Extract completed steps
        completed_section = re.search(r'## Completed Steps(.*?)##', content, re.DOTALL)
        if completed_section:
            completed_lines = completed_section.group(1).strip().split('\n')
            state["completed_steps"] = [line.strip('- ').strip() for line in completed_lines if line.strip()]
        
        # Extract pending steps
        pending_section = re.search(r'## Pending Steps(.*?)(?:##|$)', content, re.DOTALL)
        if pending_section:
            pending_lines = pending_section.group(1).strip().split('\n')
            state["pending_steps"] = [line.strip('- ').strip() for line in pending_lines if line.strip()]
        
        # Extract plan
        plan_section = re.search(r'## Plan(.*?)(?:##|$)', content, re.DOTALL)
        if plan_section:
            plan_lines = plan_section.group(1).strip().split('\n')
            state["plan"] = [line.strip('- ').strip() for line in plan_lines if line.strip()]
            state["total_steps"] = len(state["plan"])
        
        return state
    
    def _default_state(self) -> Dict[str, Any]:
        """Return default state structure"""
        return {
            "phase": "Idle",
            "current_step": 0,
            "total_steps": 0,
            "completed_steps": [],
            "pending_steps": [],
            "errors": [],
            "results": [],
            "plan": []
        }
    
    def save_state(self, state: Dict[str, Any]):
        """Save workflow state to markdown file"""
        try:
            content = f"""# Workflow State

**Last Updated:** {datetime.now().isoformat()}

## Phase: {state.get('phase', 'Idle')}

**Current Step:** {state.get('current_step', 0)} / {state.get('total_steps', 0)}

## Plan

"""
            for i, step in enumerate(state.get('plan', []), 1):
                status = "✅" if i <= state.get('current_step', 0) else "⏳"
                content += f"{status} {i}. {step}\n"
            
            content += "\n## Completed Steps\n\n"
            for step in state.get('completed_steps', []):
                content += f"- ✅ {step}\n"
            
            content += "\n## Pending Steps\n\n"
            for step in state.get('pending_steps', []):
                content += f"- ⏳ {step}\n"
            
            if state.get('errors'):
                content += "\n## Errors\n\n"
                for error in state['errors']:
                    content += f"- ❌ {error}\n"
            
            if state.get('results'):
                content += "\n## Results\n\n"
                for result in state['results']:
                    content += f"- {result}\n"
            
            self.state_file.write_text(content, encoding='utf-8')
            print(f"[AGENT] State saved to {self.state_file}")
        except Exception as e:
            print(f"[AGENT] Error saving state: {e}")
    
    def extract_plan_from_text(self, text: str) -> List[str]:
        """Extract a numbered plan from text (like a TODO list)"""
        plan = []
        
        # Look for numbered lists
        numbered_pattern = r'(?:^|\n)\s*(\d+)[\.\)]\s*(.+?)(?=\n\s*\d+[\.\)]|\n\n|$)'
        matches = re.findall(numbered_pattern, text, re.MULTILINE)
        for num, step in matches:
            plan.append(step.strip())
        
        # Look for markdown task lists
        task_pattern = r'(?:^|\n)\s*[-*]\s*(?:\[[ x]\]\s*)?(.+?)(?=\n\s*[-*]|\n\n|$)'
        task_matches = re.findall(task_pattern, text, re.MULTILINE)
        if task_matches and not plan:
            plan = [task.strip() for task in task_matches]
        
        # Look for "Step X:" patterns
        step_pattern = r'(?:Step|Task)\s*\d+[:\-]\s*(.+?)(?=\n(?:Step|Task)|\n\n|$)'
        step_matches = re.findall(step_pattern, text, re.IGNORECASE | re.MULTILINE)
        if step_matches and not plan:
            plan = [step.strip() for step in step_matches]
        
        return plan
    
    def initialize_workflow(self, plan: List[str], phase: str = "Execution"):
        """Initialize a new workflow with a plan"""
        state = {
            "phase": phase,
            "current_step": 0,
            "total_steps": len(plan),
            "completed_steps": [],
            "pending_steps": plan.copy(),
            "errors": [],
            "results": [],
            "plan": plan
        }
        self.save_state(state)
        return state
    
    def get_next_step(self, state: Dict[str, Any]) -> Optional[str]:
        """Get the next pending step"""
        current = state.get('current_step', 0)
        plan = state.get('plan', [])
        
        if current < len(plan):
            return plan[current]
        return None
    
    def mark_step_complete(self, state: Dict[str, Any], step_result: str = "", error: str = "", verified: bool = False):
        """Mark current step as complete and move to next"""
        current = state.get('current_step', 0)
        plan = state.get('plan', [])
        
        if current < len(plan):
            step = plan[current]
            state['completed_steps'].append(step)
            if step in state['pending_steps']:
                state['pending_steps'].remove(step)
            
            if error:
                state['errors'].append(f"Step {current + 1}: {error}")
            elif step_result:
                result_entry = f"Step {current + 1}: {step_result}"
                if verified:
                    result_entry += " ✅ VERIFIED"
                state['results'].append(result_entry)
            
            state['current_step'] = current + 1
        
        self.save_state(state)
        return state
    
    def add_verification_step(self, state: Dict[str, Any], verification_type: str, command: str = None):
        """Add a verification step to ensure task is actually complete"""
        verification_steps = state.get('verification_steps', [])
        
        verification = {
            'type': verification_type,  # 'test', 'run', 'check_output', 'validate'
            'command': command,
            'status': 'pending'
        }
        
        verification_steps.append(verification)
        state['verification_steps'] = verification_steps
        self.save_state(state)
        return state
    
    def mark_verification_complete(self, state: Dict[str, Any], verification_index: int, success: bool, result: str = ""):
        """Mark a verification step as complete"""
        verification_steps = state.get('verification_steps', [])
        if verification_index < len(verification_steps):
            verification_steps[verification_index]['status'] = 'complete' if success else 'failed'
            verification_steps[verification_index]['result'] = result
            state['verification_steps'] = verification_steps
            self.save_state(state)
        return state
    
    def is_workflow_complete(self, state: Dict[str, Any]) -> bool:
        """Check if workflow is complete"""
        return state.get('current_step', 0) >= state.get('total_steps', 0)
    
    def update_process_file(self, message: str):
        """Update the process tracking file"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.process_file.exists():
                content = self.process_file.read_text(encoding='utf-8')
            else:
                content = "# Update Process\n\n"
            
            content += f"\n[{timestamp}] {message}\n"
            self.process_file.write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"[AGENT] Error updating process file: {e}")

