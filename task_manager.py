"""Module providing a function printing python version."""
import datetime
import json
from typing import List, Dict, Optional

class Task:
    VALID_PRIORITIES = ["High", "Medium", "Low"]
    VALID_STATUSES = ["To Do", "In Progress", "Done"]

    def __init__(self, title: str, description: str, due_date: datetime.date, priority: str = "Medium"):
        if priority not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of {self.VALID_PRIORITIES}")
        if due_date < datetime.date.today():
            raise ValueError("Due date cannot be in the past")
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.status = "To Do"
        self.created_date = datetime.date.today()

    def update_status(self, new_status: str) -> None:
        if new_status not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of {self.VALID_STATUSES}")
        self.status = new_status

    def update_details(self, title: str = None, description: str = None,
                       due_date: datetime.date = None, priority: str = None) -> None:
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
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date.isoformat(),
            "priority": self.priority,
            "status": self.status,
            "created_date": self.created_date.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=datetime.date.fromisoformat(data["due_date"]),
            priority=data["priority"]
        )

class TaskManager:
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.task_counter = 1

    def add_task(self, title: str, description: str,
                 due_date: datetime.date, priority: str = "Medium") -> int:
        task = Task(title, description, due_date, priority)
        self.tasks[self.task_counter] = task
        self.task_counter += 1
        return self.task_counter - 1

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: int, new_status: str) -> bool:
        task = self.get_task(task_id)
        if task:
            task.update_status(new_status)
            return True
        return False

    def update_task_details(self, task_id: int, **kwargs) -> bool:
        task = self.get_task(task_id)
        if task:
            task.update_details(**kwargs)
            return True
        return False

    def delete_task(self, task_id: int) -> bool:
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def list_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> List[Dict]:
        tasks_list = []
        for task_id, task in self.tasks.items():
            if (status is None or task.status == status) and \
               (priority is None or task.priority == priority):
                tasks_list.append({
                    "id": task_id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "due_date": task.due_date,
                    "priority": task.priority
                })
        return tasks_list

    def save_to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            data = {
                "tasks": {task_id: task.to_dict() for task_id, task in self.tasks.items()},
                "task_counter": self.task_counter
            }
            json.dump(data, file, indent=4)

    def load_from_file(self, file_path: str) -> None:
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
                self.tasks = {int(task_id): Task.from_dict(task_data)
                              for task_id, task_data in data["tasks"].items()}
                self.task_counter = data["task_counter"]
        except FileNotFoundError:
            print(f"No existing file found at {file_path}. Starting with an empty task list.")

def main():
    manager = TaskManager()
    file_path = "tasks.json"
    manager.load_from_file(file_path)

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Update Task Status")
        print("4. Update Task Details")
        print("5. Delete Task")
        print("6. Save and Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date_str = input("Enter due date (YYYY-MM-DD): ")
            priority = input("Enter priority (High, Medium, Low): ")
            try:
                due_date = datetime.date.fromisoformat(due_date_str)
                task_id = manager.add_task(title, description, due_date, priority)
                print(f"Task added with ID: {task_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            tasks = manager.list_tasks()
            print("\nTasks:")
            for task in tasks:
                print(task)

        elif choice == "3":
            task_id = int(input("Enter task ID: "))
            new_status = input("Enter new status (To Do, In Progress, Done): ")
            if manager.update_task_status(task_id, new_status):
                print("Task status updated.")
            else:
                print("Task not found.")

        elif choice == "4":
            task_id = int(input("Enter task ID: "))
            updates = {}
            updates["title"] = input("Enter new title (leave blank to skip): ")
            updates["description"] = input("Enter new description (leave blank to skip): ")
            due_date_str = input("Enter new due date (YYYY-MM-DD, leave blank to skip): ")
            updates["priority"] = input("Enter new priority (High, Medium, Low, leave blank to skip): ")
            if due_date_str:
                try:
                    updates["due_date"] = datetime.date.fromisoformat(due_date_str)
                except ValueError:
                    print("Invalid date format.")
            updates = {k: v for k, v in updates.items() if v}
            if manager.update_task_details(task_id, **updates):
                print("Task details updated.")
            else:
                print("Task not found.")

        elif choice == "5":
            task_id = int(input("Enter task ID to delete: "))
            if manager.delete_task(task_id):
                print("Task deleted.")
            else:
                print("Task not found.")

        elif choice == "6":
            manager.save_to_file(file_path)
            print("Tasks saved. Exiting.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
