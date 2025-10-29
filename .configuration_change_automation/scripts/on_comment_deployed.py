import os, requests

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["REPO"]
issue_number = os.environ["ISSUE_NUMBER"]
api = f"https://api.github.com/repos/{repo}"

r = requests.get(f"{api}/issues/{issue_number}", headers={"Authorization": f"token {token}"})
labels = [l["name"] for l in r.json()["labels"]]

# Determine transition
if "status: inactive" in labels:
    prev, new = "status: inactive", "status: in staging"
elif "status: in staging" in labels:
    prev, new = "status: in staging", "status: in production"
else:
    prev = new = None

if not new:
    print("No valid environment progression found.")
    exit(0)

# Remove "approved for next environment" and old status
for lbl in ["approved for next environment", prev]:
    requests.delete(f"{api}/issues/{issue_number}/labels/{lbl.replace(' ', '%20')}",
                    headers={"Authorization": f"token {token}"})

# Add new status
requests.post(f"{api}/issues/{issue_number}/labels",
              headers={"Authorization": f"token {token}"},
              json={"labels": [new]})

# If deployed to staging → auto-request approval for production
if new == "status: in staging":
    print("Triggering next approval for production.")
    approvers = [
        l.strip()
        for l in open(".configuration_change_automation/approvers")
        if l.strip()
    ]
    body = "Deployment to **staging** complete.\n\nRequesting approval for **production**:\n" + "\n".join([f"- {a}" for a in approvers])
    requests.post(f"{api}/issues/{issue_number}/comments",
                  headers={"Authorization": f"token {token}"},
                  json={"body": body})
    # Add awaiting approval again
    requests.post(f"{api}/issues/{issue_number}/labels",
                  headers={"Authorization": f"token {token}"},
                  json={"labels": ["awaiting approval"]})

elif new == "status: in production":
    # Close issue
    requests.post(f"{api}/issues/{issue_number}/comments",
                  headers={"Authorization": f"token {token}"},
                  json={"body": "Deployment to **production** complete. Closing issue."})
    requests.patch(f"{api}/issues/{issue_number}",
                   headers={"Authorization": f"token {token}"},
                   json={"state": "closed"})
