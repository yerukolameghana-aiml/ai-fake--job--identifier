
def validate_job_text(text):
    """Check whether the job offer text is valid."""

    if not isinstance(text, str) or not text.strip():
        return False, "Please enter a job offer message."

    if len(text) > 10000:
        return False, "Please enter fewer than 10,000 characters."

    return True, ""


def get_safety_tips():
    """Return useful job safety tips."""

    return [
        "Never pay money to secure a job without careful verification.",
        "Check the employer's official website independently.",
        "Never share passwords, OTPs, or banking credentials.",
        "Be careful when a recruiter pressures you to act quickly.",
        "Verify the job using contact details found independently.",
    ]
