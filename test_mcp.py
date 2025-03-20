#!/usr/bin/env python3
"""
Simple script to test if MCP package is working correctly.
Run this script to verify the MCP installation before attempting to run the full server.
"""
import sys
import traceback

print("Testing MCP installation...")

try:
    print("Importing mcp package...")
    from mcp.server.fastmcp import FastMCP
    print("✅ Successfully imported FastMCP")
    
    print("Creating FastMCP instance...")
    mcp = FastMCP("test-server")
    print("✅ Successfully created FastMCP instance")
    
    print("Registering simple tool...")
    @mcp.tool()
    async def hello() -> str:
        return "Hello, world!"
    print("✅ Successfully registered tool")
    
    print("All tests passed! MCP appears to be correctly installed.")
    print("\nNext steps:")
    print("1. First try running the debug_server.py script")
    print("2. Then try running the main server.py script if debug_server works")

except ImportError as e:
    print(f"❌ Error importing MCP: {str(e)}")
    print("\nTry reinstalling the MCP package with:")
    print("pip uninstall mcp")
    print("pip install 'mcp[cli]'")
    
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")
    traceback.print_exc()
    
    print("\nTroubleshooting tips:")
    print("1. Make sure you're using Python 3.8 or newer")
    print("2. Check that you're in the correct virtual environment")
    print("3. Try reinstalling dependencies: pip install -r requirements.txt")
