import threading
from git_handler import GitHandler
from task_queue import TaskQueue
from workers.coder import Coder
from workers.tester import Tester
from workers.reviewer import Reviewer
from context_extractor import extract_context
from knowledge_db import KnowledgeDB
import logging
from queue import Queue

logger = logging.getLogger(__name__)

class Manager:
    def __init__(self, git_url, num_workers):
        self.git_url = git_url
        self.num_workers = num_workers
        self.git_handler = GitHandler(self.git_url)
        self.task_queue = TaskQueue()
        self.db = KnowledgeDB(dbname="project_management", user="admin", password="password")
        self.worker_threads = []
        self.lock = threading.Lock()  # To ensure thread safety
        logger.info("Manager initialized with Git URL: %s and %d workers", git_url, num_workers)

    def extract_project_info(self):
        logger.info("Cloning repository and extracting project info")
        self.git_handler.clone_repo()
        project_content = self.git_handler.get_project_content()
        context = extract_context(project_content)
        logger.debug("Extracted context: %s", context)
        return context

    def distribute_tasks(self, context):
        logger.info("Distributing tasks based on extracted context")
        task_id_code = self.db.add_task("code", "Implement feature X")
        task_id_test = self.db.add_task("test", "Test feature Y")
        task_id_review = self.db.add_task("review", "Review pull request Z")

        for _ in range(self.num_workers):
            thread = threading.Thread(target=self.worker_thread)
            thread.start()
            self.worker_threads.append(thread)

    def worker_thread(self):
        while True:
            with self.lock:
                task = self.db.get_pending_tasks()
                if not task:
                    logger.debug("No pending tasks. Exiting worker thread.")
                    break

            worker = self.db.get_worker(task['task_type'])
            if worker:
                with self.lock:
                    self.db.assign_worker_to_task(worker['id'], task['id'])
                    logger.info("Worker %d assigned to task %d", worker['id'], task['id'])

                try:
                    if task['task_type'] == "code":
                        worker_instance = Coder(worker['id'], task['id'], self.db)
                    elif task['task_type'] == "test":
                        worker_instance = Tester(worker['id'], task['id'], self.db)
                    elif task['task_type'] == "review":
                        worker_instance = Reviewer(worker['id'], task['id'], self.db)

                    worker_instance.execute(task)
                    with self.lock:
                        self.db.update_task_status(task['id'], 'completed')
                        logger.info("Task %d completed by worker %d", task['id'], worker['id'])
                except Exception as e:
                    logger.error("Error executing task %d by worker %d: %s", task['id'], worker['id'], e)

    def start(self):
        logger.info("Manager starting")
        project_info = self.extract_project_info()
        self.distribute_tasks(project_info)

        # Wait for all worker threads to complete
        for thread in self.worker_threads:
            thread.join()

        logger.info("All tasks completed. Manager shutting down.")
