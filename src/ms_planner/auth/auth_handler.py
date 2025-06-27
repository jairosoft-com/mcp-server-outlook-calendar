"""
Authentication handler for Microsoft Graph API using MSAL.
"""
import os
from typing import Dict, Optional

import msal
from dotenv import load_dotenv

from ms_planner.utils.exceptions import AuthenticationError

# Load environment variables
load_dotenv()

class AuthHandler:
    """Handles authentication with Microsoft Graph API."""

    def __init__(self):
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scopes = ["https://graph.microsoft.com/.default"]
        
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            raise AuthenticationError(
                "Missing required environment variables. "
                "Please check AZURE_TENANT_ID, AZURE_CLIENT_ID, and AZURE_CLIENT_SECRET"
            )
    
    def get_token(self) -> Dict[str, str]:
        """
        Acquire a token from Microsoft Identity Platform.
        
        Returns:
            Dict containing the access token and token type.
            
        Raises:
            AuthenticationError: If token acquisition fails.
        """
        app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        result = app.acquire_token_for_client(scopes=self.scopes)
        
        if "access_token" not in result:
            raise AuthenticationError(
                f"Failed to acquire token. Error: {result.get('error')} - {result.get('error_description')}"
            )
            
        return {
            "Authorization": f"Bearer {result['access_token']}",
            "Content-Type": "application/json"
        }
