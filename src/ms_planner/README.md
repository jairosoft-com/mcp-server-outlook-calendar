# Microsoft Graph Planner Integration

A Python package for interacting with Microsoft Planner through the Microsoft Graph API.

## Features

- **Authentication**: Secure authentication with Microsoft Graph using MSAL
- **Plans**: Create, read, update, and delete plans
- **Tasks**: Manage tasks within plans with support for assignments and due dates
- **Buckets**: Organize tasks into buckets
- **Task Details**: Add rich details to tasks including checklists and descriptions
- **Type Safety**: Built with Pydantic for robust data validation

## Installation

1. Install the package and its dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment variables in a `.env` file in the project root:
   ```
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   ```

## Quick Start

```python
from ms_planner import PlannerService, Plan, Task, TaskPriority

# Initialize the Planner service
planner_service = PlannerService()

# Create a new plan
new_plan = {
    "title": "My Project Plan",
    "owner": "group-id-here"
}
plan = planner_service.create_plan(**new_plan)

# Create a task in the plan
task = {
    "plan_id": plan['id'],
    "title": "Complete project setup",
    "priority": TaskPriority.HIGH
}
task = planner_service.create_task(**task)

# Get all tasks in a plan
tasks = planner_service.get_tasks(plan['id'])
```

## API Reference

### PlannerService

The main class for interacting with Microsoft Planner.

#### Methods

- `get_plans(group_id: str) -> List[Dict]`: Get all plans in a group
- `get_plan(plan_id: str) -> Dict`: Get a specific plan by ID
- `create_plan(title: str, owner: str, **kwargs) -> Dict`: Create a new plan
- `get_tasks(plan_id: str) -> List[Dict]`: Get all tasks in a plan
- `get_task(task_id: str) -> Dict`: Get a specific task by ID
- `create_task(plan_id: str, title: str, **kwargs) -> Dict`: Create a new task
- `get_buckets(plan_id: str) -> List[Dict]`: Get all buckets in a plan
- `get_task_details(task_id: str) -> Dict`: Get details of a specific task
- `update_task_details(task_id: str, **updates) -> Dict`: Update task details

## Error Handling

The package defines several custom exceptions:

- `PlannerError`: Base exception for all planner-related errors
- `AuthenticationError`: Raised when authentication fails
- `APIError`: Raised when an API request fails
- `ResourceNotFoundError`: Raised when a requested resource is not found
- `ValidationError`: Raised when input validation fails

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
