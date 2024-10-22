import queue
import logging

logger = logging.getLogger(__name__)

class Task:
    def __init__(self, task_type, description):
        self.task_type = task_type
        self.description = description
        self.status = 'pending'

    def __str__(self):
        return f"Task(type={self.task_type}, description={self.description}, status={self.status})"

class TaskQueue:
    def __init__(self):
        self.q = queue.Queue()
        logger.info("Task queue initialized")

    def add_task(self, task_type, description):
        task = Task(task_type, description)
        self.q.put(task)
        logger.info("Task added: %s", task)

    def get_task(self):
        if not self.q.empty():
            task = self.q.get()
            logger.info("Task retrieved: %s", task)
            return task
        else:
            logger.info("No tasks available")
            return None

    def is_empty(self):
        empty = self.q.empty()
        logger.debug("Task queue empty: %s", empty)
        return empty
