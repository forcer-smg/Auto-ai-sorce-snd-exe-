// Auto_Punch IDE - Main JavaScript

let editor = null;
let currentFiles = {};
let currentWorkspace = null;
let socket = null;
let currentSessionId = null;
let activeProgressUpdates = {}; // Track active progress updates
let fileExplorationCount = 0;

// AI Streaming state (global for persistence)
let currentStreamingMessage = '';
let streamingMessageId = null;

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing IDE...');
    
    // Initialize Socket.IO early (but wait for library to load)
    // Socket.IO script is loaded dynamically, check for it
    function initSocketWhenReady() {
        // Check multiple ways Socket.IO might be available
        let ioAvailable = false;
        let ioSource = '';
        
        if (typeof io !== 'undefined') {
            ioAvailable = true;
            ioSource = 'global io';
        } else if (typeof window.io !== 'undefined') {
            ioAvailable = true;
            ioSource = 'window.io';
        } else if (window.io && typeof window.io === 'function') {
            ioAvailable = true;
            ioSource = 'window.io function';
        }
        
        if (ioAvailable) {
            console.log('[INIT] ✅ Socket.IO library found, initializing...');
            console.log('[INIT] io source:', ioSource);
            initOtherComponents();
            return true;
        }
        return false;
    }
    
    // Try to load Socket.IO if it failed from CDN
    function loadSocketIOFallback() {
        console.log('[INIT] Attempting to load Socket.IO from alternative CDN...');
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.4/socket.io.min.js';
        script.onload = function() {
            console.log('[INIT] Socket.IO loaded from fallback CDN');
            // Wait a bit for io to be available
            setTimeout(() => {
                if (typeof io !== 'undefined' || typeof window.io !== 'undefined') {
                    initOtherComponents();
                } else {
                    console.error('[INIT] Socket.IO script loaded but io variable not available');
                }
            }, 100);
        };
        script.onerror = function() {
            console.error('[INIT] Failed to load Socket.IO from fallback CDN as well');
            console.error('[INIT] Socket.IO is required for real-time features');
            // Show user-friendly message
            const errorMsg = document.createElement('div');
            errorMsg.style.cssText = 'position: fixed; top: 10px; right: 10px; background: #f48771; color: white; padding: 15px; border-radius: 4px; z-index: 10000; max-width: 300px;';
            errorMsg.innerHTML = '<strong>⚠️ Connection Warning</strong><br>Socket.IO failed to load. Real-time features may not work. Please check your internet connection.';
            document.body.appendChild(errorMsg);
            setTimeout(() => errorMsg.remove(), 10000);
        };
        document.head.appendChild(script);
    }
    
    // Listen for socketio-loaded event
    window.addEventListener('socketio-loaded', function() {
        console.log('[INIT] Received socketio-loaded event');
        if (initSocketWhenReady()) {
            console.log('[INIT] Socket.IO initialized from event');
        }
    });
    
    // Wait for socketIOLoaded flag or check for io variable
    function waitForSocketIO() {
        // Try immediately
        if (initSocketWhenReady()) {
            return;
        }
        
        // Check if script reported it loaded
        if (window.socketIOLoaded) {
            // Give it a moment to set the io variable
            setTimeout(() => {
                if (initSocketWhenReady()) {
                    console.log('[INIT] Socket.IO initialized after socketIOLoaded flag');
                    return;
                }
            }, 200);
        }
        
        // Wait for Socket.IO to load (script loads asynchronously)
        let attempts = 0;
        const maxAttempts = 100; // 10 seconds (increased timeout)
        const checkSocketIO = setInterval(() => {
            attempts++;
            if (initSocketWhenReady()) {
                clearInterval(checkSocketIO);
                console.log('[INIT] Socket.IO library loaded after', attempts * 100, 'ms');
            } else if (attempts >= maxAttempts) {
                // 10 seconds timeout
                clearInterval(checkSocketIO);
                console.error('[INIT] Socket.IO library failed to load after 10 seconds');
                console.error('[INIT] Check if https://cdn.socket.io/4.5.4/socket.io.min.js is accessible');
                console.error('[INIT] Current io:', typeof io, 'window.io:', typeof window.io);
                console.error('[INIT] socketIOLoaded flag:', window.socketIOLoaded);
                console.error('[INIT] socketIOFailed flag:', window.socketIOFailed);
                
                // Check if script failed to load
                if (window.socketIOFailed) {
                    console.log('[INIT] Socket.IO CDN load failed, trying fallback...');
                    loadSocketIOFallback();
                } else if (window.socketIOLoaded) {
                    // Script loaded but io not available - might be a timing issue
                    console.log('[INIT] Script loaded but io not available, waiting a bit more...');
                    setTimeout(() => {
                        if (initSocketWhenReady()) {
                            console.log('[INIT] Socket.IO available after extended wait');
                        } else {
                            console.error('[INIT] Socket.IO still not available, trying fallback...');
                            loadSocketIOFallback();
                        }
                    }, 2000);
                } else {
                    // Try one more time on window load
                    window.addEventListener('load', () => {
                        if (initSocketWhenReady()) {
                            console.log('[INIT] Socket.IO loaded on window.load event');
                        } else {
                            console.log('[INIT] Socket.IO still not loaded, trying fallback...');
                            loadSocketIOFallback();
                        }
                    });
                }
            }
        }, 100);
    }
    
    // Start waiting for Socket.IO
    waitForSocketIO();
    
    // Initialize Monaco Editor with better error handling
    // Fix MIME type issue by disabling NLS (localization)
    if (typeof require !== 'undefined') {
        require.config({ 
            paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' },
            'vs/nls': { 
                availableLanguages: { '*': 'en' },
                // Disable NLS to avoid MIME type issues
                load: function(name, req, onload, config) {
                    onload({});
                }
            }
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
        require.config({ 
            paths: { vs: 'https://cdn.jsdelivr.net/npm/monaco-editor@0.45.0/min/vs' },
            'vs/nls': { 
                availableLanguages: { '*': 'en' },
                // Disable NLS to avoid MIME type issues
                load: function(name, req, onload, config) {
                    onload({});
                }
            }
        });
        require(['vs/editor/editor.main'], function() {
            console.log('Monaco Editor loaded via direct script');
            setTimeout(() => {
                initMonacoEditor();
            }, 100);
        }, function(err) {
            console.error('Monaco Editor require error:', err);
            loadMonacoEditorFallback();
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
//  🔥 HACK OR DIE 🔥
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
        
        // Initialize breakpoints after editor is created
        setTimeout(initBreakpoints, 500);

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
    // Wait for Socket.IO to be available
    if (typeof io === 'undefined') {
        console.warn('[SOCKET] Socket.IO library not loaded yet, waiting...');
        // Retry after a short delay
        setTimeout(() => {
            if (typeof io !== 'undefined' && !socket) {
                initOtherComponents();
            }
        }, 500);
        return;
    }
    
    // Initialize Socket.IO with connection options (only once)
    if (!socket) {
        console.log('[SOCKET] Initializing Socket.IO connection...');
        try {
            socket = io({
                transports: ['websocket', 'polling'],
                reconnection: true,
                reconnectionDelay: 1000,
                reconnectionAttempts: 5,
                timeout: 20000
            });
            
            socket.on('connect', (data) => {
                console.log('[SOCKET] ✅ Connected to server');
                console.log('[SOCKET] Socket ID:', socket.id);
                if (data && data.session_id) {
                    currentSessionId = data.session_id;
                }
            });
            
            socket.on('connect_error', (error) => {
                console.error('[SOCKET] ❌ Connection error:', error);
                console.error('[SOCKET] Error details:', error.message || error);
            });
            
            socket.on('disconnect', (reason) => {
                console.warn('[SOCKET] ⚠️ Disconnected:', reason);
            });
            
            socket.on('reconnect', (attemptNumber) => {
                console.log('[SOCKET] 🔄 Reconnected after', attemptNumber, 'attempts');
            });
            
            socket.on('reconnect_attempt', (attemptNumber) => {
                console.log('[SOCKET] 🔄 Reconnection attempt', attemptNumber);
            });
            
            socket.on('reconnect_failed', () => {
                console.error('[SOCKET] ❌ Reconnection failed');
            });
        
        // Set up all socket event listeners
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
            console.log('📂 Received open_file_in_editor event:', data);
            if (data && data.path && data.content !== undefined) {
                // Use relative path if provided, otherwise use full path
                const filePath = data.relative_path || data.path;
                console.log('📂 Opening file:', filePath);
                openFileInEditor(data.path, data.content, data.language);
                
                // Show notification
                const statusText = document.getElementById('terminal-status-text');
                if (statusText) {
                    const fileName = filePath.split(/[/\\]/).pop();
                    statusText.textContent = `✅ File opened: ${fileName}`;
                    statusText.style.color = '#4ec9b0';
                    setTimeout(() => {
                        statusText.textContent = '';
                    }, 3000);
                }
            } else {
                console.warn('⚠️ Invalid open_file_in_editor data:', data);
            }
        });

        // Show terminal panel when commands are executed
        socket.on('show_terminal', (data) => {
            console.log('[TERMINAL] show_terminal event received');
            showTerminalPanel();
        });
        
        // Force show terminal (for AI processing)
        socket.on('force_show_terminal', (data) => {
            console.log('[TERMINAL] force_show_terminal event received');
            const terminalPanel = document.getElementById('terminal-panel');
            if (terminalPanel) {
                terminalPanel.style.display = 'flex';
                terminalPanel.style.visibility = 'visible';
                terminalPanel.style.opacity = '1';
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

        // AI Streaming Events
        socket.on('ai_stream_start', (data) => {
            console.log('[STREAM] AI stream started', data);
            // Remove typing indicator
            const typingMessages = document.querySelectorAll('.chat-message.ai');
            typingMessages.forEach(msg => {
                if (msg.textContent.includes('🤖 Thinking...') || msg.textContent.includes('💭')) {
                    msg.remove();
                }
            });
            // Create new message for streaming
            streamingMessageId = 'stream-' + Date.now();
            currentStreamingMessage = '';
            const messagesContainer = document.getElementById('chat-messages');
            if (messagesContainer) {
                const messageDiv = document.createElement('div');
                messageDiv.id = streamingMessageId;
                messageDiv.className = 'chat-message ai streaming';
                messageDiv.innerHTML = '<span class="typing-indicator">💭</span><span class="stream-content"></span>';
                messagesContainer.appendChild(messageDiv);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
                console.log('[STREAM] Created streaming message container:', streamingMessageId);
            }
        });
        
        socket.on('ai_stream_chunk', (data) => {
            // Only log every 10th chunk to avoid console spam
            if (data.chunk_count % 10 === 0) {
                console.log('[STREAM] Received chunk:', data.chunk_count, 'chars:', data.chunk?.length);
            }
            
            if (streamingMessageId && data.chunk) {
                currentStreamingMessage += data.chunk;
                const messageDiv = document.getElementById(streamingMessageId);
                if (messageDiv) {
                    const contentSpan = messageDiv.querySelector('.stream-content');
                    if (contentSpan) {
                        // Update immediately (no delay for real-time feel)
                        contentSpan.textContent = currentStreamingMessage;
                        
                        // Auto-scroll to bottom
                        const messagesContainer = document.getElementById('chat-messages');
                        if (messagesContainer) {
                            messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        }
                    } else {
                        if (data.chunk_count === 1) {
                            console.warn('[STREAM] Content span not found in message div');
                        }
                    }
                } else {
                    if (data.chunk_count === 1) {
                        console.warn('[STREAM] Message div not found:', streamingMessageId);
                    }
                }
            } else {
                if (data.chunk_count === 1) {
                    console.warn('[STREAM] Missing streamingMessageId or chunk:', { 
                        streamingMessageId, 
                        hasChunk: !!data.chunk 
                    });
                }
            }
        });
        
        socket.on('ai_stream_end', (data) => {
            console.log('[STREAM] ✅ AI stream ended', data);
            if (streamingMessageId) {
                const messageDiv = document.getElementById(streamingMessageId);
                if (messageDiv) {
                    // Remove typing indicator
                    const typingIndicator = messageDiv.querySelector('.typing-indicator');
                    if (typingIndicator) {
                        typingIndicator.remove();
                    }
                    
                    // Format final message with code highlighting
                    const contentSpan = messageDiv.querySelector('.stream-content');
                    if (contentSpan && currentStreamingMessage) {
                        let formatted = currentStreamingMessage;
                        // Highlight code blocks
                        formatted = formatted.replace(
                            /```(\w+)?\n([\s\S]+?)```/g,
                            '<pre class="code-block"><code>$2</code></pre>'
                        );
                        // Highlight commands
                        formatted = formatted.replace(
                            /\[EXECUTE:\s*(.+?)\]/gi,
                            '<span class="command-marker">🔧 EXECUTING: $1</span>'
                        );
                        contentSpan.innerHTML = formatted;
                    }
                    
                    messageDiv.classList.remove('streaming');
                    console.log('[STREAM] ✅ Finalized streaming message:', {
                        chunks: data.total_chunks,
                        length: data.total_length,
                        messageLength: currentStreamingMessage.length
                    });
                    
                    // Final scroll
                    const messagesContainer = document.getElementById('chat-messages');
                    if (messagesContainer) {
                        messagesContainer.scrollTop = messagesContainer.scrollHeight;
                    }
                } else {
                    console.warn('[STREAM] Message div not found for finalization:', streamingMessageId);
                }
                streamingMessageId = null;
                currentStreamingMessage = '';
            } else {
                console.warn('[STREAM] No streaming message ID when stream ended');
            }
        });

        // Refresh file explorer when files are created
        socket.on('refresh_file_explorer', (data) => {
            console.log('🔄 Refreshing file explorer:', data);
            if (data && data.workspace) {
                // Reload file tree for the specific workspace
                setTimeout(() => {
                    console.log('🔄 Loading file tree for workspace:', data.workspace);
                    loadFileTree(data.workspace);
                }, 300); // Small delay to ensure file is written
            } else {
                // Fallback: refresh current workspace
                setTimeout(() => {
                    refreshExplorer();
                }, 300);
            }
        });

        } catch (error) {
            console.error('[SOCKET] ❌ Failed to initialize socket:', error);
            socket = null;
        }
    } else if (socket) {
        console.log('[SOCKET] Already initialized, socket ID:', socket.id, 'connected:', socket.connected);
    } else {
        console.warn('[SOCKET] Socket already exists but may not be connected');
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
        } else if (viewName === 'ssh') {
            loadSSHConnections();
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
    if (!treeElement) {
        console.error('[EXPLORER] File tree element not found');
        return;
    }
    
    console.log('[EXPLORER] 🔄 Loading file tree for:', path);
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
    // Get current workspace or use default
    if (currentWorkspace) {
        loadFileTree(currentWorkspace);
    } else {
        // Load workspace first, then refresh
        loadWorkspace().then(() => {
            if (currentWorkspace) {
                loadFileTree(currentWorkspace);
            } else {
                // Fallback: try to get workspace from API
                fetch('/api/workspace/get')
                    .then(res => res.json())
                    .then(data => {
                        if (data.success && data.path) {
                            currentWorkspace = data.path;
                            loadFileTree(currentWorkspace);
                        }
                    })
                    .catch(err => {
                        console.error('Failed to load workspace:', err);
                    });
            }
        });
    }
}

async function openWorkspaceFolder() {
    try {
        const response = await fetch('/api/workspace/open', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        
        const data = await response.json();
        if (data.success) {
            // Also show in terminal
            appendTerminalOutput(`\n📁 Opened folder: ${data.message || 'Workspace folder'}\n`);
        } else {
            alert('Error opening folder: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error opening folder:', error);
        alert('Error opening folder: ' + error.message);
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
            
            // Check if model already exists before creating
            const uri = monaco.Uri.file(filePath);
            let model = monaco.editor.getModel(uri);
            
            if (!model) {
                // Create new model only if it doesn't exist
                model = monaco.editor.createModel(data.content, language, uri);
            } else {
                // Update existing model
                model.setValue(data.content);
                monaco.editor.setModelLanguage(model, language);
            }
            
            editor.setModel(model);
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
// Open file in editor with content (for AI-generated files) - Cursor AI style
function openFileInEditor(filePath, content, language) {
    console.log('[EDITOR] 📂 Opening file in editor:', { filePath, language, contentLength: content?.length });
    
    if (!filePath || content === undefined) {
        console.error('[EDITOR] ❌ Invalid parameters:', { filePath, hasContent: content !== undefined });
        return;
    }
    
    // Store file content
    if (!currentFiles[filePath]) {
        currentFiles[filePath] = { 
            path: filePath,
            content: content, 
            modified: false,
            language: language || detectLanguage(filePath)
        };
        console.log('[EDITOR] ✅ File added to currentFiles:', filePath);
    } else {
        currentFiles[filePath].content = content;
        currentFiles[filePath].language = language || detectLanguage(filePath);
        console.log('[EDITOR] ✅ File content updated:', filePath);
    }
    
    // Add tab if not exists (Cursor AI style - auto-open in editor)
    const escapedPath = filePath.replace(/\\/g, '\\\\').replace(/'/g, "\\'");
    let tabExists = document.querySelector(`.tab[data-path="${escapedPath}"]`);
    
    if (!tabExists) {
        console.log('[EDITOR] Creating new tab for:', filePath);
        addTab(filePath, content);
    } else {
        console.log('[EDITOR] Tab exists, switching to it:', filePath);
        switchToTab(filePath);
    }
    
    // Set editor content and language (like Cursor AI)
    if (editor) {
        const finalLanguage = language || detectLanguage(filePath);
        console.log('[EDITOR] Setting editor content, language:', finalLanguage);
        
        try {
            const uri = monaco.Uri.file(filePath);
            let model = monaco.editor.getModel(uri);
            
            if (!model) {
                // Create new model
                model = monaco.editor.createModel(content, finalLanguage, uri);
                console.log('[EDITOR] ✅ Created new Monaco model');
            } else {
                // Update existing model
                model.setValue(content);
                monaco.editor.setModelLanguage(model, finalLanguage);
                console.log('[EDITOR] ✅ Updated existing Monaco model');
            }
            
            // Set model in editor
            editor.setModel(model);
            
            // Update language indicator
            const langEl = document.querySelector('.editor-language');
            if (langEl) {
                langEl.textContent = finalLanguage || 'Plain Text';
            }
        } catch (error) {
            console.error('[EDITOR] ❌ Error setting editor model:', error);
            // Fallback: just set value
            if (editor) {
                editor.setValue(content);
            }
        }
    } else {
        console.warn('[EDITOR] ⚠️ Editor not initialized yet, retrying...');
        setTimeout(() => {
            if (editor) {
                openFileInEditor(filePath, content, language);
            }
        }, 500);
    }
    
    // Switch to editor view (like Cursor AI) - ensure file is visible
    setTimeout(() => {
        // Make sure explorer view is active
        switchView('explorer');
        
        // Scroll file into view in file tree if possible
        const fileName = filePath.split(/[/\\]/).pop();
        const fileTreeItems = document.querySelectorAll('.file-tree-item');
        for (const item of fileTreeItems) {
            if (item.textContent.includes(fileName)) {
                item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                // Highlight briefly (like Cursor AI)
                item.style.backgroundColor = 'rgba(78, 201, 176, 0.2)';
                setTimeout(() => {
                    item.style.backgroundColor = '';
                }, 2000);
                break;
            }
        }
    }, 200);
    
    console.log('[EDITOR] ✅ File opened successfully:', filePath);
    
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

function createNewTab() {
    let counter = 1;
    let filePath = 'Untitled-' + counter;
    while (currentFiles[filePath]) {
        counter++;
        filePath = 'Untitled-' + counter;
    }
    addTab(filePath, '');
    currentFiles[filePath] = { content: '', modified: false };
    openFileInEditor(filePath, '', 'plaintext');
    return document.querySelector(`.tab[data-path="${filePath}"]`);
}

function openFileContent(fileName, content) {
    const filePath = fileName;
    addTab(filePath, content);
    currentFiles[filePath] = { content: content, modified: false };
    openFileInEditor(filePath, content);
}

function switchToTab(filePath) {
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
        if (tab.dataset.path === filePath) {
            tab.classList.add('active');
        }
    });
    
    if (currentFiles[filePath]) {
        const uri = monaco.Uri.file(filePath);
        let model = monaco.editor.getModel(uri);
        
        if (!model) {
            // Create new model only if it doesn't exist
            model = monaco.editor.createModel(
                currentFiles[filePath].content,
                detectLanguage(filePath),
                uri
            );
        } else {
            // Update existing model with current content
            model.setValue(currentFiles[filePath].content);
            monaco.editor.setModelLanguage(model, detectLanguage(filePath));
        }
        
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
    // Dispose of Monaco model when closing tab
    try {
        const uri = monaco.Uri.file(filePath);
        const model = monaco.editor.getModel(uri);
        if (model) {
            model.dispose();
            console.log('[EDITOR] Disposed model for:', filePath);
        }
    } catch (error) {
        console.warn('[EDITOR] Error disposing model:', error);
    }
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
// Function to show terminal panel and scroll to bottom
function showTerminalPanel() {
    console.log('[TERMINAL] showTerminalPanel called');
    const terminalPanel = document.getElementById('terminal-panel');
    if (terminalPanel) {
        console.log('[TERMINAL] Terminal panel found, showing...');
        terminalPanel.style.display = 'flex';
        terminalPanel.style.visibility = 'visible';
        terminalPanel.style.opacity = '1';
        terminalPanel.style.zIndex = '1000';  // Ensure it's on top
        // Scroll terminal to bottom
        setTimeout(() => {
            const terminalOutput = document.getElementById('terminal-output');
            if (terminalOutput) {
                terminalOutput.scrollTop = terminalOutput.scrollHeight;
                console.log('[TERMINAL] Scrolled to bottom');
            }
        }, 100);
        return true;
    }
    console.error('[TERMINAL] Terminal panel not found!');
    return false;
}

// Click handler function for terminal status
function showTerminalOnClick(event) {
    event.preventDefault();
    event.stopPropagation();
    console.log('[TERMINAL] Clicked on AI status - showing terminal');
    if (showTerminalPanel()) {
        console.log('[TERMINAL] Terminal panel shown successfully');
    } else {
        console.error('[TERMINAL] Failed to show terminal panel');
    }
}

function handleAIProgress(message, data) {
    // Update progress in chat or status bar
    const progressId = 'progress-' + Date.now();
    const progressEl = addProgressMessage(message, progressId);
    
    // Update status bar if available
    const statusText = document.getElementById('terminal-status-text');
    if (statusText) {
        statusText.textContent = message;
        statusText.style.color = '#4ec9b0';
        statusText.style.cursor = 'pointer';
        statusText.title = 'Click to view AI processing in terminal';
        
        // Make clickable to show terminal - use both onclick and event listener
        statusText.onclick = showTerminalOnClick;
        try {
            statusText.removeEventListener('click', showTerminalOnClick);
        } catch (e) {
            // Ignore if listener doesn't exist
        }
        statusText.addEventListener('click', showTerminalOnClick);
        
        const statusEl = document.getElementById('terminal-status');
        if (statusEl) {
            statusEl.style.display = 'block';
            statusEl.style.cursor = 'pointer';
            statusEl.title = 'Click to view AI processing in terminal';
            statusEl.onclick = showTerminalOnClick;
            try {
                statusEl.removeEventListener('click', showTerminalOnClick);
            } catch (e) {
                // Ignore if listener doesn't exist
            }
            statusEl.addEventListener('click', showTerminalOnClick);
        }
    }
    
    // Also show in terminal if terminal is visible
    const terminalOutput = document.getElementById('terminal-output');
    if (terminalOutput && terminalOutput.offsetParent !== null) {
        // Terminal is visible, add progress message
        const progressLine = document.createElement('div');
        progressLine.className = 'terminal-line';
        progressLine.textContent = `[AI] ${message}`;
        progressLine.style.color = '#4ec9b0';
        terminalOutput.appendChild(progressLine);
        terminalOutput.scrollTop = terminalOutput.scrollHeight;
    }
}

// Click handler function for terminal status
function showTerminalOnClick(event) {
    event.preventDefault();
    event.stopPropagation();
    console.log('[TERMINAL] Clicked on AI status - showing terminal');
    if (showTerminalPanel()) {
        console.log('[TERMINAL] Terminal panel shown');
    } else {
        console.error('[TERMINAL] Failed to show terminal panel');
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
    
    // Ensure socket is initialized and connected
    if (typeof io === 'undefined') {
        console.error('[CHAT] ❌ Socket.IO library not loaded');
        removeChatMessage(typingId);
        addChatMessage('ai', 'Error: Socket.IO library not loaded. Please refresh the page.');
        return;
    }
    
    if (!socket) {
        console.warn('[CHAT] Socket not initialized, initializing...');
        initOtherComponents();
        // Wait for socket to be created
        let attempts = 0;
        while (!socket && attempts < 20) {
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
    }
    
    if (!socket) {
        console.error('[CHAT] ❌ Socket failed to initialize after waiting');
        removeChatMessage(typingId);
        addChatMessage('ai', 'Error: WebSocket connection failed. Please refresh the page.');
        return;
    }
    
    // Check connection status
    if (!socket.connected) {
        console.warn('[CHAT] ⚠️ Socket not connected, attempting to connect...');
        if (socket.disconnected) {
            socket.connect();
        }
        // Wait for connection
        let attempts = 0;
        while (!socket.connected && attempts < 10) {
            await new Promise(resolve => setTimeout(resolve, 200));
            attempts++;
        }
    }
    
    if (socket.connected) {
        console.log('[CHAT] ✅ Socket connected, ID:', socket.id);
    } else {
        console.warn('[CHAT] ⚠️ Socket not connected, but proceeding with request...');
        console.warn('[CHAT] Socket state:', { 
            connected: socket.connected, 
            disconnected: socket.disconnected,
            id: socket.id 
        });
    }
    
    // Reset streaming state
    streamingMessageId = null;
    currentStreamingMessage = '';
    
    // Choose streaming method: SSE (Cursor-style) or WebSocket
    const useSSE = true; // Use Server-Sent Events like Cursor AI
    
    if (useSSE) {
        // Cursor-style streaming with Server-Sent Events
        streamWithSSE(message, typingId);
    } else {
        // WebSocket streaming (existing method)
        streamWithWebSocket(message, typingId);
    }
}

// Cursor-style streaming with Server-Sent Events
async function streamWithSSE(message, typingId) {
    try {
        const response = await fetch('/api/ai/chat?format=sse', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Accept': 'text/event-stream',
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
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Remove typing indicator
        removeChatMessage(typingId);
        
        // Create streaming message container
        streamingMessageId = 'stream-' + Date.now();
        currentStreamingMessage = '';
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            const messageDiv = document.createElement('div');
            messageDiv.id = streamingMessageId;
            messageDiv.className = 'chat-message ai streaming';
            messageDiv.innerHTML = '<span class="typing-indicator">💭</span><span class="stream-content"></span>';
            messagesContainer.appendChild(messageDiv);
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
        
        // Read SSE stream
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';
        
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            buffer += decoder.decode(value, { stream: true });
            const lines = buffer.split('\n');
            buffer = lines.pop() || ''; // Keep incomplete line in buffer
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        
                        if (data.type === 'start') {
                            console.log('[SSE] Stream started');
                        } else if (data.type === 'token') {
                            // Append token immediately (Cursor-style)
                            if (data.content) {
                                currentStreamingMessage += data.content;
                                const messageDiv = document.getElementById(streamingMessageId);
                                if (messageDiv) {
                                    const contentSpan = messageDiv.querySelector('.stream-content');
                                    if (contentSpan) {
                                        contentSpan.textContent = currentStreamingMessage;
                                        // Auto-scroll
                                        const messagesContainer = document.getElementById('chat-messages');
                                        if (messagesContainer) {
                                            messagesContainer.scrollTop = messagesContainer.scrollHeight;
                                        }
                                    }
                                }
                            }
                        } else if (data.type === 'end') {
                            console.log('[SSE] Stream ended', data);
                            // Finalize message
                            const messageDiv = document.getElementById(streamingMessageId);
                            if (messageDiv) {
                                const typingIndicator = messageDiv.querySelector('.typing-indicator');
                                if (typingIndicator) typingIndicator.remove();
                                
                                const contentSpan = messageDiv.querySelector('.stream-content');
                                if (contentSpan && currentStreamingMessage) {
                                    let formatted = currentStreamingMessage;
                                    // Highlight code blocks
                                    formatted = formatted.replace(
                                        /```(\w+)?\n([\s\S]+?)```/g,
                                        '<pre class="code-block"><code>$2</code></pre>'
                                    );
                                    // Highlight commands
                                    formatted = formatted.replace(
                                        /\[EXECUTE:\s*(.+?)\]/gi,
                                        '<span class="command-marker">🔧 EXECUTING: $1</span>'
                                    );
                                    contentSpan.innerHTML = formatted;
                                }
                                messageDiv.classList.remove('streaming');
                            }
                            streamingMessageId = null;
                            currentStreamingMessage = '';
                        } else if (data.type === 'error') {
                            console.error('[SSE] Stream error:', data.content);
                            removeChatMessage(typingId);
                            addChatMessage('ai', 'Error: ' + data.content);
                        }
                    } catch (e) {
                        console.error('[SSE] Parse error:', e, line);
                    }
                }
            }
        }
    } catch (error) {
        console.error('SSE streaming error:', error);
        removeChatMessage(typingId);
        addChatMessage('ai', 'Error: ' + error.message);
    }
}

// WebSocket streaming (existing method)
async function streamWithWebSocket(message, typingId) {
    try {
        // Send request - response will be streamed via WebSocket
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
        
        // Remove typing indicator (streaming will handle it)
        removeChatMessage(typingId);
        
        if (data.success) {
            // Check if commands were executed
            if (data.executed_commands && data.executed_commands > 0) {
                if (statusText) {
                    statusText.textContent = `✅ Executed ${data.executed_commands} command(s)`;
                    statusText.style.color = '#4ec9b0';
                    setTimeout(() => {
                        if (statusEl) statusEl.style.display = 'none';
                    }, 5000);
                }
            } else {
                if (statusEl) statusEl.style.display = 'none';
            }
            
            // If streaming was used, the message is already displayed
            // Otherwise, fallback to non-streaming display
            if (!data.streamed && data.response) {
                let formattedResponse = data.response || '';
                
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
            }
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

// Menu handlers - make globally accessible
window.showMenu = function(menuName) {
    if (menuName === 'terminal') {
        toggleTerminal();
    } else if (menuName === 'toolkit') {
        // Show toolkit view
        switchView('toolkit');
        loadToolkit();
    }
};

// Dropdown menu functions
let currentOpenMenu = null;

function toggleMenuDropdown(menuName, event) {
    event.stopPropagation();
    const menu = document.getElementById(menuName + '-menu');
    
    // Close all other menus
    closeMenuDropdowns();
    
    // Toggle current menu
    if (menu) {
        if (currentOpenMenu === menuName) {
            menu.classList.remove('show');
            currentOpenMenu = null;
        } else {
            menu.classList.add('show');
            currentOpenMenu = menuName;
        }
    }
}

function closeMenuDropdowns() {
    document.querySelectorAll('.menu-dropdown').forEach(menu => {
        menu.classList.remove('show');
    });
    currentOpenMenu = null;
}

// Close dropdowns when clicking outside
document.addEventListener('click', function(event) {
    if (!event.target.closest('.menu-item-container') && !event.target.closest('.menu-dropdown')) {
        closeMenuDropdowns();
    }
});

// File menu actions
function openFileDialog() {
    const input = document.createElement('input');
    input.type = 'file';
    input.onchange = (e) => {
        if (e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                openFileContent(e.target.files[0].name, ev.target.result);
            };
            reader.readAsText(e.target.files[0]);
        }
    };
    input.click();
}

function saveCurrentFile() {
    const activeTab = document.querySelector('.tab.active');
    if (activeTab) {
        saveFile(activeTab.dataset.path);
    } else {
        alert('No file is currently open');
    }
}

function saveAllFiles() {
    document.querySelectorAll('.tab').forEach(tab => {
        if (tab.dataset.path) {
            saveFile(tab.dataset.path);
        }
    });
}

function closeCurrentTab() {
    const activeTab = document.querySelector('.tab.active');
    if (activeTab) {
        closeTab(activeTab);
    }
}

function closeAllTabs() {
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => closeTab(tab));
}

// Edit menu actions
function undoAction() {
    if (editor) {
        editor.trigger('keyboard', 'undo', null);
    }
}

function redoAction() {
    if (editor) {
        editor.trigger('keyboard', 'redo', null);
    }
}

function cutAction() {
    if (editor) {
        editor.trigger('keyboard', 'editor.action.clipboardCutAction', null);
    }
}

function copyAction() {
    if (editor) {
        editor.trigger('keyboard', 'editor.action.clipboardCopyAction', null);
    }
}

function pasteAction() {
    if (editor) {
        editor.trigger('keyboard', 'editor.action.clipboardPasteAction', null);
    }
}

function findInFile() {
    if (editor) {
        editor.getAction('actions.find').run();
    }
}

function replaceInFile() {
    if (editor) {
        editor.getAction('actions.find').run();
        setTimeout(() => {
            const replaceBtn = document.querySelector('.find-widget .replace-input');
            if (replaceBtn) replaceBtn.focus();
        }, 100);
    }
}

function formatDocument() {
    if (editor) {
        editor.getAction('editor.action.formatDocument').run();
    }
}

function toggleComment() {
    if (editor) {
        editor.getAction('editor.action.commentLine').run();
    }
}

// View menu actions
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.style.display = sidebar.style.display === 'none' ? 'flex' : 'none';
    }
}

function togglePanel() {
    toggleTerminal();
}

// Run menu actions
function runCurrentFile() {
    const activeTab = document.querySelector('.tab.active');
    if (activeTab && activeTab.dataset.path) {
        const filePath = activeTab.dataset.path;
        const language = detectLanguage(filePath);
        
        if (language === 'python') {
            executeInTerminal(`python "${filePath}"`);
        } else if (language === 'javascript') {
            executeInTerminal(`node "${filePath}"`);
        } else if (language === 'powershell') {
            executeInTerminal(`powershell -File "${filePath}"`);
        } else {
            alert('Cannot run this file type. Please use the terminal to run it manually.');
        }
    } else {
        alert('No file is currently open');
    }
}

function runWithoutDebugging() {
    runCurrentFile();
}

// Debugging System
let debugSession = null;
let isDebugging = false;
let breakpoints = [];
let debugVariables = {};
let debugCallStack = [];

function startDebugging() {
    const activeTab = document.querySelector('.tab.active');
    if (!activeTab || !activeTab.dataset.path) {
        alert('Please open a file to debug');
        return;
    }
    
    const filePath = activeTab.dataset.path;
    const language = detectLanguage(filePath);
    
    if (!editor) {
        alert('Editor not initialized');
        return;
    }
    
    // Check if file has breakpoints
    const model = editor.getModel();
    if (!model) {
        alert('No file content to debug');
        return;
    }
    
    // Get breakpoints
    if (breakpointDecorations.length === 0) {
        const confirmDebug = confirm('No breakpoints set. Start debugging anyway?');
        if (!confirmDebug) return;
    }
    
    // Start debug session
    isDebugging = true;
    debugSession = {
        filePath: filePath,
        language: language,
        startTime: Date.now(),
        breakpoints: breakpointDecorations.map(bp => ({
            line: bp.line,
            column: 1
        }))
    };
    
    // Update UI
    updateDebugUI();
    updateDebugStatus('Debugging started - Running...');
    
    // Switch to debug view
    switchView('debug');
    
    // Run the file with debugging
    runFileWithDebugger(filePath, language);
}

function stopDebugging() {
    if (!isDebugging) return;
    
    isDebugging = false;
    debugSession = null;
    debugVariables = {};
    debugCallStack = [];
    
    // Clear debug decorations
    if (editor) {
        const model = editor.getModel();
        if (model) {
            editor.deltaDecorations([], []);
        }
    }
    
    updateDebugUI();
    updateDebugStatus('Debugging stopped');
    
    // Clear variables and call stack
    document.getElementById('debug-variables').innerHTML = 
        '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">Variables will appear here when debugging</div>';
    document.getElementById('debug-callstack').innerHTML = 
        '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">Call stack will appear here when debugging</div>';
}

function debugContinue() {
    if (!isDebugging) return;
    updateDebugStatus('Continuing execution...');
    // In a real implementation, this would resume execution
    setTimeout(() => {
        updateDebugStatus('Running...');
    }, 500);
}

function debugStepOver() {
    if (!isDebugging) return;
    updateDebugStatus('Stepping over...');
    // Simulate stepping over
    setTimeout(() => {
        updateDebugStatus('Paused on line ' + (debugSession?.currentLine || '?'));
        updateDebugVariables();
    }, 300);
}

function debugStepInto() {
    if (!isDebugging) return;
    updateDebugStatus('Stepping into...');
    // Simulate stepping into
    setTimeout(() => {
        updateDebugStatus('Paused on line ' + (debugSession?.currentLine || '?'));
        updateDebugVariables();
        updateDebugCallStack();
    }, 300);
}

function debugStepOut() {
    if (!isDebugging) return;
    updateDebugStatus('Stepping out...');
    // Simulate stepping out
    setTimeout(() => {
        updateDebugStatus('Paused on line ' + (debugSession?.currentLine || '?'));
        updateDebugVariables();
        updateDebugCallStack();
    }, 300);
}

function updateDebugUI() {
    const startBtn = document.getElementById('debug-start-btn');
    const stopBtn = document.getElementById('debug-stop-btn');
    const continueBtn = document.getElementById('debug-continue-btn');
    const stepOverBtn = document.getElementById('debug-step-over-btn');
    const stepIntoBtn = document.getElementById('debug-step-into-btn');
    const stepOutBtn = document.getElementById('debug-step-out-btn');
    
    if (isDebugging) {
        if (startBtn) startBtn.style.display = 'none';
        if (stopBtn) stopBtn.style.display = 'inline-block';
        if (continueBtn) continueBtn.style.display = 'inline-block';
        if (stepOverBtn) stepOverBtn.style.display = 'inline-block';
        if (stepIntoBtn) stepIntoBtn.style.display = 'inline-block';
        if (stepOutBtn) stepOutBtn.style.display = 'inline-block';
    } else {
        if (startBtn) startBtn.style.display = 'inline-block';
        if (stopBtn) stopBtn.style.display = 'none';
        if (continueBtn) continueBtn.style.display = 'none';
        if (stepOverBtn) stepOverBtn.style.display = 'none';
        if (stepIntoBtn) stepIntoBtn.style.display = 'none';
        if (stepOutBtn) stepOutBtn.style.display = 'none';
    }
}

function updateDebugStatus(message) {
    const statusEl = document.getElementById('debug-status');
    if (statusEl) {
        statusEl.textContent = 'Status: ' + message;
        statusEl.style.color = isDebugging ? '#4ec9b0' : '#858585';
    }
}

function updateDebugVariables() {
    const varsEl = document.getElementById('debug-variables');
    if (!varsEl) return;
    
    // Simulate variables (in real implementation, get from debugger)
    debugVariables = {
        'local': {
            'i': { value: '5', type: 'number' },
            'result': { value: '25', type: 'number' },
            'name': { value: '"test"', type: 'string' }
        },
        'global': {
            'window': { value: '[object Window]', type: 'object' }
        }
    };
    
    let html = '';
    for (const [scope, vars] of Object.entries(debugVariables)) {
        html += `<div style="margin-bottom: 10px;"><strong style="color: #4ec9b0;">${scope}</strong></div>`;
        for (const [name, info] of Object.entries(vars)) {
            html += `<div style="padding: 5px 10px; margin-left: 10px; background: rgba(0,0,0,0.2); border-radius: 3px; margin-bottom: 5px;">
                <span style="color: #4ec9b0;">${name}</span>
                <span style="color: #858585; margin-left: 10px;">${info.type}</span>
                <span style="color: #cccccc; margin-left: 10px;">= ${info.value}</span>
            </div>`;
        }
    }
    
    varsEl.innerHTML = html || '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">No variables available</div>';
}

function updateDebugCallStack() {
    const callstackEl = document.getElementById('debug-callstack');
    if (!callstackEl) return;
    
    // Simulate call stack
    debugCallStack = [
        { name: 'main()', file: 'app.py', line: 10 },
        { name: 'processData()', file: 'utils.py', line: 25 },
        { name: 'calculate()', file: 'utils.py', line: 42 }
    ];
    
    let html = '';
    debugCallStack.forEach((frame, index) => {
        html += `<div style="padding: 8px; margin-bottom: 5px; background: ${index === 0 ? 'rgba(78, 201, 176, 0.1)' : 'rgba(0,0,0,0.2)'}; border-radius: 3px; cursor: pointer;" onclick="jumpToFrame('${frame.file}', ${frame.line})">
            <div style="color: #4ec9b0; font-weight: bold;">${frame.name}</div>
            <div style="color: #858585; font-size: 11px; margin-top: 3px;">${frame.file}:${frame.line}</div>
        </div>`;
    });
    
    callstackEl.innerHTML = html || '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">No call stack available</div>';
}

function jumpToFrame(file, line) {
    // Open file and jump to line
    openFile(file);
    setTimeout(() => {
        if (editor) {
            editor.revealLineInCenter(line);
            editor.setPosition({ lineNumber: line, column: 1 });
        }
    }, 500);
}

function runFileWithDebugger(filePath, language) {
    // Execute file with debugger attached
    let command = '';
    
    if (language === 'python') {
        command = `python -m pdb "${filePath}"`;
    } else if (language === 'javascript') {
        command = `node --inspect "${filePath}"`;
    } else if (language === 'typescript') {
        command = `ts-node --inspect "${filePath}"`;
    } else {
        // For other languages, just run normally
        command = `"${filePath}"`;
    }
    
    executeInTerminal(command);
    
    // Update breakpoints list
    updateBreakpointsList();
}

function updateBreakpointsList() {
    const breakpointsEl = document.getElementById('breakpoints-list');
    if (!breakpointsEl) return;
    
    if (!editor) {
        breakpointsEl.innerHTML = '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">No file open</div>';
        return;
    }
    
    const model = editor.getModel();
    if (!model) {
        breakpointsEl.innerHTML = '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">No file content</div>';
        return;
    }
    
    if (breakpointDecorations.length === 0) {
        breakpointsEl.innerHTML = '<div style="color: #858585; text-align: center; padding: 20px; font-size: 12px;">No breakpoints set. Click in the gutter to add breakpoints.</div>';
        return;
    }
    
    let html = '';
    breakpointDecorations.forEach(bp => {
        const line = bp.line;
        const lineText = model.getLineContent(line).trim().substring(0, 50);
        html += `<div style="padding: 8px; margin-bottom: 5px; background: rgba(0,0,0,0.2); border-radius: 3px; display: flex; justify-content: space-between; align-items: center; cursor: pointer;" onclick="jumpToLine(${line})">
            <div>
                <span style="color: #4ec9b0;">Line ${line}</span>
                <span style="color: #858585; margin-left: 10px; font-size: 11px;">${lineText || '(empty line)'}</span>
            </div>
            <button onclick="removeBreakpoint(${line}); event.stopPropagation();" style="background: rgba(248, 119, 113, 0.2); border: 1px solid #f48771; color: #f48771; padding: 2px 8px; border-radius: 3px; cursor: pointer; font-size: 11px;">Remove</button>
        </div>`;
    });
    
    breakpointsEl.innerHTML = html;
}

function jumpToLine(line) {
    if (editor) {
        editor.revealLineInCenter(line);
        editor.setPosition({ lineNumber: line, column: 1 });
    }
}

function removeBreakpoint(line) {
    if (!editor) return;
    
    const index = breakpointDecorations.findIndex(d => d.line === line);
    if (index !== -1) {
        const decoration = breakpointDecorations[index];
        editor.deltaDecorations([decoration.id], []);
        breakpointDecorations.splice(index, 1);
    }
    
    updateBreakpointsList();
}

function refreshDebugView() {
    updateBreakpointsList();
    if (isDebugging) {
        updateDebugVariables();
        updateDebugCallStack();
    }
}

// Breakpoint management
let breakpointDecorations = [];

// Enable breakpoints in Monaco Editor
function initBreakpoints() {
    if (!editor) return;
    
    // Enable breakpoint clicking in gutter
    editor.onMouseDown((e) => {
        if (e.target && e.target.type === monaco.editor.MouseTargetType.GUTTER_LINE_NUMBERS) {
            const line = e.target.position.lineNumber;
            toggleBreakpoint(line);
        }
    });
}

function toggleBreakpoint(line) {
    if (!editor) return;
    
    const model = editor.getModel();
    if (!model) return;
    
    // Check if breakpoint already exists
    const existingIndex = breakpointDecorations.findIndex(d => d.line === line);
    
    if (existingIndex !== -1) {
        // Remove breakpoint
        const decoration = breakpointDecorations[existingIndex];
        editor.deltaDecorations([decoration.id], []);
        breakpointDecorations.splice(existingIndex, 1);
    } else {
        // Add breakpoint
        const decoration = {
            range: new monaco.Range(line, 1, line, 1),
            options: {
                glyphMarginClassName: 'breakpoint',
                glyphMarginHoverMessage: { value: 'Breakpoint' },
                isWholeLine: true
            }
        };
        const ids = editor.deltaDecorations([], [decoration]);
        breakpointDecorations.push({ id: ids[0], line: line });
    }
    
    updateBreakpointsList();
}

// Initialize breakpoints after Monaco is ready
if (typeof monaco !== 'undefined') {
    setTimeout(initBreakpoints, 2000);
} else {
    window.addEventListener('monaco-ready', initBreakpoints);
}

async function executeInTerminal(command) {
    toggleTerminal();
    if (command) {
        // Execute command directly
        setTimeout(async () => {
            appendTerminalOutput('$ ' + command);
            
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
                    body: JSON.stringify({ command: command })
                });
                
                const data = await response.json();
                if (data.success) {
                    appendTerminalOutput(data.output || '');
                } else {
                    appendTerminalOutput('Error: ' + (data.error || 'Command failed'));
                }
            } catch (error) {
                appendTerminalOutput('Error: ' + error.message);
            }
        }, 100);
    } else {
        // Just focus terminal input
        setTimeout(() => {
            const terminalInput = document.getElementById('terminal-input');
            if (terminalInput) terminalInput.focus();
        }, 100);
    }
}

// Command Palette
const commandPaletteCommands = [
    { id: 'file.new', label: 'New File', icon: '📄', action: () => { createNewTab(); } },
    { id: 'file.open', label: 'Open File...', icon: '📂', action: () => { const input = document.createElement('input'); input.type = 'file'; input.onchange = (e) => { if (e.target.files[0]) { const reader = new FileReader(); reader.onload = (ev) => { openFileContent(e.target.files[0].name, ev.target.result); }; reader.readAsText(e.target.files[0]); } }; input.click(); } },
    { id: 'file.save', label: 'Save', icon: '💾', shortcut: 'Ctrl+S', action: () => { const activeTab = document.querySelector('.tab.active'); if (activeTab) saveFile(activeTab.dataset.path); } },
    { id: 'file.saveAll', label: 'Save All', icon: '💾', action: () => { document.querySelectorAll('.tab').forEach(tab => saveFile(tab.dataset.path)); } },
    { id: 'file.close', label: 'Close Editor', icon: '✕', shortcut: 'Ctrl+W', action: () => { const activeTab = document.querySelector('.tab.active'); if (activeTab) closeTab(activeTab); } },
    { id: 'view.commandPalette', label: 'Show Command Palette', icon: '🔍', shortcut: 'Ctrl+Shift+P', action: () => showCommandPalette() },
    { id: 'view.terminal', label: 'Toggle Terminal', icon: '💻', shortcut: 'Ctrl+`', action: () => toggleTerminal() },
    { id: 'view.sidebar', label: 'Toggle Sidebar', icon: '📁', shortcut: 'Ctrl+B', action: () => { const sidebar = document.querySelector('.sidebar'); if (sidebar) sidebar.style.display = sidebar.style.display === 'none' ? 'flex' : 'none'; } },
    { id: 'view.settings', label: 'Open Settings', icon: '⚙️', shortcut: 'Ctrl+,', action: () => { switchView('settings'); } },
    { id: 'view.shortcuts', label: 'Keyboard Shortcuts', icon: '⌨️', shortcut: 'Ctrl+K Ctrl+S', action: () => { showHelpMenu(); setTimeout(() => switchHelpTab('shortcuts'), 100); } },
    { id: 'view.help', label: 'Show Help', icon: '❓', action: () => showHelpMenu() },
    { id: 'ai.assistant', label: 'Open AI Assistant', icon: '🤖', shortcut: 'Ctrl+Shift+A', action: () => switchView('ai') },
    { id: 'toolkit.open', label: 'Open RedTeam Toolkit', icon: '🔧', shortcut: 'Ctrl+Shift+T', action: () => { switchView('toolkit'); loadToolkit(); } },
    { id: 'browser.preview', label: 'Open Browser Preview', icon: '🌐', shortcut: 'Ctrl+Shift+B', action: () => switchView('browser') },
    { id: 'git.status', label: 'Git: Show Status', icon: '🔀', action: () => { switchView('git'); refreshGitStatus(); } },
    { id: 'search.find', label: 'Find in File', icon: '🔍', shortcut: 'Ctrl+F', action: () => { if (editor) editor.getAction('actions.find').run(); } },
    { id: 'search.replace', label: 'Replace in File', icon: '🔄', shortcut: 'Ctrl+H', action: () => { if (editor) editor.getAction('actions.find').run(); setTimeout(() => { const replaceBtn = document.querySelector('.find-widget .replace-input'); if (replaceBtn) replaceBtn.focus(); }, 100); } },
    { id: 'editor.format', label: 'Format Document', icon: '✨', shortcut: 'Shift+Alt+F', action: () => { if (editor) editor.getAction('editor.action.formatDocument').run(); } },
    { id: 'editor.comment', label: 'Toggle Line Comment', icon: '💬', shortcut: 'Ctrl+/', action: () => { if (editor) editor.getAction('editor.action.commentLine').run(); } },
];

let commandPaletteSelectedIndex = 0;
let filteredCommands = [...commandPaletteCommands];

function showCommandPalette() {
    const palette = document.getElementById('command-palette');
    const input = document.getElementById('command-palette-input');
    const results = document.getElementById('command-palette-results');
    
    if (!palette || !input || !results) return;
    
    palette.style.display = 'flex';
    filteredCommands = [...commandPaletteCommands];
    commandPaletteSelectedIndex = 0;
    input.value = '';
    input.focus();
    renderCommandPalette();
}

function closeCommandPalette() {
    const palette = document.getElementById('command-palette');
    if (palette) palette.style.display = 'none';
    commandPaletteSelectedIndex = 0;
}

function renderCommandPalette() {
    const results = document.getElementById('command-palette-results');
    if (!results) return;
    
    results.innerHTML = '';
    
    if (filteredCommands.length === 0) {
        results.innerHTML = '<div class="command-palette-item" style="color: #858585; text-align: center; padding: 20px;">No commands found</div>';
        return;
    }
    
    filteredCommands.forEach((cmd, index) => {
        const item = document.createElement('div');
        item.className = 'command-palette-item' + (index === commandPaletteSelectedIndex ? ' selected' : '');
        item.innerHTML = `
            <span class="command-icon">${cmd.icon || '📄'}</span>
            <span class="command-label">${cmd.label}</span>
            ${cmd.shortcut ? `<span class="command-shortcut">${cmd.shortcut}</span>` : ''}
        `;
        item.onclick = () => executeCommand(cmd);
        results.appendChild(item);
    });
    
    // Scroll selected item into view
    const selected = results.querySelector('.selected');
    if (selected) selected.scrollIntoView({ block: 'nearest' });
}

function filterCommands(query) {
    if (!query) {
        filteredCommands = [...commandPaletteCommands];
    } else {
        const lowerQuery = query.toLowerCase();
        filteredCommands = commandPaletteCommands.filter(cmd => 
            cmd.label.toLowerCase().includes(lowerQuery) ||
            cmd.id.toLowerCase().includes(lowerQuery)
        );
    }
    commandPaletteSelectedIndex = 0;
    renderCommandPalette();
}

function executeCommand(cmd) {
    closeCommandPalette();
    if (cmd.action) {
        try {
            cmd.action();
        } catch (error) {
            console.error('Error executing command:', error);
        }
    }
}

// Command Palette Event Handlers
document.addEventListener('DOMContentLoaded', function() {
    const input = document.getElementById('command-palette-input');
    if (input) {
        input.addEventListener('input', (e) => {
            filterCommands(e.target.value);
        });
        
        input.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                closeCommandPalette();
            } else if (e.key === 'ArrowDown') {
                e.preventDefault();
                commandPaletteSelectedIndex = Math.min(commandPaletteSelectedIndex + 1, filteredCommands.length - 1);
                renderCommandPalette();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                commandPaletteSelectedIndex = Math.max(commandPaletteSelectedIndex - 1, 0);
                renderCommandPalette();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                if (filteredCommands[commandPaletteSelectedIndex]) {
                    executeCommand(filteredCommands[commandPaletteSelectedIndex]);
                }
            }
        });
    }
});

// Help Menu
function showHelpMenu() {
    const modal = document.getElementById('help-menu-modal');
    if (modal) {
        modal.style.display = 'flex';
        switchHelpTab('welcome');
    }
}

function closeHelpMenu() {
    const modal = document.getElementById('help-menu-modal');
    if (modal) modal.style.display = 'none';
}

function switchHelpTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.help-tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.help-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Show selected tab
    const content = document.getElementById(`help-${tabName}`);
    const tabButton = Array.from(document.querySelectorAll('.help-tab')).find(btn => 
        btn.textContent.toLowerCase().includes(tabName === 'welcome' ? 'welcome' : 
        tabName === 'shortcuts' ? 'keyboard' : 
        tabName === 'docs' ? 'documentation' : 
        tabName === 'tips' ? 'tips' : 'about')
    );
    
    if (content) content.classList.add('active');
    if (tabButton) tabButton.classList.add('active');
}

// Close help menu on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const helpModal = document.getElementById('help-menu-modal');
        if (helpModal && helpModal.style.display !== 'none') {
            closeHelpMenu();
        }
        const commandPalette = document.getElementById('command-palette');
        if (commandPalette && commandPalette.style.display !== 'none') {
            closeCommandPalette();
        }
    }
});

