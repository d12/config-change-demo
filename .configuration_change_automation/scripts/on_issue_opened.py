import os
import requests

token = os.environ["GITHUB_TOKEN"]
repo = os.environ["REPO"]
issue_number = os.environ["ISSUE_NUMBER"]

approvers_file = ".configuration_change_automation/approvers"

with open(approvers_file) as f:
    approvers = [line.strip() for line in f if line.strip()]

body = "Requesting approval from:\n" + "\n".join([f"- {a}" for a in approvers])

url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
response = requests.post(
    url,
    headers={"Authorization": f"token {token}"},
    json={"body": body}
)

print("Response status:", response.status_code)
print("Response text:", response.text)
response.raise_for_status()

