import textwrap
from utilities import get_next_env, post_comment, get_configuration_yml


def main():
    next_env = get_next_env()

    if not next_env:
        print("No next environment detected; skipping.")
        exit(0)

    config = get_configuration_yml()

    approvers = config["environments"][next_env]["approvers"]
    required_number_of_approvals = config["environments"][next_env]["required_approvals"]

    approvers_string = "\n".join([f"- {a}" for a in approvers])

    body = f"""\
This change requires approvals from the following approvers:
{approvers_string}

Required number of approvals: **{required_number_of_approvals}**

Environment requested: **{next_env}**

To approve, please comment: `!approved {next_env}`
"""

    resp = post_comment(body)


if __name__ == "__main__":
    main()
