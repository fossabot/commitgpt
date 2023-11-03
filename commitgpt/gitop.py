from git import Repo, InvalidGitRepositoryError, NoSuchPathError
import os
from rich import print


class Git:
    """
    Git class to interact with git.
    """

    def __init__(self) -> None:
        """
        Sets the git repo and git object from the current working directory.
        If the current working directory is not a git repo, then it checks
        if the parent directories are git repos and sets the git repo and git
        object from the parent directory.
        If the parent directories are not git repos, then it exits.

        Raises:
            `InvalidGitRepositoryError`: if the current working directory is
            not a git repo and the parent directories are not git repos.

            `NoSuchPathError`: if the current working directory does not exist.

        Returns:
            `None`

        Raises:
            We don't want to raise any exceptions here because hence we catch
            them and exit with a message.
        """

        try:
            self.repo = Repo(os.getcwd())
        except InvalidGitRepositoryError:
            parent_dir = os.path.dirname(os.getcwd())
            while parent_dir != "/":
                try:
                    self.repo = Repo(parent_dir)
                    break
                except InvalidGitRepositoryError:
                    parent_dir = os.path.dirname(parent_dir)
            else:
                print("[bold red]Not a git repository![/bold red] :scream:")
                exit(1)
        except NoSuchPathError:
            print("[bold red]Path not found![/bold red] :scream:")
            exit(1)
        self.git = self.repo.git

    def diff(self) -> str:
        """
        `diff` gets the diff for the last commit id after git add.

        Returns:
            `diff` (str): git diff

        Raises:
            We don't want to raise any exceptions here because hence we catch
            them and exit with a message.
        """
        try:
            last_commit_id = self.git.log("--pretty=format:%H", "-1")
        except Exception as e:
            print("[bold red]No commits found with error {e}[/bold red] :scream:", e)  # noqa: E501
            exit(1)

        try:
            diff = self.git.diff(last_commit_id, "--cached")
        except Exception as e:
            print("[bold red]No changes found with error {e}[/bold red] :scream:", e)  # noqa: E501
            exit(1)

        if diff == "":
            try:
                diff = self.git.diff(last_commit_id)
            except Exception as e:
                print("[bold red]No changes found with error {e}[/bold red] :scream:", e)  # noqa: E501
                exit(1)

        return diff

    def commit(self, message: str, signoff=True):
        """
        `Commit` the changes with the provided message.

        Args:
            `message` (str): commit message

            `signoff` (bool): add signoff to commit message. Defaults to True.

        Returns:
            `None`
        """
        if signoff:
            commit_args = "-sm"
        else:
            commit_args = "-m"

        self.git.commit(commit_args, message)
