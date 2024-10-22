import subprocess
import logging
from knowledge_db import KnowledgeDB

logger = logging.getLogger(__name__)

class Tester:
    def __init__(self, worker_id, task_id, db: KnowledgeDB):
        self.worker_id = worker_id
        self.task_id = task_id
        self.db = db
        logger.info("Tester initialized for worker %d on task %d", worker_id, task_id)

    def execute(self, task):
        logger.info("Running tests for task %d", task['id'])
        try:
            result = self.run_tests()
            logger.info("Test execution complete for task %d with result: %s", task['id'], result)
            self.db.update_task_status(task['id'], 'completed', result)
        except Exception as e:
            logger.error("Error running tests for task %d: %s", task['id'], e)

    def run_tests(self):
        try:
            result = subprocess.run(['pytest'], capture_output=True, text=True)
            logger.debug("Test result: %s", result.stdout)
            return result.stdout
        except Exception as e:
            logger.error("Error executing tests: %s", e)
            raise
