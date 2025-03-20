#!/usr/bin/env python3
"""
Verification script to check if all required packages are installed.
This script will check for the presence of essential packages and their versions.
"""
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python version too old: {platform.python_version()}")
        print("   MCP requires Python 3.8 or higher.")
        return False
    else:
        print(f"✅ Python version: {platform.python_version()}")
        return True

def check_package(package_name):
    """Check if a package is installed and get its version."""
    try:
        if package_name == "mcp":
            # Special handling for mcp to test import
            module = __import__(package_name)
            version = getattr(module, "__version__", "unknown")
            print(f"✅ {package_name} is installed (version: {version})")
            return True
        else:
            # Use pip to check other packages
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                for line in result.stdout.splitlines():
                    if line.startswith("Version:"):
                        version = line.split(":", 1)[1].strip()
                        print(f"✅ {package_name} is installed (version: {version})")
                        return True
            print(f"❌ {package_name} is not installed")
            return False
    except ImportError:
        print(f"❌ {package_name} is not installed")
        return False
    except Exception as e:
        print(f"❌ Error checking {package_name}: {str(e)}")
        return False

def check_environment():
    """Check if running in a virtual environment."""
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    if in_venv:
        print(f"✅ Running in virtual environment: {sys.prefix}")
        return True
    else:
        print("⚠️ Not running in a virtual environment")
        print("   It's recommended to use a virtual environment for this project")
        return True  # Not critical

def main():
    """Run all checks."""
    print("🔍 Checking environment setup for Claude-LMStudio Bridge...")
    print("-" * 60)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        success = False
    
    # Check virtual environment
    check_environment()
    
    # Check essential packages
    required_packages = ["mcp", "httpx"]
    for package in required_packages:
        if not check_package(package):
            success = False
    
    print("-" * 60)
    if success:
        print("✅ All essential checks passed! Your environment is ready.")
        print("\nNext steps:")
        print("1. Run 'python test_mcp.py' to test MCP functionality")
        print("2. Run 'python debug_server.py' to test a simple MCP server")
        print("3. Run 'python server.py' to start the full bridge server")
    else:
        print("❌ Some checks failed. Please address the issues above.")
        print("\nCommon solutions:")
        print("1. Install MCP: pip install 'mcp[cli]'")
        print("2. Install httpx: pip install httpx")
        print("3. Upgrade Python to 3.8+: https://www.python.org/downloads/")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
