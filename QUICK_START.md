# Quick Start Guide - Auto_Punch IDE

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd "C:\Users\Administrator\Auto_Punch IDE"
pip install -r requirements.txt
```

### Step 2: Run the IDE
**Windows:**
```bash
run.bat
```

**Or manually:**
```bash
python app.py
```

### Step 3: Open in Browser
The IDE will automatically open at `http://localhost:5001`

If it doesn't open automatically, navigate to: **http://localhost:5001**

## 📖 Basic Usage

### Opening Files
1. Click the **Explorer** icon (folder icon) in the left sidebar
2. Click on any file to open it in the editor
3. Files open in tabs at the top

### Using AI Chat (Cursor Feature)
1. Click the **AI Chat** icon in the left sidebar
2. Type your question or command
3. Press Enter or click Send
4. Auto_Punch Ai will execute your command

**Example AI Commands:**
- "create file: test.py with content: print('Hello')"
- "analyze code: app.py"
- "add todo: fix the bug"
- "run tests"
- "system info"

### Using Terminal
1. Press `Ctrl+`` (backtick) to toggle terminal
2. Or click **Terminal** in the menu bar
3. Type commands and press Enter

### Saving Files
- Press `Ctrl+S` to save the current file
- Unsaved files show a `*` next to the filename

### Managing Todos
1. Click the **Todos** icon in the left sidebar
2. Type a todo and press Enter
3. Check off completed todos
4. Delete todos with the × button

## 🎯 Key Features

### VS Code Features
- ✅ Monaco Editor (same as VS Code)
- ✅ File Explorer
- ✅ Multi-tab editing
- ✅ Syntax highlighting
- ✅ Integrated Terminal
- ✅ Git integration

### Cursor Features
- ✅ AI Chat interface
- ✅ Natural language commands
- ✅ Code analysis
- ✅ Todo management

### Auto_Punch Ai Features
- ✅ All Auto_Punch Ai capabilities
- ✅ Natural language automation
- ✅ Code fixing
- ✅ Test running
- ✅ System control

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+S` | Save file |
| `Ctrl+`` | Toggle terminal |
| `Enter` | Send chat message / Execute command |

## 🔧 Troubleshooting

### Port Already in Use
If port 5001 is busy, edit `app.py` and change:
```python
port = 5001  # Change to another port like 5002
```

### Auto_Punch Ai Not Found
Make sure Auto_Punch Ai is installed at:
```
C:\Users\Administrator\Auto_Punch Ai
```

### Dependencies Missing
```bash
pip install -r requirements.txt
```

## 💡 Tips

1. **AI Chat understands natural language** - Just describe what you want
2. **Files auto-save** when you press Ctrl+S
3. **Terminal uses Auto_Punch Ai** - All commands go through Auto_Punch Ai
4. **Todos persist** - They're saved between sessions
5. **Multiple files** - Open as many files as you want in tabs

## 🎉 You're Ready!

Start coding with the power of VS Code + Cursor + Auto_Punch Ai! 🚀

