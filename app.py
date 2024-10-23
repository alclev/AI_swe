import argparse
from git_repo.py import GitRepoHandler
from tokenizer.py import Tokenizer
from reviewer.py import Reviewer
from manager.py import Manager
from worker.py import WorkerThread
from tester.py import Tester

def main(git_url, thread_count):
    # Step 1: Clone repo
    repo_handler = GitRepoHandler(git_url)
    repo_handler.clone_repo()
    
    # Step 2: Gather all files and generate dictionary
    file_dict = repo_handler.get_file_structure()

    # Step 3: Tokenize files
    tokenizer = Tokenizer(file_dict)
    tokenized_dict = tokenizer.tokenize_files()

    # Step 4: Review and understand the project
    reviewer = Reviewer(tokenized_dict)
    project_goals = reviewer.understand_project()

    # Step 5: Manager allocates tasks
    manager = Manager()
    manager.allocate_tasks(project_goals)

    # Step 6: Create worker threads and start them
    threads = []
    for _ in range(thread_count):
        worker = WorkerThread(manager.task_queue)
        threads.append(worker)
        worker.start()

    # Step 7: Create a testing object to continuously test changes
    tester = Tester(manager.task_queue)
    
    # Join threads back
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI tool for managing and enhancing a git repo.")
    parser.add_argument("-g", "--git", help="Git URL", required=True)
    parser.add_argument("-t", "--threads", help="Number of worker threads", type=int, default=4)
    args = parser.parse_args()

    main(args.git, args.threads)
