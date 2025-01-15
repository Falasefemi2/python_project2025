"""Module providing a class for managing tasks with various attributes."""
import datetime
import json
from typing import List, Dict, Optional

class Task:
    """Class representing a task with attributes like title, description,
    due date, priority, and status."""
    
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    VALID_STATUES = ["To Do", "In Progress", "Done"]
    
    def __init__(self, title: str, description: str, due_date: datetime.date,
                 priority: str = "Medium", status: str = "To Do"):
        """Initialize a new task with the given attributes.
        
        Args:
            title (str): The title of the task.
            description (str): A brief description of the task.
            due_date (datetime.date): The due date for the task.
            priority (str): The priority level of the task (default is "Medium").
            status (str): The current status of the task (default is "To Do").
        
        Raises:
            ValueError: If the priority, status, or due date are invalid.
        """
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be any of these {self.VALID_PRIORITIES}")
        if status not in self.VALID_STATUES:
            raise ValueError(f"Status must be any of these {self.VALID_STATUES}")
        if due_date < datetime.date.today():
            raise ValueError("Due date cannot be in the past")
        
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = status
        
    def update_status(self, new_status: str):
        """Update the status of the task.
        
        Args:
            new_status (str): The new status to set for the task.
        
        Raises:
            ValueError: If the new status is invalid.
        """
        if new_status not in self.VALID_STATUES:
            raise ValueError(f"Status must be one of these: {self.VALID_STATUES}")
        self.status = new_status
    
    def update_details(self, title: str = None, description: str = None,
                       due_date: datetime.date = None, priority: str = None,
                       status: str = None) -> None:
        """Update the details of the task.
        
        Args:
            title (str, optional): New title for the task.
            description (str, optional): New description for the task.
            due_date (datetime.date, optional): New due date for the task.
            priority (str, optional): New priority for the task.
            status (str, optional): New status for the task.
        
        Raises:
            ValueError: If any of the provided values are invalid.
        """
        if title:
            self.title = title
        if description:
            self.description = description
        if due_date:
            if due_date < datetime.date.today():
                raise ValueError("Due date cannot be in the past")
            self.due_date = due_date
        if priority:
            if priority not in self.VALID_PRIORITIES:
                raise ValueError(f"Priority must be among these {self.VALID_PRIORITIES}")
            self.priority = priority
        if status:
            if status not in self.VALID_STATUES:
                raise ValueError(f"Status must be among these {self.VALID_STATUES}")
            self.status = status    
    
    def to_dict(self) -> Dict:
        """Convert the task instance to a dictionary representation.
        
        Returns:
            Dict: A dictionary containing the task's attributes.
        """
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Task':
        """Create a Task instance from a dictionary representation.
        
        This method is a class method, which means it is called on the class
        itself rather than on an instance of the class. It allows you to
        create a new Task object using data stored in a dictionary format.
        
        Args:
            data (Dict): A dictionary containing the task's attributes.
        
        Returns:
            Task: A new instance of the Task class.
        """
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=datetime.date.fromisoformat(data["due_date"]),
            priority=data["priority"],
            status=data["status"]
        )


class TaskManager:
    """Class representing the task manager  such as add task, get task, update task"""
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.task_counter = 1
        
    def add_task(self, title: str, description: str, due_date: datetime.date, priority: str= "Medium", status: str= "To Do") -> int:
        """Function to add task"""
        task = Task(title, description, due_date, priority, status)
        self.tasks[self.task_counter] = task
        self.task_counter += 1
        return self.task_counter - 1
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get Task"""
        return self.tasks.get(task_id)
    
    def update_task_status(self, task_id: int, new_status: str) -> bool:
        """Update task status"""
        task = self.get_task(task_id)
        if task:
            task.update_status(new_status)
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def update_task_details(self, task_id: int, **kwargs) -> bool:
        """Update task details"""
        task = self.get_task(task_id)
        if task:
            task.update_details(**kwargs)
            return True
        return False
    
    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> List[Dict]:
        """List all tasks"""
        task_list = []
        for task_id, task in self.tasks.items():
            if (status is None or task.status == status) and \
                (priority is None or task.priority == priority):
                    task_list.append({
                        "id": task_id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                        "due_date": task.due_date,
                        "priority": task.priority                        
                    })
        return task_list
    
    def save_to_file(self, file_path: str) -> None:
        """Save file"""
        with open(file_path, "w", encoding="utf-8") as file:
            data = {
                "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()},
                "task_counter": self.task_counter
            }
            json.dump(data, file, indent=4)
    
    def load_to_file(self, file_path: str) -> None:
        """Load data"""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = {int(task_id): Task.from_dict(task_data)
                              for task_id, task_data in data["tasks"].items()}
                self.task_counter = data['task_counter']
        except FileNotFoundError:
            print(f"No existing file found at {file_path}. Starting with an empty task list.")

            