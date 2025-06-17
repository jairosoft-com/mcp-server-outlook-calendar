"""Pytest configuration and fixtures for the test suite."""

import json
import os
import sys
import importlib.util
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient


@pytest.fixture(scope="module")
def server_module():
    """Fixture to import the server module dynamically."""
    server_path = os.path.join(
        os.path.dirname(__file__), "..", "src", "ms_calendar", "server.py"
    )
    spec = importlib.util.spec_from_file_location("ms_calendar.server", server_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["ms_calendar.server"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def mock_httpx_client():
    """Fixture to mock httpx.AsyncClient."""
    with patch("httpx.AsyncClient") as mock_client:
        yield mock_client


@pytest.fixture
def mock_graph_client():
    """Fixture to mock the Microsoft Graph client."""
    with patch("ms_calendar.calendar_service.get_graph_client") as mock_client:
        mock_client.return_value = AsyncMock()
        yield mock_client.return_value


@pytest.fixture
def test_client(server_module):
    """Fixture to create a test client for the FastMCP server."""
    from httpx import ASGITransport

    app = server_module.mcp.streamable_http_app()
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


# Add any other common test utilities or fixtures here
