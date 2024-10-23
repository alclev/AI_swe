import threading
import time
from db import Database

class WorkerThread(threading.Thread):
    def __init__(self, task_queue):
        threading.Thread.__init__(self)
        self.task_queue = task_queue
        self.db = Database()

    def run(self):
        while not self.task_queue.empty():
            task = self.task_queue.get()
            print(f"Working on task: {task}")
            # Simulate task completion
            time.sleep(2)
            self.db.insert_log(f"Completed task: {task}")
            self.task_queue.task_done()
