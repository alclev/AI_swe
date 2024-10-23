import git
import os

class GitRepoHandler:
    def __init__(self, git_url, local_repo_path="/tmp/cloned_repo"):
        self.git_url = git_url
        self.local_repo_path = local_repo_path

    def clone_repo(self):
        if os.path.exists(self.local_repo_path):
            self.repo = git.Repo(self.local_repo_path)
        else:
            self.repo = git.Repo.clone_from(self.git_url, self.local_repo_path)

    def get_file_structure(self):
        file_dict = {}
        for root, dirs, files in os.walk(self.local_repo_path):
            for file in files:
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    file_dict[os.path.join(root, file)] = f.read()
        return file_dict
