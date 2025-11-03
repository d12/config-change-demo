import os, requests, yaml
from github_client import get_github_issue, post_github_comment, remove_github_label, add_github_label, close_github_issue

def get_configuration_yml():
    config_path = ".configuration_change_automation/configuration_change_automation.yml"
    with open(config_path) as f:
        config_content = f.read()
        config = yaml.safe_load(config_content)
    return config

# Count the number of comments that begin with the approval command `!approved <env>`
def get_number_of_approvals(env):
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]

    issue = get_github_issue(repo, issue_number)
    comments_url = issue["comments_url"]

    r = requests.get(
        comments_url,
        headers={"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}
    )
    r.raise_for_status()
    comments = r.json()

    approval_command = f"!approved {env}"
    approval_count = sum(1 for comment in comments if comment["body"].startswith(approval_command))

    return approval_count

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

def remove_label(label):
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]

    return remove_github_label(repo, issue_number, label)

def add_label(label):
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]

    return add_github_label(repo, issue_number, label)


def close_issue():
    repo = os.environ["REPO"]
    issue_number = os.environ["ISSUE_NUMBER"]

    return close_github_issue(repo, issue_number)