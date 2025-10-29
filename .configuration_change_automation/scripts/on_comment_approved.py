import os
import requests

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["REPO"]
issue_number = os.environ["ISSUE_NUMBER"]

api_base = f"https://api.github.com/repos/{repo}"

# Remove "awaiting approval", add "approved for next environment"
requests.delete(f"{api_base}/issues/{issue_number}/labels/awaiting%20approval",
                headers={"Authorization": f"token {token}"})
requests.post(f"{api_base}/issues/{issue_number}/labels",
              headers={"Authorization": f"token {token}"}, json={"labels": ["approved for next environment"]})

# Tag deployers
with open(".configuration_change_automation/deployers") as f:
    deployers = [line.strip() for line in f if line.strip()]

comment_body = "Deployment needed. Tagging deployers:\n" + "\n".join([f"- {d}" for d in deployers])
requests.post(f"{api_base}/issues/{issue_number}/comments",
              headers={"Authorization": f"token {token}"}, json={"body": comment_body})
