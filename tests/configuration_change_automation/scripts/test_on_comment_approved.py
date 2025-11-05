import sys
import os
import pytest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.configuration_change_automation/scripts')))
import on_comment_approved

def test_not_authorized(monkeypatch):
    monkeypatch.setenv('COMMENTER', 'notapprover')
    monkeypatch.setenv('COMMENT_BODY', '!approved staging')
    monkeypatch.setattr(on_comment_approved, 'get_next_env', lambda: 'staging')
    monkeypatch.setattr(on_comment_approved, 'get_configuration_yml', lambda: {
        'environments': {'staging': {'approvers': ['@a'], 'deployers': ['@d'], 'required_approvals': 1}}
    })
    mock_post = MagicMock()
    monkeypatch.setattr(on_comment_approved, 'post_comment', mock_post)
    with pytest.raises(SystemExit):
        on_comment_approved.main()
    mock_post.assert_called()

def test_malformed_approval(monkeypatch):
    monkeypatch.setenv('COMMENTER', 'a')
    monkeypatch.setenv('COMMENT_BODY', 'wrong')
    monkeypatch.setattr(on_comment_approved, 'get_next_env', lambda: 'staging')
    monkeypatch.setattr(on_comment_approved, 'get_configuration_yml', lambda: {
        'environments': {'staging': {'approvers': ['@a'], 'deployers': ['@d'], 'required_approvals': 1}}
    })
    mock_post = MagicMock()
    monkeypatch.setattr(on_comment_approved, 'post_comment', mock_post)
    with pytest.raises(SystemExit):
        on_comment_approved.main()
    mock_post.assert_called()

def test_not_enough_approvals(monkeypatch):
    monkeypatch.setenv('COMMENTER', 'a')
    monkeypatch.setenv('COMMENT_BODY', '!approved staging')
    monkeypatch.setattr(on_comment_approved, 'get_next_env', lambda: 'staging')
    monkeypatch.setattr(on_comment_approved, 'get_configuration_yml', lambda: {
        'environments': {'staging': {'approvers': ['@a'], 'deployers': ['@d'], 'required_approvals': 2}}
    })
    monkeypatch.setattr(on_comment_approved, 'get_number_of_approvals', lambda env: 1)
    mock_post = MagicMock()
    monkeypatch.setattr(on_comment_approved, 'post_comment', mock_post)
    with pytest.raises(SystemExit):
        on_comment_approved.main()
    mock_post.assert_called()

def test_enough_approvals(monkeypatch):
    monkeypatch.setenv('COMMENTER', 'a')
    monkeypatch.setenv('COMMENT_BODY', '!approved staging')
    monkeypatch.setattr(on_comment_approved, 'get_next_env', lambda: 'staging')
    monkeypatch.setattr(on_comment_approved, 'get_configuration_yml', lambda: {
        'environments': {'staging': {'approvers': ['@a'], 'deployers': ['@d'], 'required_approvals': 1}}
    })
    monkeypatch.setattr(on_comment_approved, 'get_number_of_approvals', lambda env: 1)
    mock_post = MagicMock()
    monkeypatch.setattr(on_comment_approved, 'post_comment', mock_post)
    mock_remove = MagicMock()
    monkeypatch.setattr(on_comment_approved, 'remove_label', mock_remove)
    mock_add = MagicMock()
    monkeypatch.setattr(on_comment_approved, 'add_label', mock_add)
    on_comment_approved.main()
    mock_post.assert_called()
    mock_remove.assert_called()
    mock_add.assert_called()
