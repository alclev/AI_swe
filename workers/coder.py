import openai
import logging
from knowledge_db import KnowledgeDB

logger = logging.getLogger(__name__)

class Coder:
    def __init__(self, worker_id, task_id, db: KnowledgeDB):
        self.worker_id = worker_id
        self.task_id = task_id
        self.db = db
        logger.info("Coder initialized for worker %d on task %d", worker_id, task_id)

    def execute(self, task):
        try:
            logger.info("Generating code for task %d", task['id'])
            code = self.generate_code(task['description'])
            logger.info("Code generation complete for task %d", task['id'])
            self.commit_code(code)
            self.db.add_project_update(commit_hash="abc123", description="Code generated for feature X")
        except Exception as e:
            logger.error("Error executing coder task %d: %s", task['id'], e)

    def generate_code(self, description):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-2024-08-06",
                messages=[{"role": "user", "content": description}],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"}
                        },
                        "required": ["code"]
                    }
                }
            )
            code = response.choices[0].message.tool_calls[0].function.parsed_arguments['code']
            logger.debug("Generated code: %s", code)
            return code
        except Exception as e:
            logger.error("Error generating code: %s", e)
            raise

    def commit_code(self, code):
        try:
            with open("repo/new_feature.py", "w") as file:
                file.write(code)
            logger.info("Committed new feature code to repo")
        except Exception as e:
            logger.error("Error writing and committing code: %sContinuing from the `coder.py` logging example, here’s how we complete the rest of the `commit_code` function with logging:")
            raise e