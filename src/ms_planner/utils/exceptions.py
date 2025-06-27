"""Custom exceptions for Microsoft Graph Planner integration."""

class PlannerError(Exception):
    """Base exception for all Planner-related errors."""
    pass

class AuthenticationError(PlannerError):
    """Raised when authentication with Microsoft Graph fails."""
    pass

class APIError(PlannerError):
    """Raised when an API request to Microsoft Graph fails."""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API request failed with status {status_code}: {message}")

class ResourceNotFoundError(PlannerError):
    """Raised when a requested resource is not found."""
    pass

class ValidationError(PlannerError):
    """Raised when input validation fails."""
    pass
