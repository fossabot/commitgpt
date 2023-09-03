import pytest
from .gitop import Git


@pytest.fixture
def git_instance():
    return Git()


def test_last_commit_id(git_instance):
    commit_id = git_instance.last_commit_id()
    assert isinstance(commit_id, str)
    assert len(commit_id) == 40  # Assuming commit IDs are 40 characters long


def test_diff(git_instance):
    commit_id = git_instance.last_commit_id()
    diff = git_instance.diff(commit_id)
    assert isinstance(diff, str)


# Run tests using pytest
if __name__ == "__main__":
    pytest.main()
