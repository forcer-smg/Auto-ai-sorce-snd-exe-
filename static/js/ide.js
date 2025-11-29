// Auto_Punch IDE - Main JavaScript

let editor = null;
let currentFiles = {};
let currentWorkspace = null;
let socket = null;
let currentSessionId = null;
let activeProgressUpdates = {}; // Track active progress updates
let fileExplorationCount = 0;

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing IDE...');
    
    // Initialize Monaco Editor with better error handling
    if (typeof require !== 'undefined') {
        require.config({ 
            paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' },
            'vs/nls': { availableLanguages: { '*': 'en' } }
        });
        require(['vs/editor/editor.main'], function () {
            console.log('Monaco Editor loaded, initializing...');
            setTimeout(() => {
                initMonacoEditor();
            }, 100);
        }, function(err) {
            console.error('Monaco Editor load error:', err);
            loadMonacoEditorFallback();
        });
    } else {
        console.log('Require.js not available, using direct loader...');
        loadMonacoEditorDirect();
    }
});

function loadMonacoEditorDirect() {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js';
    script.onload = function() {
        require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
        require(['vs/editor/editor.main'], function() {
            console.log('Monaco Editor loaded via direct script');
            setTimeout(() => {
                initMonacoEditor();
            }, 100);
        });
    };
    script.onerror = function() {
        console.error('Failed to load Monaco Editor');
        loadMonacoEditorFallback();
    };
    document.head.appendChild(script);
}

function loadMonacoEditorFallback() {
    const editorElement = document.getElementById('monaco-editor');
    if (editorElement) {
        editorElement.innerHTML = '<div style="padding: 20px; color: #f48771;"><p>⚠ Monaco Editor failed to load</p><p>Please check your internet connection and refresh the page.</p></div>';
    }
}

function initMonacoEditor() {
    try {
        const editorElement = document.getElementById('monaco-editor');
        if (!editorElement) {
            console.error('Monaco editor element not found!');
            return;
        }
        
        // Clear loading message
        const loadingDiv = document.getElementById('editor-loading');
        if (loadingDiv) {
            loadingDiv.style.display = 'none';
        }
        
        // Check if monaco is available
        if (typeof monaco === 'undefined') {
            console.error('Monaco Editor not loaded!');
            if (loadingDiv) {
                loadingDiv.innerHTML = '<p style="color: #f48771;">⚠ Monaco Editor not loaded</p><p>Please refresh the page.</p>';
            }
            return;
        }
        
        console.log('Creating Monaco Editor instance...');
        
        // Ensure element has proper dimensions
        editorElement.style.width = '100%';
        editorElement.style.height = '100%';
        
        editor = monaco.editor.create(editorElement, {
            value: `// ═══════════════════════════════════════════════════════════════
//  ██╗  ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗      ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗ 
//  ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝      ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
//  ███████║███████║██║     █████╔╝ ██║██╔██╗ ██║██║         ███████╗██║██║   ██║██║  ██║██║     ██║  ██║
//  ██╔══██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║         ╚════██║██║██║   ██║██║  ██║██║     ██║  ██║
//  ██║  ██║██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╗          ██║██║╚██████╔╝██████╔╝███████╗██████╔╝
//  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝          ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═════╝ 
// ═══════════════════════════════════════════════════════════════
//  🔥 WELCOME TO HACKING WORLD 🔥
// ═══════════════════════════════════════════════════════════════
//  ⚡ Powered by Auto_Punch Ai ⚡
//  👤 Author: SMG...
// ═══════════════════════════════════════════════════════════════

console.log("Hello, World!");`,
            language: 'javascript',
            theme: 'vs-dark',
            automaticLayout: true,
            fontSize: 14,
            minimap: { enabled: true },
            wordWrap: 'on',
            lineNumbers: 'on',
            scrollBeyondLastLine: false,
            renderLineHighlight: 'all',
            selectOnLineNumbers: true,
            roundedSelection: false,
            readOnly: false,
            cursorStyle: 'line',
            fontFamily: 'Consolas, "Courier New", monospace'
        });
        
        console.log('Monaco Editor created successfully!');

        editor.onDidChangeCursorPosition((e) => {
            const position = e.position;
            const cursorEl = document.getElementById('cursor-position');
            if (cursorEl) {
                cursorEl.textContent = 'Ln ' + position.lineNumber + ', Col ' + position.column;
            }
        });

        editor.onDidChangeModelLanguage((e) => {
            const language = e.newLanguage;
            const langEl = document.getElementById('file-language');
            if (langEl) {
                langEl.textContent = language || 'Plain Text';
            }
        });

        editor.onDidChangeModelContent(() => {
            const model = editor.getModel();
            if (model && model.uri) {
                const filePath = model.uri.path;
                if (currentFiles[filePath]) {
                    currentFiles[filePath].content = editor.getValue();
                    currentFiles[filePath].modified = true;
                    updateTab(filePath);
                }
            }
        });

        // Force layout update after creation
        setTimeout(() => {
            if (editor) {
                editor.layout();
                console.log('Monaco Editor layout updated');
            }
        }, 200);
        
        console.log('Monaco Editor initialized successfully');
        
        // Initialize other components
        initOtherComponents();
    } catch (error) {
        console.error('Error initializing Monaco Editor:', error);
        // Show fallback message
        const editorElement = document.getElementById('monaco-editor');
        if (editorElement) {
            editorElement.innerHTML = '<div style="padding: 20px; color: #ccc;">Error loading editor. Please check console for details.</div>';
        }
    }
}

