import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
import logging
import time

logger = logging.getLogger(__name__)

class KnowledgeDB:
    def __init__(self, dbname, user, password, host='localhost', port=5432, retries=3, delay=5):
        self.retries = retries
        self.delay = delay
        try:
            self.conn_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20, dbname=dbname, user=user, password=password, host=host, port=port)
            if self.conn_pool:
                logger.info("Connection pool created successfully.")
        except psycopg2.DatabaseError as e:
            logger.error("Database connection error: %s", e)
            raise

    def _execute_query(self, query, params=(), fetchone=False):
        attempt = 0
        while attempt < self.retries:
            try:
                conn = self.conn_pool.getconn()
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    if fetchone:
                        result = cursor.fetchone()
                    else:
                        result = cursor.fetchall()
                    conn.commit()
                    return result
            except psycopg2.DatabaseError as e:
                attempt += 1
                logger.warning("Database error on attempt %d: %s", attempt, e)
                if attempt < self.retries:
                    logger.info("Retrying query after %d seconds...", self.delay)
                    time.sleep(self.delay)
                else:
                    logger.error("Max retries reached for query: %s", query)
                    raise
            finally:
                if conn:
                    self.conn_pool.putconn(conn)

    def add_task(self, task_type, description):
        query = "INSERT INTO tasks (task_type, description) VALUES (%s, %s) RETURNING id;"
        task_id = self._execute_query(query, (task_type, description), fetchone=True)['id']
        logger.info("Task added with ID: %d", task_id)
        return task_id

    def update_task_status(self, task_id, status, result=None):
        query = "UPDATE tasks SET status = %s, result = %s WHERE id = %s;"
        self._execute_query(query, (status, result, task_id))
        logger.info("Updated status for task ID: %d", task_id)

    def get_pending_tasks(self):
        query = "SELECT * FROM tasks WHERE status = 'pending';"
        tasks = self._execute_query(query)
        logger.info("Fetched %d pending tasks", len(tasks))
        return tasks

    def close(self):
        self.conn_pool.closeall()
        logger.info("Closed all database connections.")
