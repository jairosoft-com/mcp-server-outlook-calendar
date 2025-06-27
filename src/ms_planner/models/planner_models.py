"""
Data models for Microsoft Planner entities.
"""
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator

class TaskPriority(Enum):
    """Priority levels for Planner tasks."""
    LOW = 0
    MEDIUM = 5
    HIGH = 10

class Assignment(BaseModel):
    """Represents an assignment of a task to a user."""
    user_id: str = Field(..., alias="userId")
    order_hint: Optional[str] = Field(None, alias="orderHint")

class Assignments(BaseModel):
    """Container for task assignments."""
    assignments: Dict[str, Assignment] = {}

class ChecklistItem(BaseModel):
    """Represents a checklist item in a task."""
    title: str
    is_checked: bool = Field(default=False, alias="isChecked")
    order_hint: Optional[str] = Field(None, alias="orderHint")

class Checklist(BaseModel):
    """Container for checklist items."""
    items: Dict[str, ChecklistItem] = {}

class TaskDetails(BaseModel):
    """Detailed information about a Planner task."""
    description: Optional[str] = None
    preview_type: str = Field(default="automatic", alias="previewType")
    references: Optional[Dict] = None
    checklist: Optional[Checklist] = None
    
    class Config:
        json_encoders = {
            Checklist: lambda v: v.dict(by_alias=True, exclude_unset=True) if v else {}
        }

class Task(BaseModel):
    """Represents a Planner task."""
    id: Optional[str] = None
    title: str
    plan_id: str = Field(..., alias="planId")
    bucket_id: Optional[str] = Field(None, alias="bucketId")
    due_date_time: Optional[datetime] = Field(None, alias="dueDateTime")
    start_date_time: Optional[datetime] = Field(None, alias="startDateTime")
    percent_complete: int = Field(default=0, alias="percentComplete")
    assigned_to: Optional[Assignments] = Field(None, alias="assignments")
    order_hint: Optional[str] = Field(None, alias="orderHint")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    
    class Config:
        use_enum_values = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None,
            Assignments: lambda v: v.dict(by_alias=True, exclude_unset=True) if v else {}
        }

class Plan(BaseModel):
    """Represents a Planner plan."""
    id: Optional[str] = None
    title: str
    owner: str
    created_by: Optional[Dict] = Field(None, alias="createdBy")
    created_date_time: Optional[datetime] = Field(None, alias="createdDateTime")
    container: Optional[Dict] = None
    
    @validator('container', pre=True, always=True)
    def set_container(cls, v, values):
        if v is None and 'owner' in values:
            return {"url": f"https://graph.microsoft.com/v1.0/groups/{values['owner']}"}
        return v

class Bucket(BaseModel):
    """Represents a Planner bucket."""
    id: Optional[str] = None
    name: str
    plan_id: str = Field(..., alias="planId")
    order_hint: Optional[str] = Field(None, alias="orderHint")

# Response models for API responses
class ListResponse(BaseModel):
    """Generic list response wrapper."""
    value: List[Dict]
    next_link: Optional[str] = Field(None, alias="@odata.nextLink")

class ErrorResponse(BaseModel):
    """Error response from Microsoft Graph API."""
    error: Dict[str, str]