// Keyboard Shortcuts
document.addEventListener('keydown', (e) => {
    // Command Palette (Ctrl+Shift+P)
    if (e.ctrlKey && e.shiftKey && e.key === 'P') {
        e.preventDefault();
        showCommandPalette();
        return;
    }
    
    // Keyboard Shortcuts (Ctrl+K Ctrl+S)
    if (e.ctrlKey && e.key === 'k' && !e.shiftKey) {
        // Wait for next key press
        const handler = (e2) => {
            if (e2.ctrlKey && e2.key === 's') {
                e2.preventDefault();
                showHelpMenu();
                setTimeout(() => switchHelpTab('shortcuts'), 100);
            }
            document.removeEventListener('keydown', handler);
        };
        document.addEventListener('keydown', handler);
        return;
    }
    
    // Settings (Ctrl+,)
    if (e.ctrlKey && e.key === ',') {
        e.preventDefault();
        switchView('settings');
        return;
    }
    
    // Save (Ctrl+S)
    if (e.ctrlKey && e.key === 's' && !e.shiftKey) {
        e.preventDefault();
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) {
            saveFile(activeTab.dataset.path);
        }
        return;
    }
    
    // Toggle Terminal (Ctrl+`)
    if (e.ctrlKey && e.key === '`') {
        e.preventDefault();
        toggleTerminal();
        return;
    }
    
    // Toggle Sidebar (Ctrl+B)
    if (e.ctrlKey && e.key === 'b' && !e.shiftKey) {
        e.preventDefault();
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.display = sidebar.style.display === 'none' ? 'flex' : 'none';
        }
        return;
    }
    
    // Toggle Panel (Ctrl+J)
    if (e.ctrlKey && e.key === 'j' && !e.shiftKey) {
        e.preventDefault();
        toggleTerminal();
        return;
    }
    
    // New File (Ctrl+N)
    if (e.ctrlKey && e.key === 'n' && !e.shiftKey) {
        e.preventDefault();
        createNewTab();
        return;
    }
    
    // Open File (Ctrl+O)
    if (e.ctrlKey && e.key === 'o' && !e.shiftKey) {
        e.preventDefault();
        const input = document.createElement('input');
        input.type = 'file';
        input.onchange = (ev) => {
            if (ev.target.files[0]) {
                const file = ev.target.files[0];
                const reader = new FileReader();
                reader.onload = (e) => {
                    openFileContent(file.name, e.target.result);
                };
                reader.readAsText(file);
            }
        };
        input.click();
        return;
    }
    
    // Close Tab (Ctrl+W)
    if (e.ctrlKey && e.key === 'w' && !e.shiftKey) {
        e.preventDefault();
        const activeTab = document.querySelector('.tab.active');
        if (activeTab) closeTab(activeTab);
        return;
    }
    
    // AI Assistant (Ctrl+Shift+A)
    if (e.ctrlKey && e.shiftKey && e.key === 'A') {
        e.preventDefault();
        switchView('ai');
        return;
    }
    
    // RedTeam Toolkit (Ctrl+Shift+T)
    if (e.ctrlKey && e.shiftKey && e.key === 'T') {
        e.preventDefault();
        switchView('toolkit');
        loadToolkit();
        return;
    }
    
    // Browser Preview (Ctrl+Shift+B)
    if (e.ctrlKey && e.shiftKey && e.key === 'B') {
        e.preventDefault();
        switchView('browser');
        return;
    }
    
    // Find (Ctrl+F) - handled by Monaco
    // Replace (Ctrl+H) - handled by Monaco
    // Format (Shift+Alt+F) - handled by Monaco
    // Comment (Ctrl+/) - handled by Monaco
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