function loadMonacoEditor() {
    // Fallback loader
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs/loader.js';
    script.onload = function() {
        require.config({ paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' } });
        require(['vs/editor/editor.main'], function () {
            initMonacoEditor();
        });
    };
    document.head.appendChild(script);
}

function initOtherComponents() {
    // Initialize Socket.IO
    if (typeof io !== 'undefined') {
        socket = io();
        socket.on('connect', (data) => {
            console.log('Connected to server');
            if (data && data.session_id) {
                currentSessionId = data.session_id;
            }
        });

        socket.on('connected', (data) => {
            if (data && data.session_id) {
                currentSessionId = data.session_id;
                console.log('Session ID:', currentSessionId);
            }
        });

        socket.on('terminal_output', (data) => {
            appendTerminalOutput(data.output);
        });

        // Handle file creation from AI
        socket.on('open_file_in_editor', (data) => {
            console.log('Received open_file_in_editor event:', data);
            if (data && data.path && data.content) {
                openFileInEditor(data.path, data.content, data.language);
            }
        });

        // Show terminal panel when commands are executed
        socket.on('show_terminal', (data) => {
            const terminalPanel = document.getElementById('terminal-panel');
            if (terminalPanel) {
                terminalPanel.style.display = 'flex';
                // Switch to terminal tab
                const terminalTab = document.querySelector('.terminal-tab[data-tab="terminal"]');
                if (terminalTab) {
                    terminalTab.click();
                }
                // Scroll terminal to bottom
                setTimeout(() => {
                    const terminalOutput = document.getElementById('terminal-output');
                    if (terminalOutput) {
                        terminalOutput.scrollTop = terminalOutput.scrollHeight;
                    }
                }, 100);
            }
        });

        // Real-time AI progress updates
        socket.on('ai_progress', (data) => {
            handleAIProgress(data.message, data.data);
        });

        socket.on('file_explored', (data) => {
            handleFileExplored(data.file, data.lines);
        });

        socket.on('code_diff', (data) => {
            handleCodeDiff(data.file, data.old_content, data.new_content);
        });

        // Browser control events
        socket.on('browser_navigate', (data) => {
            if (data && data.url) {
                navigateToUrl(data.url);
            }
        });

        socket.on('browser_screenshot_request', (data) => {
            // Request screenshot (would need canvas API or server-side screenshot)
            console.log('Browser screenshot requested');
        });

        socket.on('browser_get_url', (data) => {
            // Return current URL
            aiBrowserGetUrl().then(result => {
                console.log('Current browser URL:', result);
            });
        });

        socket.on('browser_execute_script', (data) => {
            if (data && data.script) {
                const frame = document.getElementById('browser-preview-frame');
                if (frame && frame.contentWindow) {
                    try {
                        frame.contentWindow.eval(data.script);
                        console.log('Script executed in browser preview');
                    } catch (e) {
                        console.error('Script execution error (CORS may block):', e);
                    }
                }
            }
        });
    } else {
        console.warn('Socket.IO not loaded');
    }

    // Initialize Activity Bar
    setTimeout(() => {
        const activityIcons = document.querySelectorAll('.activity-icon');
        if (activityIcons.length > 0) {
            activityIcons.forEach(icon => {
                icon.addEventListener('click', () => {
                    const view = icon.dataset.view;
                    switchView(view);
                    
                    document.querySelectorAll('.activity-icon').forEach(i => i.classList.remove('active'));
                    icon.classList.add('active');
                });
            });
            console.log('Activity bar initialized');
        }
        
        // Initialize resize handles
        initResizeHandles();
        
        // Load workspace
        loadWorkspace();
        switchView('explorer');
        
        // Load settings
        loadSettings();
    }, 100);
}

function initResizeHandles() {
    // Sidebar resize
    const sidebarResize = document.getElementById('sidebar-resize');
    const sidebarContent = document.getElementById('sidebar-content');
    
    if (sidebarResize && sidebarContent) {
        let isResizing = false;
        let startX = 0;
        let startWidth = 0;
        
        sidebarResize.addEventListener('mousedown', (e) => {
            isResizing = true;
            startX = e.clientX;
            startWidth = parseInt(window.getComputedStyle(sidebarContent).width, 10);
            document.body.style.cursor = 'col-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });
        
        let resizeTimeout;
        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            
            const width = startWidth + (e.clientX - startX);
            const minWidth = 200;
            const maxWidth = 600;
            
            if (width >= minWidth && width <= maxWidth) {
                sidebarContent.style.width = width + 'px';
                
                // Throttle editor layout updates
                clearTimeout(resizeTimeout);
                resizeTimeout = setTimeout(() => {
                    localStorage.setItem('sidebarWidth', width);
                    if (editor) {
                        editor.layout();
                    }
                }, 100);
            }
        });
        
        document.addEventListener('mouseup', () => {
            if (isResizing) {
                isResizing = false;
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        });
        
        // Load saved width
        const savedWidth = localStorage.getItem('sidebarWidth');
        if (savedWidth) {
            sidebarContent.style.width = savedWidth + 'px';
        }
    }
    
    // Terminal resize
    const terminalResize = document.getElementById('terminal-resize');
    const terminalPanel = document.getElementById('terminal-panel');
    
    if (terminalResize && terminalPanel) {
        let isResizing = false;
        let startY = 0;
        let startHeight = 0;
        
        terminalResize.addEventListener('mousedown', (e) => {
            isResizing = true;
            startY = e.clientY;
            startHeight = parseInt(window.getComputedStyle(terminalPanel).height, 10);
            document.body.style.cursor = 'row-resize';
            document.body.style.userSelect = 'none';
            e.preventDefault();
        });
        
        let terminalResizeTimeout;
        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            
            const height = startHeight - (e.clientY - startY);
            const minHeight = 150;
            const maxHeight = window.innerHeight * 0.8;
            
            if (height >= minHeight && height <= maxHeight) {
                terminalPanel.style.height = height + 'px';
                
                // Throttle localStorage updates
                clearTimeout(terminalResizeTimeout);
                terminalResizeTimeout = setTimeout(() => {
                    localStorage.setItem('terminalHeight', height);
                }, 100);
            }
        });
        
        document.addEventListener('mouseup', () => {
            if (isResizing) {
                isResizing = false;
                document.body.style.cursor = '';
                document.body.style.userSelect = '';
            }
        });
        
        // Load saved height
        const savedHeight = localStorage.getItem('terminalHeight');
        if (savedHeight) {
            terminalPanel.style.height = savedHeight + 'px';
        }
    }
}

// These are now initialized in initOtherComponents()

function switchView(viewName) {
    document.querySelectorAll('.view').forEach(view => view.classList.remove('active'));
    const targetView = document.getElementById(viewName + '-view');
    if (targetView) {
        targetView.classList.add('active');
        
        if (viewName === 'explorer') {
            loadWorkspace();
        } else if (viewName === 'todos') {
            loadTodos();
        } else if (viewName === 'git') {
            loadGitStatus();
        } else if (viewName === 'extensions') {
            loadExtensions();
        } else if (viewName === 'settings') {
            loadSettings();
        } else if (viewName === 'ai') {
            // Load toolkit status when AI view is opened
            setTimeout(() => refreshToolkitStatus(), 100);
        } else if (viewName === 'browser') {
            showBrowserPreview();
        } else {
            hideBrowserPreview();
        }
    }
}

// Workspace Management
async function loadWorkspace() {
    try {
        const response = await fetch('/api/workspace/get');
        const data = await response.json();
        currentWorkspace = data.path;
        loadFileTree(currentWorkspace);
    } catch (error) {
        console.error('Error loading workspace:', error);
    }
}

async function loadFileTree(path) {
    const treeElement = document.getElementById('file-tree');
    treeElement.innerHTML = '<div class="loading">Loading...</div>';
    
    try {
        const response = await fetch('/api/files/list?path=' + encodeURIComponent(path));
        const data = await response.json();
        
        if (data.items) {
            treeElement.innerHTML = '';
            data.items.forEach(item => {
                const itemElement = createFileTreeItem(item);
                treeElement.appendChild(itemElement);
            });
        }
    } catch (error) {
        treeElement.innerHTML = '<div class="loading">Error: ' + error.message + '</div>';
    }
}

function createFileTreeItem(item) {
    const div = document.createElement('div');
    div.className = 'file-tree-item';
    const icon = item.type === 'directory' ? 'F' : 'F';
    div.innerHTML = '<div class="file-tree-icon">' + icon + '</div><div class="file-tree-name">' + item.name + '</div>';
    
    div.addEventListener('click', () => {
        if (item.type === 'file') {
            openFile(item.path);
        } else {
            loadFileTree(item.path);
        }
    });
    
    return div;
}

function refreshExplorer() {
    if (currentWorkspace) {
        loadFileTree(currentWorkspace);
    }
}

// File Operations
async function openFile(filePath) {
    try {
        if (currentFiles[filePath]) {
            switchToTab(filePath);
            return;
        }
        
        const response = await fetch('/api/files/read', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ path: filePath })
        });
        
        const data = await response.json();
        if (data.content !== undefined) {
            addTab(filePath, data.content);
            const language = detectLanguage(filePath);
            editor.setModel(monaco.editor.createModel(data.content, language, monaco.Uri.file(filePath)));
            currentFiles[filePath] = {
                path: filePath,
                content: data.content,
                modified: false
            };
        }
    } catch (error) {
        console.error('Error opening file:', error);
        alert('Error opening file: ' + error.message);
    }
}

