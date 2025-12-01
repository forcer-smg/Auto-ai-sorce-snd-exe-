# Tomorrow's TODO - Terminal Integration Fix

## Main Issue to Fix
**Problem:** Batch files and terminal commands output to background terminal instead of dashboard terminal panel.

## Tasks

### 1. Fix Terminal Output Routing
- [ ] Investigate why subprocess output goes to background terminal
- [ ] Ensure all `subprocess.run()` calls capture output properly
- [ ] Route all terminal output through WebSocket to dashboard
- [ ] Test with various command types (batch files, Python scripts, etc.)

### 2. Real-time Terminal Streaming
- [ ] Improve real-time output streaming for long-running commands
- [ ] Add progress indicators in terminal panel
- [ ] Handle multi-line output properly
- [ ] Ensure terminal auto-scrolls to latest output

### 3. Batch File Execution
- [ ] Fix batch file execution to show output in dashboard
- [ ] Test with different batch file scenarios
- [ ] Handle batch file errors properly
- [ ] Ensure batch files don't open new console windows

### 4. Testing
- [ ] Test with simple commands (`dir`, `echo`, etc.)
- [ ] Test with batch files
- [ ] Test with Python scripts
- [ ] Test with long-running commands
- [ ] Verify all output appears in dashboard terminal

### 5. Code Review
- [ ] Review `app.py` terminal execution code
- [ ] Review `ide.js` terminal output handling
- [ ] Check WebSocket event handling
- [ ] Verify error handling

## Files to Check
- `app.py` - Terminal execution endpoints
- `static/js/ide.js` - Terminal output display
- `auto_punch_automation_integration.py` - Automation module (if exists)
- Any subprocess calls that might bypass dashboard

## Expected Behavior
When AI generates code or executes commands:
1. ✅ Terminal panel opens automatically
2. ✅ Command is displayed with `$` prefix
3. ✅ Output appears in real-time
4. ✅ All output goes to dashboard terminal (not background)
5. ✅ Terminal auto-scrolls to show latest output

## Current Status
- ✅ Code generation works
- ✅ File creation works
- ✅ Editor opening works
- ⚠️ Terminal output routing needs fix
- ⚠️ Batch file execution needs fix