// SignNow Checker Functions
async function startSignNowChecker() {
    const comboFile = document.getElementById('signnow-combo-file')?.value || 'combo.txt';
    const delay = parseFloat(document.getElementById('signnow-delay')?.value || '1.0');
    const timeout = parseInt(document.getElementById('signnow-timeout')?.value || '10');
    
    // Show terminal panel
    const terminalPanel = document.getElementById('terminal-panel');
    if (terminalPanel) {
        terminalPanel.style.display = 'flex';
        const terminalTab = document.querySelector('.terminal-tab[data-tab="terminal"]');
        if (terminalTab) {
            terminalTab.click();
        }
    }
    
    // Show status
    const statusEl = document.getElementById('terminal-status');
    const statusText = document.getElementById('terminal-status-text');
    if (statusEl && statusText) {
        statusEl.style.display = 'block';
        statusText.textContent = 'Starting SignNow checker...';
        statusText.style.color = '#4ec9b0';
    }
    
    try {
        const response = await fetch('/api/signnow/check', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                combo_file: comboFile,
                delay: delay,
                timeout: timeout
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            if (statusText) {
                statusText.textContent = '✓ Checker started - check terminal for output';
                statusText.style.color = '#4ec9b0';
                setTimeout(() => {
                    if (statusEl) statusEl.style.display = 'none';
                }, 3000);
            }
        } else {
            appendTerminalOutput(`Error: ${data.error || 'Unknown error'}\n`);
            if (statusText) {
                statusText.textContent = '✗ Error starting checker';
                statusText.style.color = '#f48771';
                setTimeout(() => {
                    if (statusEl) statusEl.style.display = 'none';
                }, 5000);
            }
        }
    } catch (error) {
        console.error('SignNow checker error:', error);
        appendTerminalOutput(`Error: ${error.message}\n`);
        if (statusText) {
            statusText.textContent = '✗ Error: ' + error.message;
            statusText.style.color = '#f48771';
            setTimeout(() => {
                if (statusEl) statusEl.style.display = 'none';
            }, 5000);
        }
    }
}