function detectLanguage(filePath) {
    const ext = filePath.split('.').pop().toLowerCase();
    const languageMap = {
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        'py': 'python',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'cs': 'csharp',
        'php': 'php',
        'rb': 'ruby',
        'go': 'go',
        'rs': 'rust',
        'html': 'html',
        'css': 'css',
        'scss': 'scss',
        'json': 'json',
        'xml': 'xml',
        'yaml': 'yaml',
        'yml': 'yaml',
        'md': 'markdown',
        'sh': 'shell',
        'bat': 'batch',
        'ps1': 'powershell'
    };
    return languageMap[ext] || 'plaintext';
}

// Tab Management
// Open file in editor with content (for AI-generated files)
function openFileInEditor(filePath, content, language) {
    // Store file content
    if (!currentFiles[filePath]) {
        currentFiles[filePath] = { content: content, modified: false };
    } else {
        currentFiles[filePath].content = content;
    }
    
    // Add tab if not exists
    const escapedPath = filePath.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    if (!document.querySelector(`.tab[data-path="${escapedPath}"]`)) {
        addTab(filePath, content);
    } else {
        // Update existing tab content
        switchToTab(filePath);
        if (editor) {
            editor.setValue(content);
        }
    }
    
    // Set language if provided
    if (language && editor && editor.getModel()) {
        const langMap = {
            'python': 'python',
            'js': 'javascript',
            'javascript': 'javascript',
            'html': 'html',
            'css': 'css',
            'json': 'json',
            'xml': 'xml',
            'yaml': 'yaml',
            'md': 'markdown',
            'markdown': 'markdown',
            'sh': 'shell',
            'bash': 'shell',
            'powershell': 'powershell',
            'cmd': 'bat'
        };
        const monacoLang = langMap[language.toLowerCase()] || language.toLowerCase();
        try {
            monaco.editor.setModelLanguage(editor.getModel(), monacoLang);
        } catch (e) {
            console.log('Language not supported:', monacoLang);
        }
    }
    
    // Switch to editor view
    setTimeout(() => {
        switchView('explorer');
    }, 100);
    
    // Show notification
    const statusText = document.getElementById('terminal-status-text');
    if (statusText) {
        statusText.textContent = `✅ File created: ${filePath.split(/[/\\]/).pop()}`;
        statusText.style.color = '#4ec9b0';
        const statusEl = document.getElementById('terminal-status');
        if (statusEl) {
            statusEl.style.display = 'block';
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 3000);
        }
    }
}

function addTab(filePath, content) {
    const tabBar = document.getElementById('tab-bar');
    const fileName = filePath.split(/[/\\]/).pop();
    
    const tab = document.createElement('div');
    tab.className = 'tab';
    tab.dataset.path = filePath;
    tab.innerHTML = '<span>' + fileName + '</span><span class="tab-close" onclick="closeTab(\'' + filePath + '\')">x</span>';
    
    tab.addEventListener('click', () => switchToTab(filePath));
    
    tabBar.appendChild(tab);
    switchToTab(filePath);
}

function switchToTab(filePath) {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.path === filePath) {
            tab.classList.add('active');
        }
    });
    
    if (currentFiles[filePath]) {
        const model = monaco.editor.createModel(
            currentFiles[filePath].content,
            detectLanguage(filePath),
            monaco.Uri.file(filePath)
        );
        editor.setModel(model);
    }
}

function updateTab(filePath) {
    const tab = document.querySelector('.tab[data-path="' + filePath + '"]');
    if (tab && currentFiles[filePath] && currentFiles[filePath].modified) {
        const fileName = filePath.split(/[/\\]/).pop();
        tab.querySelector('span').textContent = fileName + ' *';
    }
}

async function closeTab(filePath) {
    if (currentFiles[filePath] && currentFiles[filePath].modified) {
        if (!confirm('File has unsaved changes. Close anyway?')) {
            return;
        }
    }
    
    delete currentFiles[filePath];
    const tab = document.querySelector('.tab[data-path="' + filePath + '"]');
    if (tab) {
        tab.remove();
    }
    
    const remainingTabs = document.querySelectorAll('.tab');
    if (remainingTabs.length > 0) {
        const nextTab = remainingTabs[remainingTabs.length - 1];
        switchToTab(nextTab.dataset.path);
    } else {
        editor.setModel(monaco.editor.createModel('', 'plaintext'));
    }
}

// Save File
async function saveFile(filePath) {
    if (!currentFiles[filePath]) return;
    
    try {
        const response = await fetch('/api/files/write', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                path: filePath,
                content: editor.getValue()
            })
        });
        
        const data = await response.json();
        if (data.success) {
            currentFiles[filePath].modified = false;
            updateTab(filePath);
        }
    } catch (error) {
        console.error('Error saving file:', error);
        alert('Error saving file: ' + error.message);
    }
}

// Terminal
function toggleTerminal() {
    const panel = document.getElementById('terminal-panel');
    if (!panel) {
        console.error('Terminal panel not found');
        return;
    }
    
    const isHidden = panel.style.display === 'none' || !panel.style.display;
    panel.style.display = isHidden ? 'flex' : 'none';
    
    // Focus input when opening
    if (isHidden) {
        setTimeout(() => {
            const input = document.getElementById('terminal-input');
            if (input) {
                input.focus();
            }
        }, 100);
    }
}

function appendTerminalOutput(output) {
    // Ensure terminal panel is visible
    const terminalPanel = document.getElementById('terminal-panel');
    if (terminalPanel) {
        if (terminalPanel.style.display === 'none' || terminalPanel.style.display === '') {
            terminalPanel.style.display = 'flex';
        }
        // Switch to terminal tab if not already active
        const terminalTab = document.querySelector('.terminal-tab[data-tab="terminal"]');
        if (terminalTab && !terminalTab.classList.contains('active')) {
            terminalTab.click();
        }
    }
    
    const outputElement = document.getElementById('terminal-output');
    if (outputElement) {
        // Append output (preserve existing newlines)
        const text = output.endsWith('\n') ? output : output + '\n';
        outputElement.textContent += text;
        // Auto-scroll to bottom
        outputElement.scrollTop = outputElement.scrollHeight;
    }
}

