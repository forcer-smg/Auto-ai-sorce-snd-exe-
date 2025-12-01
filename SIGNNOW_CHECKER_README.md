# SignNow.com Login Checker

A Python tool to check if email/password combinations are valid on SignNow.com.

## Features

- ✅ Check credentials from combo file
- ✅ Rate limiting (configurable delay)
- ✅ JSON results export
- ✅ Real-time progress display
- ✅ Error handling
- ✅ Supports multiple combo formats

## Usage

### Basic Usage

1. Create a `combo.txt` file with credentials in one of these formats:
   ```
   email:password
   email|password
   ```

   Example:
   ```
   user@example.com:password123
   another@example.com:pass456
   test@example.com|testpass
   ```

2. Run the checker:
   ```bash
   python signnow_checker.py combo.txt
   ```

### Using the Batch File (Windows)

Simply double-click `RUN_SIGNNOW_CHECKER.bat` - it will automatically:
- Check if `combo.txt` exists
- Run the checker
- Save results to `signnow_results.json`

### Advanced Options

```bash
python signnow_checker.py combo.txt [OPTIONS]

Options:
  -d, --delay DELAY     Delay between requests in seconds (default: 1.0)
  -o, --output FILE     Output file for results (default: signnow_results.json)
  -t, --timeout SECONDS Request timeout in seconds (default: 10)
```

### Examples

```bash
# Basic check
python signnow_checker.py combo.txt

# With custom delay (2 seconds between requests)
python signnow_checker.py combo.txt -d 2.0

# Custom output file
python signnow_checker.py combo.txt -o my_results.json

# Fast check (0.5s delay, 5s timeout)
python signnow_checker.py combo.txt -d 0.5 -t 5
```

## Output

Results are saved to a JSON file with the following structure:

```json
{
  "valid": [
    {
      "email": "user@example.com",
      "password": "password123",
      "message": "Valid credentials",
      "timestamp": "2025-11-29T12:00:00"
    }
  ],
  "invalid": [
    {
      "email": "invalid@example.com",
      "message": "Invalid credentials",
      "timestamp": "2025-11-29T12:00:01"
    }
  ],
  "errors": []
}
```

## Combo File Format

The combo file can use either `:` or `|` as separators:

```
email:password
email|password
```

Empty lines and lines starting with `#` are ignored.

## Important Notes

⚠️ **Legal and Ethical Use Only**
- Only use this tool on accounts you own or have explicit permission to test
- Unauthorized access attempts may violate terms of service and laws
- Use responsibly and ethically

⚠️ **Rate Limiting**
- Default delay is 1 second between requests
- SignNow may rate limit if too many requests are made
- Adjust delay with `-d` option if needed

⚠️ **Security**
- Keep combo files secure
- Don't share results files containing valid credentials
- Use strong passwords for your own accounts

## Requirements

- Python 3.7+
- `requests` library

Install dependencies:
```bash
pip install requests
```

## Troubleshooting

### "Connection error"
- Check your internet connection
- SignNow.com may be down
- Try increasing timeout with `-t` option

### "Rate limited (429)"
- Too many requests too quickly
- Increase delay with `-d` option (e.g., `-d 3.0`)

### "File not found"
- Make sure `combo.txt` is in the same directory
- Check file path is correct

## Example Output

```
[*] Starting SignNow checker...
[*] Reading combos from: combo.txt
[*] Delay between requests: 1.0s
------------------------------------------------------------
[*] Found 10 combos to check

[1/10] Checking: user@example.com
    ✗ INVALID - user@example.com - Invalid credentials
[2/10] Checking: test@example.com
    ✓ VALID - test@example.com:password123 - Valid credentials
...

============================================================
CHECK COMPLETE
============================================================
Total checked: 10
Valid: 1
Invalid: 9
Errors: 0

✓ VALID CREDENTIALS:
  test@example.com:password123

[*] Results saved to: signnow_results.json
```

