import sys
import traceback
from mcp.server.fastmcp import FastMCP

# Print startup message to stderr for debugging
print("Starting debug server...", file=sys.stderr)

try:
    # Initialize FastMCP server
    print("Initializing FastMCP server...", file=sys.stderr)
    mcp = FastMCP("lmstudio-bridge")

    @mcp.tool()
    async def debug_test() -> str:
        """Basic test function to verify MCP server is working.
        
        Returns:
            A simple confirmation message
        """
        print("debug_test function called", file=sys.stderr)
        return "MCP server is working correctly!"

    if __name__ == "__main__":
        print("Starting server with stdio transport...", file=sys.stderr)
        # Initialize and run the server
        mcp.run(transport='stdio')
except Exception as e:
    print(f"ERROR: {str(e)}", file=sys.stderr)
    print("Traceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