// RedTeam Toolkit Functions
async function loadToolkit() {
    const categoriesDiv = document.getElementById('toolkit-categories');
    if (!categoriesDiv) return;
    
    categoriesDiv.innerHTML = '<div style="color: #858585; padding: 20px; text-align: center;">Loading RedTeam Toolkit...</div>';
    
    try {
        const response = await fetch('/api/toolkit/list');
        
        if (!response.ok) {
            // Try to get error message from response
            let errorMsg = `HTTP ${response.status}: ${response.statusText}`;
            try {
                const errorData = await response.json();
                errorMsg = errorData.error || errorMsg;
                if (errorData.traceback) {
                    console.error('Toolkit error traceback:', errorData.traceback);
                }
            } catch (e) {
                // Response is not JSON
            }
            categoriesDiv.innerHTML = `<div style="color: #f48771; padding: 20px;">Error loading toolkit: ${errorMsg}</div>`;
            console.error('Toolkit API error:', response.status, errorMsg);
            return;
        }
        
        const data = await response.json();
        
        console.log('[TOOLKIT] API Response:', {
            success: data.success,
            total: data.total,
            toolsCount: data.tools ? data.tools.length : 0,
            categories: data.categories
        });
        
        if (data.success && data.tools) {
            // Filter out "Red Team Tips" category if present
            const filteredTools = data.tools.filter(tool => tool.category !== 'Red Team Tips');
            
            if (filteredTools.length !== data.tools.length) {
                console.log(`[TOOLKIT] Filtered out ${data.tools.length - filteredTools.length} tools from Red Team Tips`);
            }
            
            console.log(`[TOOLKIT] Displaying ${filteredTools.length} tools`);
            displayToolkit(filteredTools);
        } else {
            categoriesDiv.innerHTML = `<div style="color: #f48771; padding: 20px;">Error loading toolkit: ${data.error || 'Unknown error'}</div>`;
        }
    } catch (error) {
        console.error('Toolkit load error:', error);
        categoriesDiv.innerHTML = `<div style="color: #f48771; padding: 20px;">Error loading toolkit: ${error.message}</div>`;
    }
}

