"""
Graph API client for Microsoft Graph operations.
"""
import json
import logging
from typing import Any, Dict, Optional, Union

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ms_planner.auth.auth_handler import AuthHandler
from ms_planner.utils.exceptions import APIError, ResourceNotFoundError

logger = logging.getLogger(__name__)

class GraphClient:
    """Client for making requests to Microsoft Graph API."""
    
    BASE_URL = "https://graph.microsoft.com/v1.0"
    
    def __init__(self):
        """Initialize the Graph client with authentication."""
        self.auth_handler = AuthHandler()
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "TRACE", "POST", "PATCH"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        
        return session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get the headers with authentication token."""
        return self.auth_handler.get_token()
    
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """Handle the API response and raise appropriate exceptions."""
        if response.status_code == 404:
            raise ResourceNotFoundError("The requested resource was not found.")
            
        if not response.ok:
            try:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', response.text)
            except ValueError:
                error_msg = response.text
                
            raise APIError(
                status_code=response.status_code,
                message=error_msg
            )
            
        if response.status_code == 204:  # No content
            return {}
            
        return response.json()
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Perform a GET request to the Graph API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        logger.debug(f"GET {url} with params: {params}")
        response = self.session.get(url, headers=headers, params=params)
        return self._handle_response(response)
    
    def post(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a POST request to the Graph API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        logger.debug(f"POST {url} with data: {data}")
        response = self.session.post(url, headers=headers, json=data)
        return self._handle_response(response)
    
    def patch(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a PATCH request to the Graph API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        logger.debug(f"PATCH {url} with data: {data}")
        response = self.session.patch(url, headers=headers, json=data)
        return self._handle_response(response)
    
    def delete(self, endpoint: str) -> bool:
        """Perform a DELETE request to the Graph API."""
        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        headers = self._get_headers()
        
        logger.debug(f"DELETE {url}")
        response = self.session.delete(url, headers=headers)
        
        try:
            self._handle_response(response)
            return True
        except ResourceNotFoundError:
            return False
        except Exception as e:
            raise e
