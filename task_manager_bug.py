"""Module providing a function printing python version."""
from typing import List, Dict, Optional
import json
import datetime

class Task:
    """Class task"""
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    VALID_STATUSES = ["To Do", "In Progress", "Done"]
    
    def __init__(self, title: str, description: str, due_date: datetime.date, priority: str = "Medium", status: str = "To Do"):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {self.VALID_PRIORITIES}")
        if status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of this {self.VALID_STATUSES}")
        if due_date < datetime.date.today():
            raise ValueError("Due date cannot be in the past")
        self.title = title
        self.status = status
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.created_date = datetime.date.today()

        
    def update_status(self, new_status: str) -> None:
        """Update status"""
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.status = new_status
    
    def update_details(self, title: str = None, description: str = None, due_date: datetime.date= None, priority: str = None) -> None:
        """Update details"""
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
                raise ValueError(f"Priority must be one of {self.VALID_PRIORITIES}")
            self.priority = priority
    
    def to_dict(self) -> Dict:
        """Convert to dict for json"""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "status": self.status,
            "created_date": self.created_date.isoformat()
        }
    
    
