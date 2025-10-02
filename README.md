# Microsoft Calendar MCP Server

A Model Context Protocol (MCP) server for managing Microsoft Outlook calendar events using Microsoft Graph API. This server provides tools for fetching calendar events within specified date ranges and integrates seamlessly with Claude Desktop, MCP Inspector, and other MCP-compatible clients.

**🚀 Current Status**: Production-ready with dual transport support (stdio and SSE) for maximum compatibility.

## Features

- 📅 Fetch calendar events for specific users and date ranges
- 🔐 Secure Microsoft Graph API authentication using Azure AD
- 🌐 Support for timezone-aware operations
- 🔧 FastMCP-based server with dual transport support:
  - **stdio transport**: For Claude Desktop and CLI clients
  - **SSE transport**: For MCP Inspector and web-based clients
- 📊 Detailed event information including attendees and metadata
- 🏥 Health check endpoint for monitoring

## Prerequisites

- Python 3.13 or higher
- Azure AD application with appropriate Microsoft Graph API permissions:
  - `Calendars.Read` or `Calendars.ReadWrite`
  - `User.Read` (for accessing user information)
- Service principal credentials (Client ID, Client Secret, Tenant ID)

## Installation

### Method 1: Using UV (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-server-outlook-calendar
   ```

2. Install dependencies using UV:
   ```bash
   uv sync
   ```

### Method 2: Using pip

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-server-outlook-calendar
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Unix/macOS
   # OR
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Configuration

4. Create a `.env` file in the project root with your Azure AD credentials:
   ```env
   AZURE_TENANT_ID=your_tenant_id_here
   AZURE_CLIENT_ID=your_client_id_here
   AZURE_CLIENT_SECRET=your_client_secret_here
   ```

5. Test your connection:
   ```bash
   # Using UV
   uv run python test_connection.py
   
   # Using pip
   python test_connection.py
   ```

## Usage

### Running the Server

#### Method 1: SSE Transport (for MCP Inspector)

```bash
# Using UV (recommended)
uv run python main.py

# Using pip
python main.py
```

**Server will run on**: `http://0.0.0.0:8000`
**SSE Endpoint**: `http://0.0.0.0:8000/sse`
**Health Check**: `http://0.0.0.0:8000/health`

#### Method 2: Stdio Transport (for Claude Desktop)

```bash
# Using UV
uv run python -m ms_calendar.server

# Using pip
python -m ms_calendar.server
```

#### Running with Claude Desktop (MCP)

To integrate this server with Claude Desktop using MCP (Model Context Protocol):

1. Add the server configuration to your Claude Desktop config file:

   **On macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
   **On Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

   ```json
   {
     "mcpServers": {
       "ms-calendar": {
         "command": "python",
         "args": [
           "-m", "ms_calendar.server"
         ],
         "cwd": "/path/to/your/mcp-server-outlook-calendar"
       }
     }
   }
   ```
   
   Note: Update the `cwd` path to match your local project location.

2. Restart Claude Desktop to load the new server configuration.

The server will be available as a tool within Claude Desktop for calendar operations.

### As a Python Library

```python
from ms_calendar.calendar_service import fetch_all_calendar_events, get_graph_client
from datetime import datetime, timedelta
import asyncio

async def main():
    # Get a Graph client
    graph_client = get_graph_client()
    
    # Fetch events for the next 7 days
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=7)
    
    events = await fetch_all_calendar_events(
        graph_client=graph_client,
        user_id="user@example.com",
        start_date=start_date,
        end_date=end_date
    )
    
    for event in events:
        print(f"Event: {event.subject} - {event.start.date_time} to {event.end.date_time}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Running with MCP Inspector

For development and testing, you can use the MCP Inspector with SSE transport:

1. Start the server in SSE mode:
   ```bash
   # Using UV (recommended)
   uv run python main.py
   
   # Using pip
   python main.py
   ```

2. Run the MCP Inspector:
   ```bash
   npx @modelcontextprotocol/inspector
   ```

3. Configure the inspector:
   - **Transport Type:** `SSE`
   - **URL:** `http://127.0.0.1:8000/sse`
   - The inspector will automatically open in your browser

