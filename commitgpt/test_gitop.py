import pytest
from commitgpt.gitop import Git
import os
from git import Repo

@pytest.fixture
def git_instance():
    return Git()

def setup_git():
    _ = Git()
    repo = Repo(os.getcwd())
    git = repo.git
    with open("test.txt", "w") as f:
        f.write("Test commit with signoff\n")
    git.add("test.txt")

def teardown_git():
    repo = Repo(os.getcwd())
    git = repo.git
    git.reset("HEAD~1", hard=False)
    os.remove("test.txt")

def test_diff(git_instance):
    diff = git_instance.diff()
    assert isinstance(diff, str)


def test_commit_with_signoff(git_instance):
    setup_git()
    message = "Test commit with signoff"
    git_instance.commit(message, signoff=True)
    teardown_git()

def test_commit_without_signoff(git_instance):
    setup_git()
    message = "Test commit with signoff"
    git_instance.commit(message, signoff=False)
    teardown_git()

def test_commit_with_invalid_message(git_instance):
    setup_git()
    message = ""
    with pytest.raises(Exception):
        git_instance.commit(message, signoff=True)
    repo = Repo(os.getcwd())
    git = repo.git
    git.rm("--cached","test.txt")
    os.remove("test.txt")

def test_commit_without_git_add(git_instance):
    with open("test.txt", "w") as f:
        f.write("Test commit with signoff\n")
    diff = git_instance.diff()
    assert diff == ""
    os.remove("test.txt")

def test_commit_without_git_add_2(git_instance):
    diff = git_instance.diff()
    assert diff == ""

def test_init_with_valid_repo():
    git = Git()
    assert git is not None

def test_init_with_invalid_repo(tmpdir):
    non_git_dir = tmpdir.mkdir("non_git_repo")
    os.chdir(str(non_git_dir))
    with pytest.raises(SystemExit):
        _ = Git()

if __name__ == "__main__":
    pytest.main()
