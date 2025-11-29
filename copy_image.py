import shutil
import os

source = r'C:\Users\Administrator\Downloads\tai.jpeg'
destination = r'C:\Users\Administrator\Auto_Punch IDE\static\images\hacking-bg.jpg'

# Create directory if it doesn't exist
os.makedirs(os.path.dirname(destination), exist_ok=True)

# Check if source exists
if os.path.exists(source):
    try:
        # Copy the file
        shutil.copy2(source, destination)
        if os.path.exists(destination):
            file_size = os.path.getsize(destination)
            print("=" * 50)
            print("SUCCESS: Image copied successfully!")
            print("=" * 50)
            print(f"Source: {source}")
            print(f"Destination: {destination}")
            print(f"File size: {file_size:,} bytes")
            print("=" * 50)
            print("\nNext steps:")
            print("1. Restart the IDE server (if running)")
            print("2. Hard refresh browser: Ctrl + Shift + R")
            print("3. Go to Settings -> Appearance -> Theme")
            print("4. Select 'Hacking Mode (Cyberpunk)'")
            print("\nThe Tai Lung background will appear!")
        else:
            print("ERROR: Copy failed - destination file not found")
    except Exception as e:
        print(f"ERROR: {e}")
else:
    print(f"ERROR: Source file not found: {source}")
    print("\nPlease check:")
    print("1. The file exists at the specified path")
    print("2. You have permission to read the file")

