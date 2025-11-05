import os, requests, textwrap
import sys
from utilities import get_next_env, get_configuration_yml, post_comment, get_number_of_approvals, remove_label, add_label

def main():
    commenter = os.environ.get("COMMENTER", "")
    comment_body = os.environ.get("COMMENT_BODY", "")

    config = get_configuration_yml()
    next_env = get_next_env()

    approvers = config["environments"][next_env]["approvers"]
    deployers = config["environments"][next_env]["deployers"]
    required_number_of_approvals = config["environments"][next_env]["required_approvals"]

    # --- Authorization check ---
    if f"@{commenter}" not in approvers:
        msg = f"⚠️ @{commenter}, you are not authorized to approve configuration changes."
        post_comment(msg)
        sys.exit(0)

    # Ensure the approval matches the expected environment
    # Comment body should begin with "!approved <env>"
    expected_approval_command = f"!approved {next_env}"
    if not comment_body.startswith(expected_approval_command):
        msg = (f"⚠️ @{commenter}, your approval is malformed or does not match the expected environment "
                  f"'{next_env}'. Please use the command: `{expected_approval_command}` to approve.")
        post_comment(msg)
        sys.exit(0)

    # Count approvals, see if we have enough to move forward.
    current_approval_count = get_number_of_approvals(next_env)
    if current_approval_count < required_number_of_approvals:
        msg = (f"✅ @{commenter}, your approval has been recorded. "
               f"We have {current_approval_count}/{required_number_of_approvals} approvals for deployment to **{next_env}**.")
        post_comment(msg)
        sys.exit(0)

    # We have enough approvals; update labels and tag deployers.

    # Update labels
    remove_label("awaiting approval")
    add_label("approved for next environment")

    # Tag deployers
    deployers_string = "\n".join([f"- {d}" for d in deployers])

    body = f"""\
    The required number of approvals has been met. Tagging deployers to apply change in IBM Verify:
    {deployers_string}

    Changes should be applied in: **{next_env}**

    After the changes have been applied, deployers should comment: `!deployed {next_env}`
    """
    
    post_comment(body)

if __name__ == "__main__":
    main()
