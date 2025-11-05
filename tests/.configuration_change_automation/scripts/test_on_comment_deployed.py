import sys
import os
import pytest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.configuration_change_automation/scripts')))
import on_comment_deployed

def test_deploy_to_staging(monkeypatch):
    monkeypatch.setattr(on_comment_deployed, 'get_next_env', lambda: 'staging')
    monkeypatch.setattr(on_comment_deployed, 'get_configuration_yml', lambda: {
        'environments': {
            'staging': {'approvers': ['@a'], 'required_approvals': 1},
            'prod': {'approvers': ['@b'], 'required_approvals': 2}
        }
    })
    mock_remove = MagicMock()
    mock_add = MagicMock()
    mock_post = MagicMock()
    monkeypatch.setattr(on_comment_deployed, 'remove_label', mock_remove)
    monkeypatch.setattr(on_comment_deployed, 'add_label', mock_add)
    monkeypatch.setattr(on_comment_deployed, 'post_comment', mock_post)
    on_comment_deployed.main()
    mock_remove.assert_any_call('approved for next environment')
    mock_add.assert_any_call('awaiting approval')
    mock_post.assert_called()

def test_deploy_to_prod(monkeypatch):
    monkeypatch.setattr(on_comment_deployed, 'get_next_env', lambda: 'prod')
    monkeypatch.setattr(on_comment_deployed, 'get_configuration_yml', lambda: {
        'environments': {
            'prod': {'approvers': ['@b'], 'required_approvals': 2}
        }
    })
    mock_remove = MagicMock()
    mock_add = MagicMock()
    mock_post = MagicMock()
    mock_close = MagicMock()
    monkeypatch.setattr(on_comment_deployed, 'remove_label', mock_remove)
    monkeypatch.setattr(on_comment_deployed, 'add_label', mock_add)
    monkeypatch.setattr(on_comment_deployed, 'post_comment', mock_post)
    monkeypatch.setattr(on_comment_deployed, 'close_issue', mock_close)
    on_comment_deployed.main()
    mock_remove.assert_any_call('approved for next environment')
    mock_post.assert_called()
    mock_close.assert_called()
