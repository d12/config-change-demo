import os, requests, yaml

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
    next_env = "prod"
else:
    next_env = None

if not next_env:
    print("No next environment detected; skipping.")
    exit(0)

config_path = ".configuration_change_automation/configuration_change_automation.yml"
with open(config_path) as f:
    config_content = f.read()
    config = yaml.safe_load(config_content)
    # Get the {environment}.approvers key
    approvers = config["environments"][next_env]["approvers"]
    required_number_of_approvals = config["environments"][next_env]["required_approvals"]

body = f"Requesting approval from:\n" + "\n".join([f"- {a}" for a in approvers])
body += f"\n\nRequired number of approvals: **{required_number_of_approvals}**"
body += f"\n\nEnvironment requested: **{next_env}**"

resp = requests.post(
    f"{api}/issues/{issue_number}/comments",
    headers={"Authorization": f"token {token}"},
    json={"body": body},
)

print("Response:", resp.status_code, resp.text)
