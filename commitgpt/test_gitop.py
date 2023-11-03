import pytest
from commitgpt.gitop import Git


@pytest.fixture
def git_instance():
    return Git()


def test_diff(git_instance):
    diff = git_instance.diff()
    assert isinstance(diff, str)


# Run tests using pytest
if __name__ == "__main__":
    pytest.main()
