import os, requests

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["REPO"]
issue_number = os.environ["ISSUE_NUMBER"]
commenter = os.environ.get("COMMENTER", "").lstrip("@")
api = f"https://api.github.com/repos/{repo}"

# --- Load approvers ---
approvers_file = ".configuration_change_automation/approvers"
with open(approvers_file) as f:
    approvers = [l.strip().lstrip("@") for l in f if l.strip()]

print(f"Commenter: {commenter}")
print(f"Allowed approvers: {approvers}")

# --- Authorization check ---
if commenter not in approvers:
    msg = f"⚠️ @{commenter}, you are not authorized to approve configuration changes."
    requests.post(f"{api}/issues/{issue_number}/comments", headers=headers, json={"body": msg})
    print("User not authorized, exiting.")
    sys.exit(0)

# Get labels to decide environment
r = requests.get(f"{api}/issues/{issue_number}", headers={"Authorization": f"token {token}"})
labels = [l["name"] for l in r.json()["labels"]]

if "status: inactive" in labels:
    next_env = "staging"
elif "status: in staging" in labels:
    next_env = "production"
else:
    next_env = None

if not next_env:
    print("No valid environment state found.")
    exit(0)

# Update labels
requests.delete(f"{api}/issues/{issue_number}/labels/awaiting%20approval",
                headers={"Authorization": f"token {token}"})
requests.post(f"{api}/issues/{issue_number}/labels",
              headers={"Authorization": f"token {token}"},
              json={"labels": ["approved for next environment"]})

# Tag deployers
with open(".configuration_change_automation/deployers") as f:
    deployers = [l.strip() for l in f if l.strip()]

comment = f"Approved for deployment to **{next_env}**.\nTagging deployers:\n" + "\n".join([f"- {d}" for d in deployers])
requests.post(f"{api}/issues/{issue_number}/comments",
              headers={"Authorization": f"token {token}"}, json={"body": comment})
