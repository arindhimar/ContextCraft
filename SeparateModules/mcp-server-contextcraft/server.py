from mcp.server.fastmcp import FastMCP

# Use the same display name if you prefer
mcp = FastMCP("ContextCraft", dependencies=[])

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # This blocks and serves indefinitely
    mcp.run()
