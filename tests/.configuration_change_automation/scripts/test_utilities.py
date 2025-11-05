import os
import pytest
import sys
from unittest.mock import patch, mock_open, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.configuration_change_automation/scripts')))
import utilities

def test_get_configuration_yml():
    config_content = 'environments:\n  staging:\n    approvers: ["a"]\n    required_approvals: 1\n  prod:\n    approvers: ["b"]\n    required_approvals: 2\n'
    with patch('builtins.open', mock_open(read_data=config_content)):
        with patch('utilities.yaml.safe_load', return_value={'environments': {'staging': {}, 'prod': {}}}):
            config = utilities.get_configuration_yml()
            assert 'environments' in config

@patch('utilities.get_github_issue')
@patch('utilities.requests.get')
def test_get_number_of_approvals(mock_requests_get, mock_get_github_issue):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    os.environ['GITHUB_TOKEN'] = 'token'
    mock_get_github_issue.return_value = {'comments_url': 'url'}
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = [{'body': '!approved staging'}, {'body': 'other'}]
    mock_requests_get.return_value = mock_resp
    count = utilities.get_number_of_approvals('staging')
    assert count == 1

@patch('utilities.get_github_issue')
def test_get_next_env_inactive(mock_get_github_issue):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    mock_get_github_issue.return_value = {'labels': [{'name': 'status: inactive'}]}
    assert utilities.get_next_env() == 'staging'

@patch('utilities.get_github_issue')
def test_get_next_env_staging(mock_get_github_issue):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    mock_get_github_issue.return_value = {'labels': [{'name': 'status: in staging'}]}
    assert utilities.get_next_env() == 'prod'

@patch('utilities.get_github_issue')
def test_get_next_env_unexpected(mock_get_github_issue):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    mock_get_github_issue.return_value = {'labels': [{'name': 'other'}]}
    with pytest.raises(ValueError):
        utilities.get_next_env()

@patch('utilities.post_github_comment')
def test_post_comment(mock_post):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    os.environ['GITHUB_TOKEN'] = 'token'
    mock_post.return_value = {'id': 1}
    assert utilities.post_comment('body') == {'id': 1}

@patch('utilities.remove_github_label')
def test_remove_label(mock_remove):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    mock_remove.return_value = {'id': 2}
    assert utilities.remove_label('label') == {'id': 2}

@patch('utilities.add_github_label')
def test_add_label(mock_add):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    mock_add.return_value = {'id': 3}
    assert utilities.add_label('label') == {'id': 3}

@patch('utilities.close_github_issue')
def test_close_issue(mock_close):
    os.environ['REPO'] = 'repo'
    os.environ['ISSUE_NUMBER'] = '1'
    mock_close.return_value = {'id': 4}
    assert utilities.close_issue() == {'id': 4}