async function handleTerminalKeyPress(event) {
    if (event.key === 'Enter') {
        const input = document.getElementById('terminal-input');
        if (!input) {
            console.error('Terminal input not found');
            return;
        }
        
        const command = input.value.trim();
        if (!command) {
            return; // Don't execute empty commands
        }
        
        appendTerminalOutput('$ ' + command);
        input.value = '';
        
        // Show live status on dashboard
        const statusEl = document.getElementById('terminal-status');
        const statusText = document.getElementById('terminal-status-text');
        if (statusEl && statusText) {
            statusEl.style.display = 'block';
            statusText.textContent = 'Executing: ' + command;
            statusText.style.color = '#4ec9b0';
        }
        
        try {
            const response = await fetch('/api/terminal/execute', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    command: command,
                    working_dir: currentWorkspace || undefined
                })
            });
            
            const data = await response.json();
            
            if (data.output !== undefined) {
                appendTerminalOutput(data.output);
                // Update status with result
                if (statusText) {
                    statusText.textContent = data.success !== false ? '✓ Command completed' : '✗ Command failed';
                    statusText.style.color = data.success !== false ? '#4ec9b0' : '#f48771';
                    setTimeout(() => {
                        if (statusEl) statusEl.style.display = 'none';
                    }, 3000);
                }
            } else if (data.error) {
                appendTerminalOutput('Error: ' + data.error);
                if (statusText) {
                    statusText.textContent = '✗ Error: ' + data.error;
                    statusText.style.color = '#f48771';
                    setTimeout(() => {
                        if (statusEl) statusEl.style.display = 'none';
                    }, 5000);
                }
            } else {
                appendTerminalOutput('No output from command');
            }
        } catch (error) {
            console.error('Terminal execution error:', error);
            appendTerminalOutput('Error: ' + error.message);
            if (statusText) {
                statusText.textContent = '✗ Error: ' + error.message;
                statusText.style.color = '#f48771';
                setTimeout(() => {
                    if (statusEl) statusEl.style.display = 'none';
                }, 5000);
            }
        }
        
        // Refocus input
        setTimeout(() => {
            if (input) input.focus();
        }, 50);
    }
}

// Real-time progress handlers
function handleAIProgress(message, data) {
    // Update progress in chat or status bar
    const progressId = 'progress-' + Date.now();
    const progressEl = addProgressMessage(message, progressId);
    
    // Update status bar if available
    const statusText = document.getElementById('terminal-status-text');
    if (statusText) {
        statusText.textContent = message;
        statusText.style.color = '#4ec9b0';
    }
}

function handleFileExplored(filePath, lines) {
    fileExplorationCount++;
    const fileName = filePath.split(/[/\\]/).pop();
    const message = `📁 Read ${fileName}${lines ? ` (${lines})` : ''}`;
    handleAIProgress(message, { file: filePath, lines: lines });
}

function handleCodeDiff(filePath, oldContent, newContent) {
    const fileName = filePath.split(/[/\\]/).pop();
    const diffId = 'diff-' + Date.now();
    const diffEl = createDiffView(filePath, fileName, oldContent, newContent, diffId);
    
    // Add to chat messages
    const messagesContainer = document.getElementById('chat-messages');
    if (messagesContainer) {
        messagesContainer.appendChild(diffEl);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

function addProgressMessage(message, messageId) {
    const messagesContainer = document.getElementById('chat-messages');
    if (!messagesContainer) return null;
    
    // Remove previous progress messages of the same type
    const existing = document.getElementById(messageId);
    if (existing) existing.remove();
    
    const progressDiv = document.createElement('div');
    progressDiv.id = messageId;
    progressDiv.className = 'chat-message progress-message';
    progressDiv.innerHTML = `<span class="progress-indicator">⏳</span> ${message}`;
    
    messagesContainer.appendChild(progressDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return progressDiv;
}

function createDiffView(filePath, fileName, oldContent, newContent, diffId) {
    const diffContainer = document.createElement('div');
    diffContainer.id = diffId;
    diffContainer.className = 'code-diff-container';
    
    // Calculate line counts
    const oldLines = oldContent.split('\n');
    const newLines = newContent.split('\n');
    const oldLineCount = oldLines.length;
    const newLineCount = newLines.length;
    
    // Header
    const header = document.createElement('div');
    header.className = 'diff-header';
    header.innerHTML = `
        <span class="diff-file-name">${fileName}</span>
        <span class="diff-stats">+${newLineCount} -${oldLineCount}</span>
    `;
    diffContainer.appendChild(header);
    
    // Diff content
    const diffContent = document.createElement('div');
    diffContent.className = 'diff-content';
    
    // Create side-by-side diff view
    const diffView = document.createElement('div');
    diffView.className = 'diff-view';
    
    // Old content (left)
    const oldView = document.createElement('div');
    oldView.className = 'diff-old';
    const oldPre = document.createElement('pre');
    oldPre.className = 'diff-code';
    oldPre.textContent = oldContent;
    oldView.appendChild(oldPre);
    
    // New content (right)
    const newView = document.createElement('div');
    newView.className = 'diff-new';
    const newPre = document.createElement('pre');
    newPre.className = 'diff-code';
    newPre.textContent = newContent;
    newView.appendChild(newPre);
    
    diffView.appendChild(oldView);
    diffView.appendChild(newView);
    diffContent.appendChild(diffView);
    diffContainer.appendChild(diffContent);
    
    return diffContainer;
}

// AI Chat
async function sendChatMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    addChatMessage('user', message);
    input.value = '';
    
    // Reset progress tracking
    fileExplorationCount = 0;
    activeProgressUpdates = {};
    
    const typingId = addChatMessage('ai', '🤖 Thinking...');
    
    // Show execution status
    const statusEl = document.getElementById('terminal-status');
    const statusText = document.getElementById('terminal-status-text');
    if (statusEl && statusText) {
        statusEl.style.display = 'block';
        statusText.textContent = '🤖 AI processing request...';
        statusText.style.color = '#4ec9b0';
    }
    
    try {
        const response = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'X-Session-ID': currentSessionId || 'default'
            },
            body: JSON.stringify({
                message: message,
                context: {
                    currentFile: Object.keys(currentFiles)[0] || null,
                    workspace: currentWorkspace
                }
            })
        });
        
        const data = await response.json();
        
        removeChatMessage(typingId);
        
        if (data.success) {
            // Check if commands were executed
            if (data.executed_commands && data.executed_commands > 0) {
                statusText.textContent = `✅ Executed ${data.executed_commands} command(s)`;
                statusText.style.color = '#4ec9b0';
                setTimeout(() => {
                    if (statusEl) statusEl.style.display = 'none';
                }, 5000);
            } else {
                if (statusEl) statusEl.style.display = 'none';
            }
            
            // Format response with code highlighting
            let formattedResponse = data.response || '';
            
            // If response is empty, show a message
            if (!formattedResponse || formattedResponse.trim() === '') {
                formattedResponse = '🤖 AI processed your request but returned no text response.';
            }
            
            // Highlight code blocks
            formattedResponse = formattedResponse.replace(
                /```(\w+)?\n([\s\S]+?)```/g,
                '<pre class="code-block"><code>$2</code></pre>'
            );
            
            // Highlight commands
            formattedResponse = formattedResponse.replace(
                /\[EXECUTE:\s*(.+?)\]/gi,
                '<span class="command-marker">🔧 EXECUTING: $1</span>'
            );
            
            addChatMessage('ai', formattedResponse);
        } else {
            if (statusEl) statusEl.style.display = 'none';
            addChatMessage('ai', data.response || 'Sorry, I could not process that request.');
        }
    } catch (error) {
        removeChatMessage(typingId);
        if (statusEl && statusText) {
            statusText.textContent = '❌ Error: ' + error.message;
            statusText.style.color = '#f48771';
            setTimeout(() => {
                if (statusEl) statusEl.style.display = 'none';
            }, 5000);
        }
        addChatMessage('ai', 'Error: ' + error.message);
    }
}

