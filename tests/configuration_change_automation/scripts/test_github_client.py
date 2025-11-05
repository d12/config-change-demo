import os
import pytest
import requests
from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.configuration_change_automation/scripts')))
import github_client

@patch('github_client.requests.get')
def test_get_github_issue_success(mock_get):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {'id': 1}
    mock_get.return_value = mock_resp
    with patch('github_client.gh_auth_headers', return_value={}):
        result = github_client.get_github_issue('repo', 1)
        assert result == {'id': 1}

@patch('github_client.requests.post')
def test_post_github_comment_success(mock_post):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {'id': 2}
    mock_post.return_value = mock_resp
    with patch('github_client.gh_auth_headers', return_value={}):
        result = github_client.post_github_comment('repo', 1, 'body')
        assert result == {'id': 2}

@patch('github_client.requests.delete')
def test_remove_github_label_success(mock_delete):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {'id': 3}
    mock_delete.return_value = mock_resp
    with patch('github_client.gh_auth_headers', return_value={}):
        result = github_client.remove_github_label('repo', 1, 'label')
        assert result == {'id': 3}

@patch('github_client.requests.post')
def test_add_github_label_success(mock_post):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {'id': 4}
    mock_post.return_value = mock_resp
    with patch('github_client.gh_auth_headers', return_value={}):
        result = github_client.add_github_label('repo', 1, 'label')
        assert result == {'id': 4}

@patch('github_client.requests.patch')
def test_close_github_issue_success(mock_patch):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {'id': 5}
    mock_patch.return_value = mock_resp
    with patch('github_client.gh_auth_headers', return_value={}):
        result = github_client.close_github_issue('repo', 1)
        assert result == {'id': 5}

@patch.dict(os.environ, {'GITHUB_TOKEN': 'token'})
def test_gh_auth_headers():
    headers = github_client.gh_auth_headers()
    assert headers == {'Authorization': 'token token'}
