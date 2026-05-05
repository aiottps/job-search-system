import sys
import os
import subprocess

def check_env():
    print("=== Environment Check ===")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Version: {sys.version}")
    print(f"Current Directory: {os.getcwd()}")
    
    # Check WindowsApps
    if "WindowsApps" in sys.executable:
        print("\n[WARNING] You are using the Microsoft Store Python stub (WindowsApps).")
        print("This can cause issues with pip and package paths.")
        print("RECOMMENDATION: Install official Python from python.org and disable 'App execution aliases' in Windows Settings.\n")

    # Check UTF-8
    print(f"PYTHONUTF8: {os.environ.get('PYTHONUTF8')}")
    print(f"Filesystem Encoding: {sys.getfilesystemencoding()}")
    print(f"Stdout Encoding: {sys.stdout.encoding}")

    # Check pip
    print("\nChecking pip...")
    try:
        pip_v = subprocess.check_output([sys.executable, "-m", "pip", "--version"], text=True)
        print(f"pip check: {pip_v.strip()}")
    except Exception as e:
        print(f"pip check failed: {e}")

    # Check pytest
    print("\nChecking pytest...")
    try:
        import pytest
        print(f"pytest version: {pytest.__version__}")
    except ImportError:
        print("pytest NOT installed. Run 'python -m pip install pytest'")

    # Check app import
    print("\nChecking app import...")
    sys.path.append(os.getcwd())
    try:
        from app.schemas.job import JobItem
        print("App import: SUCCESS")
    except ImportError as e:
        print(f"App import failed: {e}")
        print(f"Path searched: {sys.path}")

if __name__ == "__main__":
    check_env()
