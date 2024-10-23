# Automated Code Management System with AI Workers

## Project Overview

This project is an **Automated Code Management System** designed to automate code-related tasks such as coding, testing, and reviewing by leveraging AI-powered workers. Tasks are distributed to workers that perform them using the OpenAI API, and the system handles task management, Git integration, and worker coordination.

### Key Features:
- **Task Queue Management**: Organizes coding, testing, and reviewing tasks in a queue.
- **AI-powered Workers**: Utilizes OpenAI GPT models to perform coding, testing, and code review tasks.
- **PostgreSQL-backed Workflow**: Stores tasks, workers, and project updates in a PostgreSQL database.
- **Git Integration**: Automatically clones repositories, commits code, and manages project updates.
- **Multithreading**: Manages concurrent workers using Python's threading to perform tasks in parallel.

---

## Table of Contents
1. Project Overview
2. System Architecture
3. Getting Started
    - Prerequisites
    - Installation
    - Database Setup
    - Environment Variables
4. Usage
5. Contributing
6. License

---

## System Architecture

1. **Database Layer**: PostgreSQL stores tasks, workers, and project updates.
2. **Task Queue**: Tasks are assigned to workers from the task queue based on availability.
3. **Workers**: Different workers for coding, testing, and reviewing tasks:
    - **Coder**: Uses OpenAI to generate code.
    - **Tester**: Runs tests on the project using `pytest`.
    - **Reviewer**: Reviews code and provides feedback.
4. **Git Integration**: Automatically clones the repository, commits changes, and manages Git updates.
5. **Concurrency**: Workers are managed using Python’s `threading` for efficient task distribution.

---

## Getting Started

### Prerequisites

- **Python 3.12+**: Install Python from [python.org](https://www.python.org/downloads/)
- **PostgreSQL**: You can install PostgreSQL using Homebrew:
    ```
    brew install postgresql
    brew services start postgresql
    ```
- **OpenAI API Key**: Sign up for an API key from OpenAI [here](https://beta.openai.com/signup).

### Installation

1. Clone the repository:
    ```
    git clone <your_repo_url>
    cd <your_project_directory>
    ```

2. Set up a virtual environment:
    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```

### Database Setup

1. Ensure PostgreSQL is running:
    ```
    brew services start postgresql
    ```

2. Create the `project_management` database:
    ```
    psql -U <your_postgres_user> -d postgres
    CREATE DATABASE project_management;
    \c project_management
    ```

3. Create the required tables:
    ```
    CREATE TABLE tasks (
        id SERIAL PRIMARY KEY,
        task_type VARCHAR(50) NOT NULL,
        description TEXT,
        status VARCHAR(50) DEFAULT 'pending',
        result TEXT,
        worker_id INT
    );

    CREATE TABLE workers (
        id SERIAL PRIMARY KEY,
        worker_type VARCHAR(50) NOT NULL,
        status VARCHAR(50) DEFAULT 'idle'
    );

    CREATE TABLE project_updates (
        id SERIAL PRIMARY KEY,
        commit_hash VARCHAR(50),
        description TEXT
    );
    ```

### Environment Variables

Create a `.env` file in the root of the project directory with the following content:


---

## Usage

1. Run the application:
    ```
    python main.py --git <git_repo_url> --num_workers <number_of_workers>
    ```

2. This will start the task manager, clone the repository, and distribute tasks to the available workers.

---

## Contributing

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/new-feature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add new feature'`).
5. Push to your branch (`git push origin feature/new-feature`).
6. Open a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