function displayToolkit(tools) {
    const categoriesDiv = document.getElementById('toolkit-categories');
    const categoryNav = document.getElementById('toolkit-category-nav');
    const categoryLinks = document.getElementById('category-links');
    if (!categoriesDiv) return;
    
    // Group tools by category
    const categories = {};
    tools.forEach(tool => {
        // Ensure tool has required properties (defensive check)
        if (!tool || typeof tool !== 'object') {
            console.warn('[TOOLKIT] Invalid tool object:', tool);
            return;
        }
        if (!tool.name || typeof tool.name !== 'string' || tool.name.trim() === '') {
            console.warn('[TOOLKIT] Tool missing or invalid name property:', tool);
            return; // Skip tools without valid names
        }
        const category = (tool.category && String(tool.category)) || 'Other';
        if (!categories[category]) {
            categories[category] = [];
        }
        categories[category].push(tool);
    });
    
    // Build category navigation
    let navHtml = '';
    const sortedCategories = Object.keys(categories).sort();
    sortedCategories.forEach(category => {
        // Ensure category is a string before processing
        const categoryStr = String(category || 'other');
        const categoryId = categoryStr.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
        navHtml += `<button onclick="scrollToCategory('${categoryId}')" style="padding: 6px 12px; background: rgba(78, 201, 176, 0.2); border: 1px solid rgba(78, 201, 176, 0.4); border-radius: 15px; color: #4ec9b0; cursor: pointer; font-size: 12px; transition: all 0.2s;" onmouseover="this.style.background='rgba(78, 201, 176, 0.3)'; this.style.transform='scale(1.05)'" onmouseout="this.style.background='rgba(78, 201, 176, 0.2)'; this.style.transform='scale(1)'">${categoryStr} (${categories[category].length})</button>`;
    });
    if (categoryLinks) {
        categoryLinks.innerHTML = navHtml;
        if (categoryNav) categoryNav.style.display = 'block';
    }
    
    // Build HTML with category IDs for navigation
    let html = '';
    sortedCategories.forEach(category => {
        const categoryTools = categories[category];
        // Ensure category is a string before processing
        const categoryStr = String(category || 'other');
        const categoryId = categoryStr.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
        html += `<div id="category-${categoryId}" class="toolkit-category" style="margin-bottom: 30px; scroll-margin-top: 20px;">`;
        html += `<h3 style="color: #4ec9b0; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #3c3c3c;">${categoryStr} (${categoryTools.length} tools)</h3>`;
        html += `<div class="toolkit-tools" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">`;
        
        categoryTools.forEach(tool => {
            // Ensure tool has required properties (defensive check)
            if (!tool || !tool.name || typeof tool.name !== 'string') {
                console.warn('[TOOLKIT] Skipping invalid tool:', tool);
                return;
            }
            
            // Generate tool ID from name if not present
            const toolNameStr = String(tool.name || 'unknown-tool');
            const toolId = (tool.id && String(tool.id)) || toolNameStr.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
            // Escape tool.id for use in onclick - ensure it's always a string
            const safeToolId = String(toolId || toolNameStr).replace(/'/g, "\\'").replace(/"/g, '&quot;');
            const toolName = toolNameStr;
            const toolDesc = (tool.description && String(tool.description)) || 'No description available';
            html += `<div class="toolkit-tool" style="padding: 15px; background: rgba(78, 201, 176, 0.05); border: 1px solid rgba(78, 201, 176, 0.2); border-radius: 5px; cursor: pointer; transition: all 0.2s;" onmouseover="this.style.background='rgba(78, 201, 176, 0.1)'; this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(78, 201, 176, 0.05)'; this.style.transform='translateY(0)'" onclick="useToolkitTool('${safeToolId}')">`;
            html += `<div style="font-weight: bold; color: #4ec9b0; margin-bottom: 5px;">${toolName}</div>`;
            html += `<div style="color: #858585; font-size: 12px;">${toolDesc}</div>`;
            if (tool.discovered) {
                html += `<div style="color: #858585; font-size: 10px; margin-top: 5px; font-style: italic;">📍 Auto-discovered</div>`;
            }
            html += `</div>`;
        });
        
        html += `</div></div>`;
    });
    
    categoriesDiv.innerHTML = html;
    
    // Setup scroll buttons visibility
    setupToolkitScrollButtons();
}

