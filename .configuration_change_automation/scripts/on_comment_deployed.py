import textwrap
from utilities import get_next_env, remove_label, add_label, post_comment, get_configuration_yml, close_issue

def main():
    next_env = get_next_env()
    config = get_configuration_yml()

    approvers = config["environments"][next_env]["approvers"]

    prev_label = f"status: { 'in staging' if next_env == 'prod' else 'inactive' }"
    next_label = f"status: in { next_env }"

    # Remove "approved for next environment" and old status
    for label in ["approved for next environment", prev_label]:
        remove_label(label)

    # Add new status
    add_label(next_label)

    # If deployed to staging → auto-request approval for production
    # TODO: If we ever expand this to more environments, we can DRY this up instead of just hardcoding staging -> prod.
    if next_env == "staging":
        approvers_string = "\n".join([f"- {a}" for a in approvers]) 
        body = f"Deployment to **staging** complete.\n\nRequesting approval for **production**:\n{approvers_string}"

        body = f"""\
        Deployment to **staging** has been recorded. This change now requires approvals from the following:

        {approvers_string}

        Required number of approvals: **{config["environments"]["prod"]["required_approvals"]}**

        Environment requested: **prod**

        To approve, please comment: `!approved prod`. Or, close the issue to cancel deploying to production.
        """

        post_comment(body)

        # Add awaiting approval again
        add_label("awaiting approval")

    else:
        # Close issue
        post_comment("✅ Deployment to **production** complete. Closing issue.")
        close_issue()

if __name__ == "__main__":
    main()
