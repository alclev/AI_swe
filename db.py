import psycopg2

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="code_enhancer", 
            user="your_user", 
            password="your_password", 
            host="localhost"
        )
        self.create_tables()

    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    task_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logs (
                    id SERIAL PRIMARY KEY,
                    log_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tests (
                    id SERIAL PRIMARY KEY,
                    file_name TEXT,
                    test_result BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()

    def insert_task(self, task_name, status):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (task_name, status) VALUES (%s, %s)", (task_name, status))
            self.conn.commit()

    def update_task_status(self, task_id, status):
        with self.conn.cursor() as cur:
            cur.execute("UPDATE tasks SET status = %s WHERE id = %s", (status, task_id))
            self.conn.commit()

    def insert_log(self, message):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO logs (log_message) VALUES (%s)", (message,))
            self.conn.commit()

    def insert_test_result(self, file_name, result):
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO tests (file_name, test_result) VALUES (%s, %s)", (file_name, result))
            self.conn.commit()