function scrollToCategory(categoryId) {
    const element = document.getElementById(`category-${categoryId}`);
    if (element) {
        const content = document.getElementById('toolkit-content');
        if (content) {
            const offset = element.offsetTop - content.offsetTop - 20;
            content.scrollTo({
                top: offset,
                behavior: 'smooth'
            });
        }
    }
}

function scrollToolkit(direction) {
    const content = document.getElementById('toolkit-content');
    if (!content) return;
    
    const scrollAmount = 300; // pixels to scroll
    const currentScroll = content.scrollTop;
    const maxScroll = content.scrollHeight - content.clientHeight;
    
    if (direction === 'up') {
        content.scrollTo({
            top: Math.max(0, currentScroll - scrollAmount),
            behavior: 'smooth'
        });
    } else if (direction === 'down') {
        content.scrollTo({
            top: Math.min(maxScroll, currentScroll + scrollAmount),
            behavior: 'smooth'
        });
    }
}

function setupToolkitScrollButtons() {
    const content = document.getElementById('toolkit-content');
    const scrollUpBtn = document.getElementById('toolkit-scroll-up');
    const scrollDownBtn = document.getElementById('toolkit-scroll-down');
    
    if (!content || !scrollUpBtn || !scrollDownBtn) return;
    
    function updateScrollButtons() {
        const scrollTop = content.scrollTop;
        const scrollHeight = content.scrollHeight;
        const clientHeight = content.clientHeight;
        const maxScroll = scrollHeight - clientHeight;
        
        // Show/hide buttons based on scroll position
        if (scrollTop > 50) {
            scrollUpBtn.style.display = 'block';
        } else {
            scrollUpBtn.style.display = 'none';
        }
        
        if (scrollTop < maxScroll - 50) {
            scrollDownBtn.style.display = 'block';
        } else {
            scrollDownBtn.style.display = 'none';
        }
    }
    
    // Update on scroll
    content.addEventListener('scroll', updateScrollButtons);
    
    // Initial update
    updateScrollButtons();
    
    // Update on resize
    window.addEventListener('resize', updateScrollButtons);
}

