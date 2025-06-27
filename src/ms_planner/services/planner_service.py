"""
Service for interacting with Microsoft Planner through Microsoft Graph API.
"""
from typing import Dict, List, Optional, Union

from ms_planner.services.graph_client import GraphClient
from ms_planner.utils.exceptions import (
    PlannerError,
    ResourceNotFoundError,
    ValidationError
)

class PlannerService:
    """Service for Microsoft Planner operations."""
    
    def __init__(self, client: Optional[GraphClient] = None):
        """Initialize the Planner service.
        
        Args:
            client: Optional GraphClient instance. If not provided, a new one will be created.
        """
        self.client = client or GraphClient()
    
    # Plan operations
    def get_plans(self, group_id: str) -> List[Dict]:
        """Get all plans in a group.
        
        Args:
            group_id: The ID of the Microsoft 365 group.
            
        Returns:
            List of plans in the group.
        """
        endpoint = f"groups/{group_id}/planner/plans"
        try:
            result = self.client.get(endpoint)
            return result.get('value', [])
        except Exception as e:
            raise PlannerError(f"Failed to get plans: {str(e)}")
    
    def get_plan(self, plan_id: str) -> Dict:
        """Get a specific plan by ID.
        
        Args:
            plan_id: The ID of the plan to retrieve.
            
        Returns:
            The plan details.
            
        Raises:
            ResourceNotFoundError: If the plan is not found.
        """
        endpoint = f"planner/plans/{plan_id}"
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise ResourceNotFoundError(f"Plan with ID {plan_id} not found: {str(e)}")
    
    def create_plan(self, title: str, owner: str, **kwargs) -> Dict:
        """Create a new plan.
        
        Args:
            title: The title of the plan.
            owner: The ID of the Microsoft 365 group that owns the plan.
            **kwargs: Additional plan properties.
            
        Returns:
            The created plan details.
        """
        if not title or not owner:
            raise ValidationError("Title and owner are required to create a plan.")
            
        plan_data = {
            "owner": owner,
            "title": title,
            **kwargs
        }
        
        try:
            return self.client.post("planner/plans", plan_data)
        except Exception as e:
            raise PlannerError(f"Failed to create plan: {str(e)}")
    
    # Task operations
    def get_tasks(self, plan_id: str) -> List[Dict]:
        """Get all tasks in a plan.
        
        Args:
            plan_id: The ID of the plan.
            
        Returns:
            List of tasks in the plan.
        """
        endpoint = f"planner/plans/{plan_id}/tasks"
        try:
            result = self.client.get(endpoint)
            return result.get('value', [])
        except Exception as e:
            raise PlannerError(f"Failed to get tasks for plan {plan_id}: {str(e)}")
    
    def get_task(self, task_id: str) -> Dict:
        """Get a specific task by ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            The task details.
            
        Raises:
            ResourceNotFoundError: If the task is not found.
        """
        endpoint = f"planner/tasks/{task_id}"
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise ResourceNotFoundError(f"Task with ID {task_id} not found: {str(e)}")
    
    def create_task(self, plan_id: str, title: str, **kwargs) -> Dict:
        """Create a new task in a plan.
        
        Args:
            plan_id: The ID of the plan to add the task to.
            title: The title of the task.
            **kwargs: Additional task properties.
            
        Returns:
            The created task details.
        """
        if not plan_id or not title:
            raise ValidationError("Plan ID and title are required to create a task.")
            
        task_data = {
            "planId": plan_id,
            "title": title,
            **kwargs
        }
        
        try:
            return self.client.post("planner/tasks", task_data)
        except Exception as e:
            raise PlannerError(f"Failed to create task: {str(e)}")
    
    # Bucket operations
    def get_buckets(self, plan_id: str) -> List[Dict]:
        """Get all buckets in a plan.
        
        Args:
            plan_id: The ID of the plan.
            
        Returns:
            List of buckets in the plan.
        """
        endpoint = f"planner/plans/{plan_id}/buckets"
        try:
            result = self.client.get(endpoint)
            return result.get('value', [])
        except Exception as e:
            raise PlannerError(f"Failed to get buckets for plan {plan_id}: {str(e)}")
    
    # Task details operations
    def get_task_details(self, task_id: str) -> Dict:
        """Get details of a specific task.
        
        Args:
            task_id: The ID of the task.
            
        Returns:
            The task details.
        """
        endpoint = f"planner/tasks/{task_id}/details"
        try:
            return self.client.get(endpoint)
        except Exception as e:
            raise PlannerError(f"Failed to get details for task {task_id}: {str(e)}")
    
    def update_task_details(self, task_id: str, **updates) -> Dict:
        """Update details of a specific task.
        
        Args:
            task_id: The ID of the task to update.
            **updates: The fields to update.
            
        Returns:
            The updated task details.
        """
        if not updates:
            raise ValidationError("No update data provided.")
            
        # Get the current details first to get the etag
        current_details = self.get_task_details(task_id)
        
        # Prepare headers with etag for concurrency control
        endpoint = f"planner/tasks/{task_id}/details"
        
        try:
            return self.client.patch(endpoint, updates)
        except Exception as e:
            raise PlannerError(f"Failed to update task {task_id}: {str(e)}")
