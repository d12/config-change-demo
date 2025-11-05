import sys
import os
import pytest
from unittest.mock import patch, MagicMock
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../.configuration_change_automation/scripts')))
import on_issue_opened

def test_on_issue_opened_post_comment(monkeypatch):
    monkeypatch.setattr(on_issue_opened, 'get_next_env', lambda: 'staging')
    monkeypatch.setattr(on_issue_opened, 'get_configuration_yml', lambda: {
        'environments': {
            'staging': {'approvers': ['a', 'b'], 'required_approvals': 2}
        }
    })
    mock_post = MagicMock(return_value={'id': 1})
    monkeypatch.setattr(on_issue_opened, 'post_comment', mock_post)
    on_issue_opened.main()
    mock_post.assert_called_once()

def test_on_issue_opened_no_next_env(monkeypatch):
    monkeypatch.setattr(on_issue_opened, 'get_next_env', lambda: None)
    with pytest.raises(SystemExit):
        on_issue_opened.main()
