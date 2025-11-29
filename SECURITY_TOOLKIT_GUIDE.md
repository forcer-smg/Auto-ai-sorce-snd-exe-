# Security Toolkit Integration Guide

## Overview
The Security Toolkit provides full AI control over Git, Nmap, and Burp Suite Community Edition.

## Available Tools

### 1. Git Operations
Full Git integration with AI control.

**Available Commands:**
- `[GIT: status]` - Check git status
- `[GIT: add .]` - Stage all files
- `[GIT: commit "message"]` - Commit changes
- `[GIT: push origin main]` - Push to remote
- `[GIT: pull origin main]` - Pull from remote
- `[GIT: clone https://github.com/user/repo.git]` - Clone repository
- `[GIT: branch create feature-branch]` - Create new branch
- `[GIT: log 10]` - View commit log

**API Endpoint:**
```
POST /api/git/command
{
    "action": "status|add|commit|push|pull|clone|branch|log|diff",
    "params": {
        "message": "commit message",
        "files": ["file1.txt", "file2.txt"],
        "remote": "origin",
        "branch": "main",
        "repo_url": "https://github.com/user/repo.git",
        "destination": "./local-path"
    }
}
```

### 2. Nmap Scanner
Full Nmap integration for network scanning.

**Available Commands:**
- `[NMAP: scan 192.168.1.1]` - Basic scan
- `[NMAP: quick 192.168.1.0/24]` - Quick scan (top 1000 ports)
- `[NMAP: full 192.168.1.1]` - Full scan (all ports)
- `[NMAP: stealth 192.168.1.1]` - Stealth SYN scan
- `[NMAP: version 192.168.1.1]` - Version detection
- `[NMAP: os 192.168.1.1]` - OS detection
- `[NMAP: vuln target.com]` - Vulnerability scan

**API Endpoint:**
```
POST /api/nmap/scan
{
    "action": "scan|quick|full|stealth|version|os|vuln",
    "target": "192.168.1.1",
    "options": ["-sV", "-p", "80,443"],
    "format": "text|json|xml"
}
```

### 3. Burp Suite Community Edition
Launch and control Burp Suite.

**Available Commands:**
- `[BURP: launch]` - Launch Burp Suite GUI
- `[BURP: launch project.burp]` - Launch with project file
- `[BURP: status]` - Check installation status

**API Endpoint:**
```
POST /api/burp/command
{
    "action": "launch|status",
    "params": {
        "project_file": "path/to/project.burp",
        "headless": false
    }
}
```

## Installation Requirements

### Git
- **Windows**: Install from https://git-scm.com/download/win
- **Linux**: `sudo apt-get install git` or `sudo yum install git`
- **macOS**: `brew install git` or included with Xcode

### Nmap
- **Windows**: Download from https://nmap.org/download.html
  - Install to: `C:\Program Files (x86)\Nmap\` or `C:\Program Files\Nmap\`
- **Linux**: `sudo apt-get install nmap` or `sudo yum install nmap`
- **macOS**: `brew install nmap`

### Burp Suite Community Edition
- **Download**: https://portswigger.net/burp/communitydownload
- **Installation**: 
  - Extract to: `C:\Program Files\BurpSuiteCommunity\`
  - Or: `C:\Program Files (x86)\BurpSuiteCommunity\`
- **Requirements**: Java 11 or higher
  - Download Java: https://www.oracle.com/java/technologies/downloads/

## Usage Examples

### Example 1: Git Workflow
```
User: "Check git status and commit all changes with message 'Update security toolkit'"

AI will execute:
[GIT: status]
[GIT: add .]
[GIT: commit "Update security toolkit"]
```

### Example 2: Network Scanning
```
User: "Scan my local network 192.168.1.0/24 for open ports"

AI will execute:
[NMAP: quick 192.168.1.0/24]
```

### Example 3: Vulnerability Assessment
```
User: "Scan target.com for vulnerabilities"

AI will execute:
[NMAP: vuln target.com]
```

### Example 4: Burp Suite Launch
```
User: "Launch Burp Suite for web application testing"

AI will execute:
[BURP: launch]
```

## AI Integration

The AI automatically recognizes these command patterns and executes them:

1. **Git Commands**: `[GIT: action params]`
2. **Nmap Commands**: `[NMAP: action target]`
3. **Burp Commands**: `[BURP: action params]`

The AI can also use direct terminal commands:
- `git status`
- `nmap -sV 192.168.1.1`
- `java -jar burpsuite_community.jar`

## Status Check

Check tool availability:
```
GET /api/security-toolkit/status
```

Response:
```json
{
    "success": true,
    "status": {
        "git": {
            "available": true,
            "workspace": "C:\\Users\\Administrator\\project"
        },
        "nmap": {
            "available": true,
            "path": "nmap"
        },
        "burp_suite": {
            "installed": true,
            "path": "C:\\Program Files\\BurpSuiteCommunity\\burpsuite_community.jar",
            "java_available": true
        }
    }
}
```

## Notes

- All tools run with full AI control
- Nmap scans may take time (up to 5 minutes timeout)
- Burp Suite Community Edition runs in GUI mode only
- Git operations use the current workspace directory
- All commands are logged and visible in the AI chat interface

