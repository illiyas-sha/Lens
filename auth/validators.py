from auth.config import (
    ALLOWED_DOMAINS,
    EXCEPTION_EMAILS,
    ROLL_NUMBER_LENGTH,
    ROLL_NUMBER_PREFIX,
)


def is_valid_college_email(email: str) -> bool:
    """True if `email` is an allowed institution address or an explicit exception.
    """
    email = email.strip().lower()

    exceptions = {e.strip().lower() for e in EXCEPTION_EMAILS}
    if email in exceptions:
        return True

    if "@" not in email:
        return False
    local_part, _, domain = email.partition("@")

    allowed_domains = {d.strip().lower() for d in ALLOWED_DOMAINS}
    if domain not in allowed_domains:
        return False

    segments = local_part.split(".")
    if len(segments) < 2:
        return False

    *name_parts, roll_number = segments
    if not all(part.isalpha() for part in name_parts):
        return False

    if len(roll_number) != ROLL_NUMBER_LENGTH or not roll_number.isdigit():
        return False
    if not roll_number.startswith(ROLL_NUMBER_PREFIX):
        return False

    return True