function addChatMessage(type, content) {
    const messagesContainer = document.getElementById('chat-messages');
    const messageId = 'msg-' + Date.now();
    const messageDiv = document.createElement('div');
    messageDiv.id = messageId;
    messageDiv.className = 'chat-message ' + type;
    
    // Support HTML content for formatted messages
    if (type === 'ai' && (content.includes('<pre') || content.includes('<span class="command-marker"') || content.includes('EXECUTING:') || content.includes('COMMAND EXECUTION'))) {
        messageDiv.innerHTML = content;
    } else {
        messageDiv.textContent = content;
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return messageId;
}

function removeChatMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

function handleChatKeyPress(event) {
    if (event.key === 'Enter') {
        sendChatMessage();
    }
}

// Todos
async function loadTodos() {
    try {
        const response = await fetch('/api/todos/list');
        const data = await response.json();
        
        const todosList = document.getElementById('todos-list');
        todosList.innerHTML = '';
        
        if (data.todos && data.todos.length > 0) {
            data.todos.forEach(todo => {
                const todoElement = createTodoElement(todo);
                todosList.appendChild(todoElement);
            });
        } else {
            todosList.innerHTML = '<div class="loading">No todos yet</div>';
        }
    } catch (error) {
        console.error('Error loading todos:', error);
    }
}

function createTodoElement(todo) {
    const div = document.createElement('div');
    div.className = 'todo-item ' + (todo.status === 'completed' ? 'completed' : '');
    div.innerHTML = '<input type="checkbox" class="todo-checkbox" ' + (todo.status === 'completed' ? 'checked' : '') + ' onchange="toggleTodo(' + todo.id + ', this.checked)"><span class="todo-content">' + todo.content + '</span><button class="todo-delete" onclick="deleteTodo(' + todo.id + ')">x</button>';
    return div;
}

async function addTodo() {
    const input = document.getElementById('new-todo-input');
    const content = input.value.trim();
    
    if (!content) return;
    
    try {
        const response = await fetch('/api/todos/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: content })
        });
        
        const data = await response.json();
        if (data.success) {
            input.value = '';
            loadTodos();
        }
    } catch (error) {
        console.error('Error adding todo:', error);
    }
}

async function toggleTodo(todoId, completed) {
    try {
        await fetch('/api/todos/update', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                id: todoId,
                status: completed ? 'completed' : 'pending'
            })
        });
        loadTodos();
    } catch (error) {
        console.error('Error updating todo:', error);
    }
}

async function deleteTodo(todoId) {
    try {
        await fetch('/api/todos/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: todoId })
        });
        loadTodos();
    } catch (error) {
        console.error('Error deleting todo:', error);
    }
}

function handleTodoKeyPress(event) {
    if (event.key === 'Enter') {
        addTodo();
    }
}

function refreshTodos() {
    loadTodos();
}

// Git
async function loadGitStatus() {
    try {
        const response = await fetch('/api/git/status');
        const data = await response.json();
        
        const gitInfo = document.getElementById('git-info');
        if (data.status) {
            gitInfo.textContent = data.status;
        } else if (data.error) {
            gitInfo.textContent = 'Error: ' + data.error;
        } else {
            gitInfo.textContent = 'Not a git repository';
        }
    } catch (error) {
        document.getElementById('git-info').textContent = 'Error: ' + error.message;
    }
}

function refreshGitStatus() {
    loadGitStatus();
}

// Extensions
let extensionTab = 'installed';

async function loadExtensions() {
    try {
        const response = await fetch('/api/extensions/list');
        const data = await response.json();
        
        const extensionsList = document.getElementById('extensions-list');
        extensionsList.innerHTML = '';
        
        if (data.extensions && data.extensions.length > 0) {
            data.extensions.forEach(ext => {
                const extElement = createExtensionElement(ext, 'installed');
                extensionsList.appendChild(extElement);
            });
        } else {
            extensionsList.innerHTML = '<div class="loading">No extensions installed</div>';
        }
    } catch (error) {
        console.error('Error loading extensions:', error);
    }
}

function createExtensionElement(ext, type) {
    const div = document.createElement('div');
    div.className = 'extension-item';
    const manifest = ext.manifest || {};
    const enabled = ext.enabled !== false;
    
    // Get extension details
    const name = manifest.displayName || ext.name || ext.id;
    const publisher = manifest.publisher || ext.publisher || 'Unknown';
    const description = manifest.description || ext.description || 'No description';
    const version = manifest.version || ext.version || '1.0.0';
    const downloads = ext.downloads || 0;
    const rating = ext.rating || 0;
    
    div.innerHTML = '<div class="extension-header"><div class="extension-info"><h4>' + 
        name + '</h4><p class="extension-publisher">' + publisher + '</p>' +
        (description ? '<p class="extension-description">' + description.substring(0, 150) + (description.length > 150 ? '...' : '') + '</p>' : '') +
        '</div><div class="extension-actions">' +
        (type === 'installed' ? 
            '<button class="ext-btn" onclick="toggleExtension(\'' + ext.id + '\', ' + !enabled + ')">' +
            (enabled ? 'Disable' : 'Enable') + '</button>' +
            '<button class="ext-btn ext-btn-danger" onclick="uninstallExtension(\'' + ext.id + '\')">Uninstall</button>' :
            '<button class="ext-btn ext-btn-primary" onclick="installExtension(\'' + ext.id + '\')">Install</button>') +
        '</div></div><div class="extension-details">' +
        '<span class="extension-version">v' + version + '</span>' +
        (downloads > 0 ? '<span class="extension-downloads">' + (downloads > 1000 ? (downloads/1000).toFixed(1) + 'k' : downloads) + ' downloads</span>' : '') +
        (rating > 0 ? '<span class="extension-rating">★ ' + rating.toFixed(1) + '</span>' : '') +
        (manifest.engines ? '<span class="extension-engine">VS Code ' + (manifest.engines.vscode || 'any') + '</span>' : '') +
        '</div>';
    return div;
}

async function searchExtensions() {
    const query = document.getElementById('extension-search-input').value.trim();
    if (!query) return;
    
    try {
        const response = await fetch('/api/extensions/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query, limit: 50 })
        });
        
        const data = await response.json();
        const extensionsList = document.getElementById('extensions-list');
        extensionsList.innerHTML = '';
        
        if (data.extensions && data.extensions.length > 0) {
            data.extensions.forEach(ext => {
                const extElement = createExtensionElement(ext, 'marketplace');
                extensionsList.appendChild(extElement);
            });
        } else {
            extensionsList.innerHTML = '<div class="loading">No extensions found</div>';
        }
    } catch (error) {
        console.error('Error searching extensions:', error);
    }
}

