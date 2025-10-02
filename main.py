#!/usr/bin/env python3
"""
HTTP version of the MCP server for use with MCP Inspector
"""
from ms_calendar.server import mcp

if __name__ == "__main__":
    # Run on SSE transport for MCP Inspector
    mcp.run(transport="sse")
