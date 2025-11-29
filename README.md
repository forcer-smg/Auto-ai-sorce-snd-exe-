# Auto_Punch IDE

A standalone IDE that combines VS Code and Cursor features, powered by **Auto_Punch Ai** as the main agent.

## Features

### VS Code Features
- ✅ Monaco Editor (same editor as VS Code)
- ✅ File Explorer
- ✅ Multi-tab editing
- ✅ Syntax highlighting for 20+ languages
- ✅ Integrated Terminal
- ✅ Git integration
- ✅ Search functionality
- ✅ Status bar with cursor position

### Cursor Features
- ✅ AI Chat interface
- ✅ Natural language commands
- ✅ Code analysis and fixing
- ✅ Todo management
- ✅ AI-powered code completion

### Auto_Punch Ai Integration
- ✅ All Auto_Punch Ai capabilities
- ✅ Natural language automation
- ✅ Code analysis
- ✅ Test running
- ✅ Git operations
- ✅ System control

## Installation

### Windows
1. Double-click `run.bat`
2. The IDE will automatically install dependencies and start

### Manual Installation
```bash
cd "C:\Users\Administrator\Auto_Punch IDE"
pip install -r requirements.txt
python app.py
```

## Usage

1. **Start the IDE**: Run `run.bat` or `python app.py`
2. **Open Browser**: The IDE will open automatically at `http://localhost:5001`
3. **Open Files**: Click files in the explorer to open them
4. **AI Chat**: Click the AI icon in the activity bar to chat with Auto_Punch Ai
5. **Terminal**: Press `Ctrl+`` to toggle terminal
6. **Save Files**: Press `Ctrl+S` to save

## Keyboard Shortcuts

- `Ctrl+S` - Save file
- `Ctrl+`` - Toggle terminal
- `Enter` - Send chat message / Execute terminal command

## Architecture

- **Backend**: Flask + Flask-SocketIO
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Editor**: Monaco Editor (VS Code's editor)
- **AI Agent**: Auto_Punch Ai (natural language automation)

## API Endpoints

- `/api/workspace/*` - Workspace management
- `/api/files/*` - File operations
- `/api/ai/chat` - AI chat
- `/api/code/*` - Code analysis
- `/api/terminal/*` - Terminal execution
- `/api/todos/*` - Todo management
- `/api/git/*` - Git operations

## Requirements

- Python 3.7+
- Auto_Punch Ai installed at `C:\Users\Administrator\Auto_Punch Ai`
- All Auto_Punch Ai dependencies

## Notes

- The IDE runs on port 5001 by default
- All Auto_Punch Ai features are available through the AI chat
- Files are saved automatically when you use Ctrl+S
- The terminal uses Auto_Punch Ai's automation system

## Troubleshooting

1. **Port already in use**: Change port in `app.py` (line with `port = 5001`)
2. **Auto_Punch Ai not found**: Make sure Auto_Punch Ai is installed at the correct path
3. **Dependencies missing**: Run `pip install -r requirements.txt`

## License

Same as Auto_Punch Ai

