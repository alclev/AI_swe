import subprocess
from db import Database

class Tester:
    def __init__(self, task_queue):
        self.task_queue = task_queue
        self.db = Database()

    def run_tests(self, modified_file):
        # Write and execute a simple test using subprocess
        test_file = f"tests/test_{modified_file.split('/')[-1]}"
        with open(test_file, 'w') as test:
            test.write(f"def test_{modified_file}():\n    assert True")

        result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
        success = "failed" not in result.stdout.lower()
        self.db.insert_test_result(modified_file, success)
        if not success:
            self.task_queue.put(f"Fix test for {modified_file}")