async function installExtension(extensionId) {
    // Find the extension element to show progress
    const extElements = document.querySelectorAll('.extension-item');
    let extElement = null;
    for (const el of extElements) {
        if (el.textContent.includes(extensionId)) {
            extElement = el;
            break;
        }
    }
    
    // Show installing state
    if (extElement) {
        const installBtn = extElement.querySelector('.ext-btn-primary');
        if (installBtn) {
            installBtn.textContent = 'Installing...';
            installBtn.disabled = true;
        }
    }
    
    // Show status on dashboard
    const statusEl = document.getElementById('terminal-status');
    const statusText = document.getElementById('terminal-status-text');
    statusEl.style.display = 'block';
    statusText.textContent = 'Installing extension: ' + extensionId;
    statusText.style.color = '#4ec9b0';
    
    try {
        const response = await fetch('/api/extensions/install', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: extensionId })
        });
        
        const data = await response.json();
        if (data.success) {
            // Update button
            if (extElement && installBtn) {
                installBtn.textContent = 'Installed';
                installBtn.style.background = '#4ec9b0';
                installBtn.disabled = true;
            }
            
            // Show success on dashboard
            statusText.textContent = '✓ Extension installed: ' + extensionId;
            statusText.style.color = '#4ec9b0';
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 3000);
            
            // Reload extensions list
            if (extensionTab === 'installed') {
                setTimeout(() => loadExtensions(), 1000);
            }
        } else {
            // Show error
            if (extElement && installBtn) {
                installBtn.textContent = 'Install';
                installBtn.disabled = false;
            }
            
            statusText.textContent = '✗ Installation failed: ' + (data.error || 'Unknown error');
            statusText.style.color = '#f48771';
            setTimeout(() => {
                statusEl.style.display = 'none';
            }, 5000);
            
            alert('Installation failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        if (extElement) {
            const installBtn = extElement.querySelector('.ext-btn-primary');
            if (installBtn) {
                installBtn.textContent = 'Install';
                installBtn.disabled = false;
            }
        }
        
        statusText.textContent = '✗ Error: ' + error.message;
        statusText.style.color = '#f48771';
        setTimeout(() => {
            statusEl.style.display = 'none';
        }, 5000);
        
        alert('Error installing extension: ' + error.message);
    }
}

async function uninstallExtension(extensionId) {
    if (!confirm('Uninstall ' + extensionId + '?')) return;
    
    try {
        const response = await fetch('/api/extensions/uninstall', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: extensionId })
        });
        
        const data = await response.json();
        if (data.success) {
            loadExtensions();
        } else {
            alert('Uninstall failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Error uninstalling extension: ' + error.message);
    }
}

async function toggleExtension(extensionId, enable) {
    try {
        const endpoint = enable ? '/api/extensions/enable' : '/api/extensions/disable';
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: extensionId })
        });
        
        const data = await response.json();
        if (data.success) {
            loadExtensions();
        }
    } catch (error) {
        console.error('Error toggling extension:', error);
    }
}

function switchExtensionTab(tab) {
    extensionTab = tab;
    document.querySelectorAll('.ext-tab').forEach(t => {
        t.classList.remove('active');
        if (t.textContent.toLowerCase().includes(tab)) {
            t.classList.add('active');
        }
    });
    
    if (tab === 'installed') {
        loadExtensions();
    } else {
        document.getElementById('extensions-list').innerHTML = '<div class="loading">Search for extensions above</div>';
    }
}

function handleExtensionSearchKeyPress(event) {
    if (event.key === 'Enter') {
        searchExtensions();
    }
}

function refreshExtensions() {
    if (extensionTab === 'installed') {
        loadExtensions();
    } else {
        searchExtensions();
    }
}

// Menu handlers
function showMenu(menuName) {
    if (menuName === 'terminal') {
        toggleTerminal();
    } else if (menuName === 'file') {
        // File menu actions
        console.log('File menu clicked');
    } else if (menuName === 'edit') {
        // Edit menu actions
        console.log('Edit menu clicked');
    } else if (menuName === 'view') {
        // View menu actions
        console.log('View menu clicked');
    } else if (menuName === 'run') {
        // Run menu actions
        console.log('Run menu clicked');
    } else if (menuName === 'help') {
        // Help menu actions
        alert('Auto_Punch IDE\n\nPowered by Auto_Punch Ai\n\nKeyboard Shortcuts:\n- Ctrl+` : Toggle Terminal\n- Ctrl+S : Save File');
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) {
            saveFile(activeTab.dataset.path);
        }
    }
    
    if (e.ctrlKey && e.key === '`') {
        e.preventDefault();
        toggleTerminal();
    }
});

// Settings
function loadSettings() {
    // Load saved settings from localStorage
    const theme = localStorage.getItem('theme') || 'default';
    const fontSize = localStorage.getItem('fontSize') || '14';
    const animations = localStorage.getItem('animations') !== 'false';
    const wordWrap = localStorage.getItem('wordWrap') !== 'false';
    const lineNumbers = localStorage.getItem('lineNumbers') !== 'false';
    const minimap = localStorage.getItem('minimap') !== 'false';
    const tabSize = localStorage.getItem('tabSize') || '4';
    const shell = localStorage.getItem('shell') || 'powershell';
    const terminalStatus = localStorage.getItem('terminalStatus') !== 'false';
    const aiModel = localStorage.getItem('aiModel') || 'hacxgpt';
    const aiAutoExec = localStorage.getItem('aiAutoExec') !== 'false';
    const autoSave = localStorage.getItem('autoSave') === 'true';
    const overlayOpacity = localStorage.getItem('overlayOpacity') || '40';
    const showLogo = localStorage.getItem('showLogo') === 'true';
    
    // Apply settings
    if (document.getElementById('theme-select')) document.getElementById('theme-select').value = theme;
    if (document.getElementById('font-size-slider')) {
        document.getElementById('font-size-slider').value = fontSize;
        document.getElementById('font-size-value').textContent = fontSize + 'px';
    }
    if (document.getElementById('animations-toggle')) document.getElementById('animations-toggle').checked = animations;
    if (document.getElementById('word-wrap-toggle')) document.getElementById('word-wrap-toggle').checked = wordWrap;
    if (document.getElementById('line-numbers-toggle')) document.getElementById('line-numbers-toggle').checked = lineNumbers;
    if (document.getElementById('minimap-toggle')) document.getElementById('minimap-toggle').checked = minimap;
    if (document.getElementById('tab-size-input')) document.getElementById('tab-size-input').value = tabSize;
    if (document.getElementById('shell-select')) document.getElementById('shell-select').value = shell;
    if (document.getElementById('terminal-status-toggle')) document.getElementById('terminal-status-toggle').checked = terminalStatus;
    if (document.getElementById('ai-model-select')) document.getElementById('ai-model-select').value = aiModel;
    if (document.getElementById('ai-auto-exec-toggle')) document.getElementById('ai-auto-exec-toggle').checked = aiAutoExec;
    if (document.getElementById('auto-save-toggle')) document.getElementById('auto-save-toggle').checked = autoSave;
    if (document.getElementById('overlay-opacity-slider')) {
        document.getElementById('overlay-opacity-slider').value = overlayOpacity;
        document.getElementById('overlay-opacity-value').textContent = overlayOpacity + '%';
    }
    if (document.getElementById('logo-toggle')) document.getElementById('logo-toggle').checked = showLogo;
    
    // Apply theme
    changeTheme(theme);
    
    // Apply logo
    toggleLogo(showLogo);
}

