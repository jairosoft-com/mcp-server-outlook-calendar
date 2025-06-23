# Calendar MCP Server

A lightweight FastMCP service for managing calendar events using Microsoft Graph API.

## Features

- Fetch calendar events for a user within a specified date range
- Support for Microsoft Graph API authentication
- Simple RPC-style interface for calendar operations

## Prerequisites

- Python 3.13 or higher
- Azure AD application with appropriate Graph API permissions
- Service principal credentials (Client ID, Client Secret, Tenant ID)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YourOrg/calendar-mcp-server.git
   cd calendar-mcp-server
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # OR
   source .venv/bin/activate  # On Unix/macOS
   ```

3. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

4. Create a `.env` file in the project root with your Azure AD credentials:
   ```
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   USER_ID=target_user_id
   USER_EMAIL=user@example.com
   ```

## Usage

### Running the Server

#### Standard Execution

```bash
python -m ms_calendar.server
```

#### Running with Claude Desktop (MCP)

To run this server locally with Claude Desktop using MCP (Model Context Protocol):

1. Create an `mcp-config.json` file in your project root with the following content:
   ```json
   {
     "mcpServers": {
       "weather": {
         "command": "uv",
         "args": [
           "--directory",
           "D:\\AI Projects\\mcp-server-weather",
           "run",
           "main.py"
         ]
       }
     }
   }
   ```
   
   Note: Update the directory path to match your local project location.

2. Start the MCP server using the configuration:
   ```bash
   npx @modelcontextprotocol/cli --config mcp-config.json
   ```

The server will start and be available for Claude Desktop to connect to.

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

### As a FastMCP server

```bash
weather-mcp-server --transport stdio
```

Or

```bash
uv run main.py
```

To run the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector
```
Copy the Session token and the Proxy server address (see example below).

```bash
Proxy server listening on 127.0.0.1:6277
Session token: dc7a47f8b6b1a3eede7c507a8d1c9a7f7e6b3ff46c138f8480bbfbae3c45a9e4
```

Open the MCP Inspector in your browser:http://127.0.0.1:6274, and in the Configuration, paste the values to the following fields below:

```
Command: uv 
Argument: run main.py
Inspector Proxy Address: http://127.0.0.1:6274
Proxy Session Token: dc7a47f8b6b1a3eede7c507a8d1c9a7f7e6b3ff46c138f8480bbfbae3c45a9e4
```

## API Reference

### get_alerts

Fetch formatted weather alerts for a given two-letter US state code.

**Arguments:**
- `state` (str): Two-letter uppercase state abbreviation (e.g. "CA").

**Returns:**
- `str`: Formatted alerts separated by `---`, or an error message.

### get_forecast

Fetch formatted weather forecast for a location.

**Arguments:**
- `latitude` (float): Latitude between -90 and 90.
- `longitude` (float): Longitude between -180 and 180.

**Returns:**
- `str`: Forecast for up to next 5 periods or an error message.

### /health

Health check endpoint.

**HTTP GET** `/health`

**Returns JSON:**
- `{"status": "ok"}`

## Testing & Coverage

- Tests use `pytest`, `pytest-asyncio`, and `pytest-cov`.
- Network calls are monkeypatched for isolation in unit tests.
- Run all tests with:
  ```sh
  pytest
  ```
- Generate an HTML coverage report with:
  ```sh
  pytest --cov=src --cov-report=html
  open htmlcov/index.html
  ```

## Fixtures & Mocking

- Test fixtures and monkeypatching are used to mock NWS API responses and isolate tests from network dependencies.
- See `tests/conftest.py` for reusable fixtures.

## References

* [https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed](https://medium.com/data-engineering-with-dremio/building-a-basic-mcp-server-with-python-4c34c41031ed)
* [https://modelcontextprotocol.io/quickstart/server](https://modelcontextprotocol.io/quickstart/server)