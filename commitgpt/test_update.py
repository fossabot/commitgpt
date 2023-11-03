import pytest
from unittest.mock import patch
from commitgpt.update import check_update, update, check_and_update
from commitgpt import __VERSION__ as version
@pytest.fixture
def mock_feedparser():
    with patch("feedparser.parse") as mock_feed:
        yield mock_feed

def test_check_update_with_new_version(mock_feedparser):
    curr_version = version
    new_version = str(1) + version
    mock_feedparser.return_value = {
        "entries": [
            {"title": f"{curr_version}"},
            {"title": f"{new_version}"},
        ]
    }
    assert check_update() is True

def test_check_update_with_same_version(mock_feedparser):
    mock_feedparser.return_value = {
        "entries": [
            {"title": f"{version}"},
        ]
    }
    assert check_update() is False

def test_check_update_with_no_releases(mock_feedparser):
    mock_feedparser.return_value = {
        "entries": []
    }
    assert check_update() is False

def test_update():
    with patch("os.system") as mock_os_system:
        update()
        mock_os_system.assert_called()

def test_check_and_update_with_new_version(mock_feedparser):
    curr_version = version
    new_version = str(1) + version
    mock_feedparser.return_value = {
        "entries": [
            {"title": f"{curr_version}"},
            {"title": f"{new_version}"},
        ]
    }
    with patch("typer.confirm") as mock_confirm, patch("os.system") as mock_os_system: # noqa: E501
        mock_confirm.return_value = True
        check_and_update()
        mock_os_system.assert_called()

def test_check_and_update_with_no_new_version(mock_feedparser):
    mock_feedparser.return_value = {
        "entries": [
            {"title": f"{version}"},
        ]
    }
    with patch("typer.confirm") as mock_confirm, patch("os.system") as mock_os_system:  # noqa: E501
        mock_confirm.return_value = True
        check_and_update()
        mock_os_system.assert_not_called()

def test_check_and_update_user_declines_update(mock_feedparser):
    curr_version = version
    new_version = str(1) + version
    mock_feedparser.return_value = {
        "entries": [
            {"title": f"{curr_version}"},
            {"title": f"{new_version}"},
        ]
    }

    with patch("typer.confirm") as mock_confirm, patch("os.system") as mock_os_system: # noqa: E501
        mock_confirm.return_value = False
        check_and_update()
        mock_os_system.assert_not_called()