function toggleLogo(enabled) {
    localStorage.setItem('showLogo', enabled);
    const logo = document.getElementById('menu-logo');
    const logoImage = document.getElementById('logo-image');
    
    if (logo) {
        if (enabled) {
            logo.style.display = 'flex';
            // Check if image exists
            if (logoImage) {
                // Force reload to check if image exists
                const currentSrc = logoImage.src.split('?')[0];
                logoImage.src = currentSrc + '?v=' + Date.now();
                
                logoImage.onload = function() {
                    logo.style.display = 'flex';
                    console.log('Logo image loaded successfully');
                };
                
                logoImage.onerror = function() {
                    console.warn('Logo image not found, hiding logo');
                    logo.style.display = 'none';
                };
            }
        } else {
            logo.style.display = 'none';
        }
    }
}

function changeTheme(theme) {
    localStorage.setItem('theme', theme);
    document.body.className = '';
    
    // Show/hide overlay opacity setting
    const overlaySetting = document.getElementById('overlay-opacity-setting');
    if (overlaySetting) {
        overlaySetting.style.display = theme === 'hacking' ? 'block' : 'none';
    }
    
    if (theme === 'hacking') {
        document.body.classList.add('theme-hacking');
        // Load saved overlay opacity
        const opacity = localStorage.getItem('overlayOpacity') || '40';
        changeOverlayOpacity(opacity);
    } else if (theme === 'dark') {
        document.body.style.background = '#1e1e1e';
        document.body.style.color = '#cccccc';
    } else if (theme === 'light') {
        document.body.style.background = '#ffffff';
        document.body.style.color = '#333333';
    }
}

function changeOverlayOpacity(value) {
    localStorage.setItem('overlayOpacity', value);
    const opacityValue = document.getElementById('overlay-opacity-value');
    if (opacityValue) {
        opacityValue.textContent = value + '%';
    }
    
    // Convert percentage to decimal (0-1 range)
    const opacity = value / 100;
    
    // Update CSS variable on root element
    document.documentElement.style.setProperty('--hack-overlay-opacity', opacity);
    
    // Force re-render by toggling a class
    const body = document.body;
    if (body.classList.contains('theme-hacking')) {
        body.classList.remove('theme-hacking');
        setTimeout(() => {
            body.classList.add('theme-hacking');
        }, 10);
    }
}

function changeFontSize(size) {
    localStorage.setItem('fontSize', size);
    document.getElementById('font-size-value').textContent = size + 'px';
    if (editor) {
        editor.updateOptions({ fontSize: parseInt(size) });
    }
}

function toggleAnimations(enabled) {
    localStorage.setItem('animations', enabled);
    if (!enabled) {
        document.body.style.animation = 'none';
        document.querySelectorAll('*').forEach(el => {
            el.style.animation = 'none';
            el.style.transition = 'none';
        });
    }
}

function toggleWordWrap(enabled) {
    localStorage.setItem('wordWrap', enabled);
    if (editor) {
        editor.updateOptions({ wordWrap: enabled ? 'on' : 'off' });
    }
}

function toggleLineNumbers(enabled) {
    localStorage.setItem('lineNumbers', enabled);
    if (editor) {
        editor.updateOptions({ lineNumbers: enabled ? 'on' : 'off' });
    }
}

function toggleMinimap(enabled) {
    localStorage.setItem('minimap', enabled);
    if (editor) {
        editor.updateOptions({ minimap: { enabled: enabled } });
    }
}

function changeTabSize(size) {
    localStorage.setItem('tabSize', size);
    if (editor) {
        editor.updateOptions({ tabSize: parseInt(size) });
    }
}

function changeShell(shell) {
    localStorage.setItem('shell', shell);
}

function toggleTerminalStatus(enabled) {
    localStorage.setItem('terminalStatus', enabled);
}

function changeAIModel(model) {
    localStorage.setItem('aiModel', model);
}

function toggleAIAutoExec(enabled) {
    localStorage.setItem('aiAutoExec', enabled);
}

function setDefaultWorkspace(path) {
    localStorage.setItem('defaultWorkspace', path);
}

function browseWorkspace() {
    // This would ideally open a file dialog, but for now just prompt
    const path = prompt('Enter workspace path:');
    if (path) {
        document.getElementById('default-workspace-input').value = path;
        setDefaultWorkspace(path);
    }
}

function toggleAutoSave(enabled) {
    localStorage.setItem('autoSave', enabled);
    if (enabled) {
        // Set up auto-save interval
        setInterval(() => {
            const activeTab = document.querySelector('.tab.active');
            if (activeTab && currentFiles[activeTab.dataset.path]) {
                saveFile(activeTab.dataset.path);
            }
        }, 30000); // Auto-save every 30 seconds
    }
}

function handleSettingsSearch(event) {
    if (event.key === 'Enter') {
        const query = event.target.value.toLowerCase();
        const sections = document.querySelectorAll('.settings-section');
        sections.forEach(section => {
            const text = section.textContent.toLowerCase();
            if (text.includes(query)) {
                section.style.display = 'block';
                section.scrollIntoView({ behavior: 'smooth', block: 'center' });
            } else {
                section.style.display = 'none';
            }
        });
    }
}

// Browser Preview Functions
let browserHistory = [];
let browserHistoryIndex = -1;
let currentBrowserUrl = '';

function switchView(view) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    
    // Show selected view
    const viewElement = document.getElementById(view + '-view');
    if (viewElement) {
        viewElement.classList.add('active');
    }
    
    // Handle browser view specially
    if (view === 'browser') {
        showBrowserPreview();
    } else {
        hideBrowserPreview();
    }
}

function showBrowserPreview() {
    const previewPanel = document.getElementById('browser-preview-panel');
    const editor = document.getElementById('monaco-editor');
    if (previewPanel && editor) {
        previewPanel.style.display = 'flex';
        editor.style.display = 'none';
    }
}

function hideBrowserPreview() {
    const previewPanel = document.getElementById('browser-preview-panel');
    const editor = document.getElementById('monaco-editor');
    if (previewPanel && editor) {
        previewPanel.style.display = 'none';
        editor.style.display = 'block';
    }
}

