import os, requests, yaml
from github_client import get_github_issue, post_github_comment


def get_configuration_yml():
    config_path = ".configuration_change_automation/configuration_change_automation.yml"
    with open(config_path) as f:
        config_content = f.read()
        config = yaml.safe_load(config_content)
    return config

def get_next_env():
    issue = get_github_issue(os.environ["REPO"], os.environ["ISSUE_NUMBER"])
    labels = [l["name"] for l in issue["labels"]]

    if "status: inactive" in labels:
        next_env = "staging"
    elif "status: in staging" in labels:
        next_env = "prod"
    else:
        print(f"Unexpected labels found: {labels}")
        raise ValueError("No next environment detected; something is wrong.")

    return next_env

def post_comment(body):
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]
    token = os.environ["GITHUB_TOKEN"]

    return post_github_comment(repo, issue_number, body)