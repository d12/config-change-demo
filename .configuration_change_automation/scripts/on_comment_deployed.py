import os
import requests

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["REPO"]
issue_number = os.environ["ISSUE_NUMBER"]

api_base = f"https://api.github.com/repos/{repo}"

# Get current labels
labels_resp = requests.get(f"{api_base}/issues/{issue_number}", headers={"Authorization": f"token {token}"})
labels = [lbl["name"] for lbl in labels_resp.json()["labels"]]

# Logic for state progression
if "status: inactive" in labels:
    old, new = "status: inactive", "status: in staging"
elif "status: in staging" in labels:
    old, new = "status: in staging", "status: in production"
else:
    old, new = None, None

if new:
    if old:
        requests.delete(f"{api_base}/issues/{issue_number}/labels/{old.replace(' ', '%20')}",
                        headers={"Authorization": f"token {token}"})
    requests.post(f"{api_base}/issues/{issue_number}/labels",
                  headers={"Authorization": f"token {token}"}, json={"labels": [new]})

    # If now in production, close issue
    if new == "status: in production":
        requests.patch(f"{api_base}/issues/{issue_number}",
                       headers={"Authorization": f"token {token}"},
                       json={"state": "closed"})