function searchToolkit(query) {
    const tools = document.querySelectorAll('.toolkit-tool');
    const categories = document.querySelectorAll('.toolkit-category');
    const lowerQuery = query.toLowerCase();
    
    if (!query || query.trim() === '') {
        // Show all tools and categories
        tools.forEach(tool => tool.style.display = '');
        categories.forEach(cat => cat.style.display = '');
        setupToolkitScrollButtons();
        return;
    }
    
    tools.forEach(tool => {
        const text = tool.textContent.toLowerCase();
        if (text.includes(lowerQuery)) {
            tool.style.display = '';
        } else {
            tool.style.display = 'none';
        }
    });
    
    // Hide categories with no visible tools
    categories.forEach(category => {
        const allTools = category.querySelectorAll('.toolkit-tool');
        let hasVisible = false;
        allTools.forEach(tool => {
            if (tool.style.display !== 'none') {
                hasVisible = true;
            }
        });
        if (!hasVisible) {
            category.style.display = 'none';
        } else {
            category.style.display = '';
        }
    });
    
    setupToolkitScrollButtons();
}

function useToolkitTool(toolId) {
    // Ask AI to use the tool
    const toolName = toolId.replace(/-/g, ' ');
    const message = `Use the RedTeam tool: ${toolName}. Install it if needed and show me how to use it.`;
    
    // Switch to AI view and send message
    switchView('ai');
    setTimeout(() => {
        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            chatInput.value = message;
            sendChatMessage();
        }
    }, 100);
}

