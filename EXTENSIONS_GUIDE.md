# Extensions Guide - Auto_Punch IDE

## 🎯 Extension System

Auto_Punch IDE now supports installing extensions from the VS Code Marketplace, just like Cursor AI!

## ✨ Features

- ✅ **VS Code Marketplace Integration** - Install any VS Code extension
- ✅ **Search Extensions** - Search the marketplace
- ✅ **Install/Uninstall** - Easy extension management
- ✅ **Enable/Disable** - Control which extensions are active
- ✅ **Extension Browser** - Beautiful UI to browse extensions

## 🚀 How to Use

### Accessing Extensions

1. Click the **Extensions** icon in the activity bar (left sidebar)
2. You'll see two tabs:
   - **Installed** - All your installed extensions
   - **Marketplace** - Search and install new extensions

### Installing Extensions

#### Method 1: Search and Install
1. Go to **Marketplace** tab
2. Type the extension name in the search box
3. Press Enter or click Search
4. Click **Install** on any extension you want

#### Method 2: Install by ID
You can also ask the AI:
```
"install extension: ms-python.python"
"install extension: esbenp.prettier-vscode"
```

### Managing Extensions

- **Enable/Disable**: Click the Enable/Disable button
- **Uninstall**: Click the Uninstall button
- **Refresh**: Click the refresh icon to reload the list

## 📦 Popular Extensions to Try

### Language Support
- `ms-python.python` - Python
- `ms-vscode.vscode-typescript-next` - TypeScript
- `golang.go` - Go
- `rust-lang.rust-analyzer` - Rust

### Code Formatting
- `esbenp.prettier-vscode` - Prettier
- `ms-python.black-formatter` - Black formatter

### Themes
- `pkief.material-icon-theme` - Material Icon Theme
- `zhuangtongfa.material-theme` - One Dark Pro

### Productivity
- `github.copilot` - GitHub Copilot
- `ms-vscode.vscode-json` - JSON tools
- `redhat.vscode-yaml` - YAML support

## 🔧 Extension API

Extensions are stored in: `extensions/` directory

Each extension has:
- `package.json` - Extension manifest
- Extension files and resources

## 💡 Tips

1. **Search by name**: Just type the extension name (e.g., "python", "prettier")
2. **Install popular ones**: Extensions with high download counts are usually reliable
3. **Check compatibility**: Extensions show their VS Code version requirement
4. **Restart may be needed**: Some extensions require IDE restart to fully activate

## 🎉 That's It!

You can now install any VS Code extension and use it in Auto_Punch IDE, just like Cursor AI!

