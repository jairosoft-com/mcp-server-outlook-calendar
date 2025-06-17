"""
Tests for the Microsoft Calendar MCP server.
"""

import pytest
import warnings
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch, Mock

# Suppress deprecation warnings for test execution
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Import the module under test
try:
    from ms_calendar.calendar_service import fetch_all_calendar_events, get_graph_client
    from msgraph.generated.models import Event, EventCollectionResponse
except ImportError:
    raise

# Test functions are being uncommented one by one to identify issues
# First test: fetch_all_calendar_events_success

@pytest.mark.asyncio
async def test_fetch_all_calendar_events_success():
    """Test successful fetching of calendar events."""
    # Create a mock graph client
    mock_graph_client = AsyncMock()
    
    # Create a mock event
    mock_event = MagicMock()
    mock_event.id = "event123"
    mock_event.subject = "Test Event"
    
    # Create a mock response
    mock_response = MagicMock()
    mock_response.value = [mock_event]
    
    # Configure the mock to return our test event
    mock_graph_client.users.by_user_id.return_value.calendar.calendar_view.get.return_value = mock_response
    
    # Call the function with test data
    start = datetime.utcnow()
    end = start + timedelta(days=7)
    events = await fetch_all_calendar_events(mock_graph_client, "user123", start, end)
    
    # Verify the results
    assert len(events) == 1
    assert events[0].id == "event123"
    assert events[0].subject == "Test Event"

@pytest.mark.asyncio
async def test_fetch_all_calendar_events_empty():
    """Test fetching calendar events when there are no events."""
    # Create a mock graph client that returns no events
    mock_graph_client = AsyncMock()
    mock_response = MagicMock()
    mock_response.value = []
    mock_graph_client.users.by_user_id.return_value.calendar.calendar_view.get.return_value = mock_response
    
    # Call the function with test data
    start = datetime.utcnow()
    end = start + timedelta(days=7)
    events = await fetch_all_calendar_events(mock_graph_client, "user123", start, end)
    
    # Verify the results
    assert len(events) == 0

@pytest.mark.asyncio
async def test_get_calendar_events_time_specific():
    """Test the get_calendar_events_time_specific tool."""
    from ms_calendar.server import get_calendar_events_time_specific
    
    # Mock the get_graph_client function
    with patch('ms_calendar.calendar_service.get_graph_client') as mock_get_client:
        # Create a mock graph client
        mock_graph_client = AsyncMock()
        mock_get_client.return_value = mock_graph_client
        
        # Create a mock event
        mock_event = MagicMock()
        mock_event.id = "event123"
        mock_event.subject = "Test Event"
        mock_event.attendees = []
        
        # Create a mock response
        mock_response = MagicMock()
        mock_response.value = [mock_event]
        
        # Configure the mock to return our test event
        mock_graph_client.users.by_user_id.return_value.calendar.calendar_view.get.return_value = mock_response
        
        # Call the function with test data
        result = await get_calendar_events_time_specific(
            user_id="user123",
            start="2025-06-16",
            end="2025-06-17",
            timezone="UTC"
        )
        
        # Verify the results
        assert isinstance(result, dict)
        assert result["count"] == 1
        assert result["events"][0]["id"] == "event123"
        assert result["events"][0]["subject"] == "Test Event"

@pytest.mark.asyncio
async def test_health_check():
    """Test the health check endpoint."""
    from ms_calendar.server import health_check
    
    # Call the function
    result = await health_check()
    
    # Verify the results
    assert result == {"status": "ok"}

# Test error cases
@pytest.mark.asyncio
async def test_invalid_timezone():
    """Test with an invalid timezone."""
    from ms_calendar.server import get_calendar_events_time_specific
    
    # Call the function with an invalid timezone
    with pytest.raises(ValueError) as excinfo:
        await get_calendar_events_time_specific(
            user_id="user123",
            start="2025-06-16",
            end="2025-06-17",
            timezone="Invalid/Timezone"
        )
    
    # Verify the error message
    assert "Invalid timezone" in str(excinfo.value)