function refreshToolkit() {
    loadToolkit();
    // Reset scroll position
    const content = document.getElementById('toolkit-content');
    if (content) {
        content.scrollTop = 0;
    }
}

// SSH Connection Functions
function toggleSSHAuthMethod() {
    const method = document.getElementById('ssh-auth-method').value;
    const passwordGroup = document.getElementById('ssh-password-group');
    const keyGroup = document.getElementById('ssh-key-group');
    const keyPassphraseGroup = document.getElementById('ssh-key-passphrase-group');
    
    if (method === 'password') {
        passwordGroup.style.display = 'block';
        keyGroup.style.display = 'none';
        keyPassphraseGroup.style.display = 'none';
    } else {
        passwordGroup.style.display = 'none';
        keyGroup.style.display = 'block';
        keyPassphraseGroup.style.display = 'block';
    }
}

async function addSSHConnection() {
    const host = document.getElementById('ssh-host').value.trim();
    const port = parseInt(document.getElementById('ssh-port').value) || 22;
    const username = document.getElementById('ssh-username').value.trim();
    const authMethod = document.getElementById('ssh-auth-method').value;
    const password = authMethod === 'password' ? document.getElementById('ssh-password').value : null;
    const keyPath = authMethod === 'key' ? document.getElementById('ssh-key-path').value.trim() : null;
    const name = document.getElementById('ssh-name').value.trim() || `${username}@${host}`;
    
    if (!host || !username) {
        alert('Please fill in Host and Username');
        return;
    }
    
    if (authMethod === 'password' && !password) {
        alert('Please enter password');
        return;
    }
    
    if (authMethod === 'key' && !keyPath) {
        alert('Please enter private key path');
        return;
    }
    
    try {
        const response = await fetch('/api/ssh/add', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                host: host,
                port: port,
                username: username,
                auth_method: authMethod,
                password: password,
                key_path: keyPath
            })
        });
        
        const data = await response.json();
        if (data.success) {
            // Clear form
            document.getElementById('ssh-host').value = '';
            document.getElementById('ssh-port').value = '22';
            document.getElementById('ssh-username').value = '';
            document.getElementById('ssh-password').value = '';
            document.getElementById('ssh-key-path').value = '';
            document.getElementById('ssh-name').value = '';
            
            // Reload connections
            loadSSHConnections();
            alert('SSH connection added successfully!');
        } else {
            alert('Error: ' + (data.error || 'Failed to add connection'));
        }
    } catch (error) {
        console.error('SSH connection error:', error);
        alert('Error adding SSH connection: ' + error.message);
    }
}

async function loadSSHConnections() {
    try {
        const response = await fetch('/api/ssh/list');
        const data = await response.json();
        
        const connectionsDiv = document.getElementById('ssh-connections');
        if (!connectionsDiv) return;
        
        if (data.success && data.connections) {
            if (data.connections.length === 0) {
                connectionsDiv.innerHTML = '<div style="color: #858585; padding: 20px; text-align: center;">No SSH connections saved. Add one above.</div>';
                return;
            }
            
            let html = '';
            data.connections.forEach(conn => {
                const status = conn.connected ? '🟢 Connected' : '⚪ Disconnected';
                html += `<div style="padding: 15px; background: rgba(78, 201, 176, 0.05); border: 1px solid rgba(78, 201, 176, 0.2); border-radius: 5px; margin-bottom: 10px;">`;
                html += `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">`;
                html += `<div>`;
                html += `<div style="font-weight: bold; color: #4ec9b0; margin-bottom: 5px;">${conn.name}</div>`;
                html += `<div style="color: #858585; font-size: 12px;">${conn.username}@${conn.host}:${conn.port}</div>`;
                html += `<div style="color: #858585; font-size: 11px; margin-top: 5px;">${status}</div>`;
                html += `</div>`;
                html += `<div style="display: flex; gap: 5px;">`;
                if (conn.connected) {
                    html += `<button onclick="disconnectSSH('${conn.id}')" style="padding: 6px 12px; background: #f48771; border: none; color: white; border-radius: 3px; cursor: pointer; font-size: 11px;">Disconnect</button>`;
                } else {
                    html += `<button onclick="connectSSH('${conn.id}')" style="padding: 6px 12px; background: #4ec9b0; border: none; color: white; border-radius: 3px; cursor: pointer; font-size: 11px;">Connect</button>`;
                }
                html += `<button onclick="deleteSSHConnection('${conn.id}')" style="padding: 6px 12px; background: #f48771; border: none; color: white; border-radius: 3px; cursor: pointer; font-size: 11px;">Delete</button>`;
                html += `</div>`;
                html += `</div>`;
                html += `</div>`;
            });
            
            connectionsDiv.innerHTML = html;
        } else {
            connectionsDiv.innerHTML = '<div style="color: #f48771; padding: 20px;">Error loading connections</div>';
        }
    } catch (error) {
        console.error('Error loading SSH connections:', error);
        document.getElementById('ssh-connections').innerHTML = '<div style="color: #f48771; padding: 20px;">Error loading connections</div>';
    }
}

async function connectSSH(connectionId) {
    try {
        socketio.emit('show_terminal', {});
        socketio.emit('force_show_terminal', {});
        socketio.emit('terminal_output', {'output': `\n🔐 Connecting to SSH connection: ${connectionId}...\n`});
        
        const response = await fetch('/api/ssh/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: connectionId })
        });
        
        const data = await response.json();
        if (data.success) {
            socketio.emit('terminal_output', {'output': `✅ Connected successfully!\n`});
            loadSSHConnections();
        } else {
            socketio.emit('terminal_output', {'output': `❌ Connection failed: ${data.error || 'Unknown error'}\n`});
        }
    } catch (error) {
        console.error('SSH connect error:', error);
        socketio.emit('terminal_output', {'output': `❌ Error: ${error.message}\n`});
    }
}

async function disconnectSSH(connectionId) {
    try {
        const response = await fetch('/api/ssh/disconnect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: connectionId })
        });
        
        const data = await response.json();
        if (data.success) {
            loadSSHConnections();
        }
    } catch (error) {
        console.error('SSH disconnect error:', error);
    }
}

async function deleteSSHConnection(connectionId) {
    if (!confirm('Are you sure you want to delete this SSH connection?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/ssh/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: connectionId })
        });
        
        const data = await response.json();
        if (data.success) {
            loadSSHConnections();
        } else {
            alert('Error: ' + (data.error || 'Failed to delete connection'));
        }
    } catch (error) {
        console.error('SSH delete error:', error);
        alert('Error deleting connection: ' + error.message);
    }
}

function refreshSSHConnections() {
    loadSSHConnections();
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
    
    // Load toolkit when toolkit view is opened
    if (view === 'toolkit') {
        loadToolkit();
    }
    
    // Load toolkit status when AI view is opened
    if (view === 'ai') {
        setTimeout(() => refreshToolkitStatus(), 100);
    }
    
    // Refresh debug view when opened
    if (view === 'debug') {
        setTimeout(() => {
            updateBreakpointsList();
            if (isDebugging) {
                updateDebugVariables();
                updateDebugCallStack();
            }
        }, 100);
    }
}

// Initialization is handled in initOtherComponents()

