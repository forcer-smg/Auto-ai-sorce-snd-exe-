# New Tools Added to RedTeam-Tools Toolkit

## Tools Added

### 1. 365-Stealer
**Repository:** https://github.com/AlteredSecurity/365-Stealer  
**Description:** Phishing simulation tool written in Python3 for executing Illicit Consent Grant attacks in Microsoft 365/Azure AD.

**Features:**
- Azure App Registration automation
- OAuth consent grant attacks
- Token stealing and refresh
- Data exfiltration (Outlook, OneDrive, OneNote)
- Email rule creation
- Mail sending capabilities
- Management portal

**Installation:**
```bash
cd RedTeam-Tools/365-Stealer
pip install -r requirements.txt
```

**Usage:**
```bash
python 365-Stealer.py --help
python 365-Stealer.py --app-registration
python 365-Stealer.py --run-app
```

**Documentation:** See [365-Stealer README](https://github.com/AlteredSecurity/365-Stealer)

### 2. requests-ip-rotator
**Repository:** https://github.com/Ge0rg3/requests-ip-rotator  
**Description:** IP rotation library for Python requests using AWS API Gateway.

**Features:**
- Automatic IP rotation via AWS API Gateway
- Seamless integration with requests library
- Bypass rate limiting
- Geographic IP selection

**Installation:**
```bash
cd RedTeam-Tools/requests-ip-rotator
pip install -r requirements.txt
```

**Usage:**
```python
from requests_ip_rotator import ApiGateway, EXTRA_REGIONS
import requests

gateway = ApiGateway("https://example.com", regions=EXTRA_REGIONS)
gateway.start()

session = requests.Session()
session.mount("https://example.com", gateway)

response = session.get("https://example.com")
```

**Documentation:** See [requests-ip-rotator README](https://github.com/Ge0rg3/requests-ip-rotator)

## Integration with Auto_Punch IDE

Both tools are now available in the RedTeam-Tools directory and can be:

1. **Accessed via Toolkit Panel** - Browse and execute tools from the IDE
2. **Executed via AI Chat** - Ask Auto_Punch Ai to use these tools
3. **Run via Terminal** - Execute directly from integrated terminal

## Adding Tools to Toolkit

To add these tools, run:
```powershell
.\ADD_TOOLKIT_TOOLS.ps1
```

Or manually:
```bash
cd RedTeam-Tools
git clone https://github.com/AlteredSecurity/365-Stealer.git
git clone https://github.com/Ge0rg3/requests-ip-rotator.git
```

## Tool Categories

- **365-Stealer**: Phishing / Initial Access / Credential Access
- **requests-ip-rotator**: Defense Evasion / Infrastructure

## Notes

- Both tools require Python dependencies
- 365-Stealer requires Azure App Registration setup
- requests-ip-rotator requires AWS API Gateway configuration
- Tools are for authorized security testing only

## Next Steps

1. ✅ Tools added to RedTeam-Tools directory
2. Install dependencies for each tool
3. Configure tools as needed
4. Test tool execution from IDE
5. Rebuild app to include tools in distribution