function navigateBrowser() {
    const urlInput = document.getElementById('browser-url-input');
    const previewUrl = document.getElementById('browser-preview-url');
    const frame = document.getElementById('browser-preview-frame');
    const status = document.getElementById('browser-status');
    
    if (!urlInput || !frame) return;
    
    let url = urlInput.value.trim();
    if (!url) return;
    
    // Add protocol if missing
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        // Check if it's a search query or URL
        if (url.includes('.') && !url.includes(' ')) {
            url = 'https://' + url;
        } else {
            url = 'https://www.google.com/search?q=' + encodeURIComponent(url);
        }
    }
    
    currentBrowserUrl = url;
    if (previewUrl) previewUrl.value = url;
    
    // Add to history
    browserHistory.push(url);
    browserHistoryIndex = browserHistory.length - 1;
    
    // Update status
    if (status) {
        status.textContent = `Loading ${url}...`;
        status.style.color = '#4ec9b0';
    }
    
    // Load URL in iframe
    frame.src = url;
    
    // Update status when loaded
    frame.onload = function() {
        if (status) {
            status.textContent = `Loaded: ${url}`;
            status.style.color = '#4ec9b0';
        }
    };
    
    frame.onerror = function() {
        if (status) {
            status.textContent = `Error loading: ${url}`;
            status.style.color = '#f48771';
        }
    };
    
    // Notify AI that browser navigated
    if (socket) {
        socket.emit('browser_navigated', { url: url });
    }
}

function browserBack() {
    if (browserHistoryIndex > 0) {
        browserHistoryIndex--;
        const url = browserHistory[browserHistoryIndex];
        navigateToUrl(url);
    }
}

function browserForward() {
    if (browserHistoryIndex < browserHistory.length - 1) {
        browserHistoryIndex++;
        const url = browserHistory[browserHistoryIndex];
        navigateToUrl(url);
    }
}

function browserReload() {
    const frame = document.getElementById('browser-preview-frame');
    if (frame && currentBrowserUrl) {
        frame.src = currentBrowserUrl;
    }
}

function navigateToUrl(url) {
    const previewUrl = document.getElementById('browser-preview-url');
    const urlInput = document.getElementById('browser-url-input');
    const frame = document.getElementById('browser-preview-frame');
    
    if (frame) {
        currentBrowserUrl = url;
        if (previewUrl) previewUrl.value = url;
        if (urlInput) urlInput.value = url;
        frame.src = url;
    }
}

function toggleBrowserFullscreen() {
    const previewPanel = document.getElementById('browser-preview-panel');
    if (previewPanel) {
        if (previewPanel.style.position === 'fixed') {
            previewPanel.style.position = 'absolute';
            previewPanel.style.top = '0';
            previewPanel.style.left = '0';
            previewPanel.style.right = '0';
            previewPanel.style.bottom = '0';
            previewPanel.style.zIndex = '1000';
        } else {
            previewPanel.style.position = 'fixed';
            previewPanel.style.top = '0';
            previewPanel.style.left = '0';
            previewPanel.style.right = '0';
            previewPanel.style.bottom = '0';
            previewPanel.style.zIndex = '10000';
        }
    }
}

function closeBrowserPreview() {
    hideBrowserPreview();
    // Switch back to explorer view
    switchView('explorer');
    document.querySelectorAll('.activity-icon').forEach(icon => {
        icon.classList.remove('active');
        if (icon.dataset.view === 'explorer') {
            icon.classList.add('active');
        }
    });
}

function refreshBrowser() {
    browserReload();
}

function handleBrowserUrlKeyPress(event) {
    if (event.key === 'Enter') {
        navigateBrowser();
    }
}

// API function for AI to control browser
async function aiNavigateBrowser(url) {
    try {
        const response = await fetch('/api/browser/navigate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });
        const data = await response.json();
        if (data.success) {
            navigateToUrl(url);
            return { success: true, message: `Navigated to ${url}` };
        }
        return { success: false, error: data.error };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function aiBrowserScreenshot() {
    try {
        const response = await fetch('/api/browser/screenshot');
        const data = await response.json();
        return data;
    } catch (error) {
        return { success: false, error: error.message };
    }
}

async function aiBrowserGetUrl() {
    const frame = document.getElementById('browser-preview-frame');
    if (frame) {
        try {
            // Try to get URL from iframe (may be blocked by CORS)
            return { success: true, url: currentBrowserUrl || frame.src };
        } catch (e) {
            return { success: true, url: currentBrowserUrl || 'Unknown (CORS blocked)' };
        }
    }
    return { success: false, error: 'Browser preview not active' };
}

// Toolkit Status Functions
async function refreshToolkitStatus() {
    try {
        const response = await fetch('/api/toolkit/status');
        const data = await response.json();
        
        const statusContent = document.getElementById('toolkit-status-content');
        if (!statusContent) return;
        
        let html = '<div class="toolkit-item">';
        
        // Security Toolkit Status
        if (data.security_toolkit) {
            const st = data.security_toolkit;
            html += '<div class="toolkit-section"><strong>🔒 Security Toolkit</strong></div>';
            
            if (st.git) {
                const gitStatus = st.git.available ? '✅ Available' : '❌ Not Available';
                html += `<div class="toolkit-item-detail">Git: ${gitStatus}</div>`;
            }
            
            if (st.nmap) {
                const nmapStatus = st.nmap.available ? '✅ Available' : '❌ Not Available';
                html += `<div class="toolkit-item-detail">Nmap: ${nmapStatus}</div>`;
            }
            
            if (st.burp_suite) {
                const burpStatus = st.burp_suite.installed ? '✅ Installed' : '❌ Not Installed';
                html += `<div class="toolkit-item-detail">Burp Suite: ${burpStatus}</div>`;
                if (st.burp_suite.path) {
                    html += `<div class="toolkit-item-detail-small">Path: ${st.burp_suite.path}</div>`;
                }
            }
        }
        
        // Dashboard Fix Agent Status
        if (data.dashboard_fix_agent) {
            html += '<div class="toolkit-section"><strong>🛠️ Dashboard Fix Agent</strong></div>';
            const agentStatus = data.dashboard_fix_agent.available ? '✅ Available' : '❌ Not Available';
            html += `<div class="toolkit-item-detail">Status: ${agentStatus}</div>`;
            if (data.dashboard_fix_agent.openai_available) {
                html += `<div class="toolkit-item-detail">OpenAI: ✅ Available</div>`;
            } else {
                html += `<div class="toolkit-item-detail">OpenAI: ⚠️ Not Configured (using fallback)</div>`;
            }
        }
        
        html += '</div>';
        statusContent.innerHTML = html;
    } catch (error) {
        console.error('Error loading toolkit status:', error);
        const statusContent = document.getElementById('toolkit-status-content');
        if (statusContent) {
            statusContent.innerHTML = '<div class="error">Error loading toolkit status</div>';
        }
    }
}

// Load toolkit status on AI view open
function switchView(view) {
    // Hide all views
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    
    // Show selected view
    const viewElement = document.getElementById(view + '-view');
    if (viewElement) {
        viewElement.classList.add('active');
    }
    
    // Handle browser view specially
    if (view === 'browser') {
        showBrowserPreview();
    } else {
        hideBrowserPreview();
    }
    
    // Load toolkit status when AI view is opened
    if (view === 'ai') {
        setTimeout(() => refreshToolkitStatus(), 100);
    }
}

// Initialization is handled in initOtherComponents()

