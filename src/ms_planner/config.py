"""
Configuration and constants for Microsoft Graph Planner integration.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Microsoft Graph API endpoints
GRAPH_API_BASE_URL = "https://graph.microsoft.com/v1.0/"
AUTHORITY_URL = "https://login.microsoftonline.com/"

# Required environment variables
REQUIRED_ENV_VARS = [
    "AZURE_TENANT_ID",
    "AZURE_CLIENT_ID",
    "AZURE_CLIENT_SECRET"
]

def validate_config():
    """Validate that all required environment variables are set."""
    missing_vars = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}. "
            "Please check your .env file."
        )

# Validate configuration on import
try:
    validate_config()
except ValueError as e:
    import warnings
    warnings.warn(str(e))
