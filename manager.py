from queue import Queue
from db import Database

class Manager:
    def __init__(self):
        self.db = Database()
        self.task_queue = Queue()

    def allocate_tasks(self, project_goals):
        # Simple example of task allocation based on the project goals
        if "fix" in project_goals:
            self.task_queue.put("Fix Bug X")
            self.db.insert_task("Fix Bug X", "Pending")
        
        if "enhance" in project_goals:
            self.task_queue.put("Enhance Feature Y")
            self.db.insert_task("Enhance Feature Y", "Pending")
