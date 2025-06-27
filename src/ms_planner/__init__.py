"""
Microsoft Graph Planner Integration

This package provides a high-level interface for interacting with Microsoft Planner
through the Microsoft Graph API.
"""

__version__ = "0.1.0"

from ms_planner.services.planner_service import PlannerService
from ms_planner.services.graph_client import GraphClient
from ms_planner.auth.auth_handler import AuthHandler
from ms_planner.models.planner_models import (
    Task,
    Plan,
    Bucket,
    TaskDetails,
    TaskPriority,
    Assignment,
    ChecklistItem
)

__all__ = [
    'PlannerService',
    'GraphClient',
    'AuthHandler',
    'Task',
    'Plan',
    'Bucket',
    'TaskDetails',
    'TaskPriority',
    'Assignment',
    'ChecklistItem'
]
