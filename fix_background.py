#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix background image placement"""

import shutil
import os
import sys

def main():
    source = r'C:\Users\Administrator\Downloads\tai.jpeg'
    dest_dir = r'C:\Users\Administrator\Auto_Punch IDE\static\images'
    destination = os.path.join(dest_dir, 'hacking-bg.jpg')
    
    print("=" * 60)
    print("Auto_Punch IDE - Background Image Setup")
    print("=" * 60)
    print()
    
    # Check source
    if not os.path.exists(source):
        print(f"ERROR: Source file not found: {source}")
        print("\nPlease make sure the file exists at that location.")
        return False
    
    print(f"Source file found: {source}")
    print(f"File size: {os.path.getsize(source):,} bytes")
    print()
    
    # Create destination directory
    os.makedirs(dest_dir, exist_ok=True)
    print(f"Destination directory: {dest_dir}")
    
    # Copy file
    try:
        print("Copying file...")
        shutil.copy2(source, destination)
        
        if os.path.exists(destination):
            file_size = os.path.getsize(destination)
            print()
            print("=" * 60)
            print("SUCCESS! Image copied successfully!")
            print("=" * 60)
            print(f"Source: {source}")
            print(f"Destination: {destination}")
            print(f"File size: {file_size:,} bytes")
            print()
            print("File is ready to use!")
            print()
            print("Next steps:")
            print("1. Restart the IDE server (if running)")
            print("2. Hard refresh browser: Ctrl + Shift + R")
            print("3. Go to Settings -> Appearance -> Theme")
            print("4. Select 'Hacking Mode (Cyberpunk)'")
            print()
            print("The background image will appear!")
            print("=" * 60)
            return True
        else:
            print("ERROR: Copy failed - destination file not created")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)

