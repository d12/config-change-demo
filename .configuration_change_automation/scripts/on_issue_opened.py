import os, requests

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["REPO"]
issue_number = os.environ["ISSUE_NUMBER"]
api = f"https://api.github.com/repos/{repo}"

# Get current labels to know the state
r = requests.get(f"{api}/issues/{issue_number}", headers={"Authorization": f"token {token}"})
labels = [l["name"] for l in r.json()["labels"]]

if "status: inactive" in labels:
    next_env = "staging"
elif "status: in staging" in labels:
    next_env = "production"
else:
    next_env = None

if not next_env:
    print("No next environment detected; skipping.")
    exit(0)

approvers_path = ".configuration_change_automation/approvers"
with open(approvers_path) as f:
    approvers = [l.strip() for l in f if l.strip()]

body = f"Requesting approval from:\n" + "\n".join([f"- {a}" for a in approvers])
body += f"\n\nEnvironment requested: **{next_env}**"

resp = requests.post(
    f"{api}/issues/{issue_number}/comments",
    headers={"Authorization": f"token {token}"},
    json={"body": body},
)

print("Response:", resp.status_code, resp.text)