**Note**: The SSE transport is currently marked as deprecated in favor of StreamableHttp, but it remains fully functional for MCP Inspector usage.

## API Reference

### get_calendar_events_time_specific

Fetch calendar events for a user within a specified date range using Microsoft Graph API.

**Arguments:**
- `user_id` (str): Microsoft Graph user ID or email address (e.g., "user@example.com")
- `start` (str): Start date in ISO format (default: "2025-06-16")
- `end` (str): End date in ISO format (default: "2025-06-16")  
- `timezone` (str): IANA timezone identifier (default: "Asia/Manila")

**Returns:**
- `dict`: JSON object containing:
  - `count` (int): Number of events found
  - `events` (list): Array of event objects with:
    - `id` (str): Event unique identifier
    - `subject` (str): Event title/subject
    - `attendees` (list): Array of attendee objects with email, name, and type
- `str`: Error message if the operation fails

**Example Response:**
```json
{
  "count": 2,
  "events": [
    {
      "id": "AAMkAGI2...",
      "subject": "Team Meeting",
      "attendees": [
        {
          "email": "john@example.com",
          "name": "John Doe",
          "type": "required"
        }
      ]
    }
  ]
}
```

### /health

Health check endpoint for monitoring server status.

**HTTP GET** `/health`

**Returns JSON:**
- `{"status": "ok"}`

## Azure AD Setup

To use this server, you'll need to set up an Azure AD application:

1. **Register an Application:**
   - Go to [Azure Portal](https://portal.azure.com) → Azure Active Directory → App registrations
   - Click "New registration"
   - Provide a name and select account types
   - Register the application

2. **Configure API Permissions:**
   - Go to "API permissions" in your app
   - Add Microsoft Graph permissions:
     - `Calendars.Read` (to read calendar events)
     - `User.Read` (to read user information)
   - Grant admin consent for your organization

3. **Create Client Secret:**
   - Go to "Certificates & secrets"
   - Create a new client secret
   - Copy the secret value (you won't see it again)

4. **Note Application Details:**
   - Copy the Application (client) ID
   - Copy the Directory (tenant) ID
   - Use these in your `.env` file

## Testing & Coverage

- Tests use `pytest`, `pytest-asyncio`, and `pytest-cov`
- Microsoft Graph API calls can be mocked for testing
- Run all tests with:
  ```bash
  pytest
  ```
- Generate an HTML coverage report with:
  ```bash
  pytest --cov=src --cov-report=html
  open htmlcov/index.html
  ```

## Transport Support

### SSE Transport (Server-Sent Events)
- **Entry Point**: `main.py`
- **Port**: 8000 (default)
- **Use Cases**: MCP Inspector, web-based clients, development/testing
- **Features**: Real-time communication, HTTP debugging support
- **Health Check**: `GET /health` returns `{"status": "ok"}`

### Stdio Transport
- **Entry Point**: `ms_calendar.server` module
- **Use Cases**: Claude Desktop, CLI clients, production deployments
- **Features**: Lower overhead, direct process communication

## Development

This project uses modern Python development tools:
- **Package Manager**: UV (recommended) or pip
- **Framework**: FastMCP for MCP server implementation
- **API Client**: Microsoft Graph SDK for calendar access
- **Authentication**: Azure Identity for secure Azure AD integration
- **Code Quality**:
  - **Black** for code formatting (88-char line length)
  - **Flake8** for linting with custom rules
  - **MyPy** for strict type checking
- **Testing**: pytest with asyncio support and coverage reporting
- **Type Safety**: Full mypy support with `py.typed` marker

## Project Analysis

For a comprehensive technical analysis of this project, including architecture details, security considerations, and performance characteristics, see [ANALYSIS.md](./ANALYSIS.md).

## References

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/quickstart/server)
- [Microsoft Graph API - Calendar](https://docs.microsoft.com/en-us/graph/api/resources/calendar)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Azure Identity Python SDK](https://docs.microsoft.com/en-us/python/api/azure-identity/)
- [UV Package Manager](https://github.com/astral-sh/uv)
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector)