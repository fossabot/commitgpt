from git import Repo
import os


class Git:
    """Git class to interact with git."""

    def __init__(self) -> None:
        """init
        Sets the git repo and git object.

        Returns:
            None
        """

        self.repo = Repo(os.getcwd())
        self.git = self.repo.git

    def last_commit_id(self) -> str:
        """last_commit_id gets the last commit id.

        Returns:
            str: last commit id
        """

        return self.git.log("--pretty=format:%H", "-1")

    def diff(self, commit_id: str, after_add=True) -> str:
        """diff gets the diff for the commit id.

        Args:
            commit_id (str): commit id
            after_add (bool, optional): changes after git add.
            Defaults to True.

        Returns:
            str: diff
        """

        if after_add:
            return self.git.diff(commit_id, "--cached")
        else:
            return self.git.diff(commit_id)

    def commit(self, message: str, **kwargs: dict) -> None:
        """Commit the changes.

        Args:
            message (str): commit message
            kwargs (dict): commit args. Defaults to {}.


        Returns:
            None
        """

        commit_args = ""
        if kwargs.get("signoff"):
            if commit_args != "":
                commit_args += " "
            commit_args += "--signoff"
        if commit_args != "":
            commit_args += " "

        commit_args += "-m"

        self.git.commit(commit_args.split(" "), message)

        return None
