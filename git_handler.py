import git
import logging
import time

logger = logging.getLogger(__name__)

class GitHandler:
    def __init__(self, git_url, retries=3, delay=5):
        self.git_url = git_url
        self.repo = None
        self.retries = retries
        self.delay = delay
        logger.info("Initialized GitHandler with Git URL: %s", git_url)

    def clone_repo(self):
        logger.info("Cloning repository from %s", self.git_url)
        attempt = 0
        while attempt < self.retries:
            try:
                self.repo = git.Repo.clone_from(self.git_url, 'repo')
                logger.info("Repository cloned successfully")
                return
            except git.exc.GitError as e:
                attempt += 1
                logger.warning("Git error during cloning (attempt %d): %s", attempt, e)
                if attempt < self.retries:
                    logger.info("Retrying after %d seconds...", self.delay)
                    time.sleep(self.delay)
                else:
                    logger.error("Max retries reached. Cloning failed.")
                    raise
            except Exception as e:
                logger.error("Unexpected error cloning repository: %s", e)
                raise

    def get_project_content(self):
        if not self.repo:
            logger.error("Repository not cloned, cannot fetch content.")
            raise Exception("Repository not cloned.")
        try:
            with open("repo/README.md", "r") as readme:
                content = readme.read()
                logger.info("Extracted README.md content")
                return content
        except FileNotFoundError:
            logger.error("README.md not found in repository.")
            raise
        except Exception as e:
            logger.error("Error reading README.md: %s", e)
            raise

    def commit_changes(self, message="Auto commit by worker"):
        if not self.repo:
            logger.error("Repository not initialized, cannot commit.")
            raise Exception("Repository not initialized.")
        try:
            self.repo.git.add(A=True)
            self.repo.git.commit('-m', message)
            logger.info("Changes committed to repository with message: %s", message)
        except git.exc.GitError as e:
            logger.error("Git error during commit: %s", e)
            raise
        except Exception as e:
            logger.error("Unknown error during commit: %s", e)
            raise
