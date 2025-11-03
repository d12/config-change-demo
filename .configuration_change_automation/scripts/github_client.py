import os, requests

API = "https://api.github.com"

def get_github_issue(repo, issue_number):
    r = requests.get(
        f"{API}/repos/{repo}/issues/{issue_number}",
        headers=gh_auth_headers()
    )

    # Raise error if request failed
    r.raise_for_status()

    return r.json()

def post_github_comment(repo, issue_number, body):
    r = requests.post(
        f"{API}/repos/{repo}/issues/{issue_number}/comments",
        headers=gh_auth_headers(),
        json={"body": body},
    )

    # Raise error if request failed
    r.raise_for_status()

    return r.json()

def gh_auth_headers():
    return {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}