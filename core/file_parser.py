import re

def parse_file_command(text: str):
    """
    Extract filename and content from user text.
    Returns (filename, content) or (None, None)
    """

    stripped = text.strip()

    # Pattern 1: create file xyz with content abc
    match = re.search(
        r"create(?:\s+a)?\s+file\s+([\w\-.]+)\s+with content\s+(.+)",
        stripped,
        re.IGNORECASE
    )
    if match:
        filename = match.group(1)
        content = match.group(2).strip().strip("\"'")
        return filename, content

    # Pattern 2: create file name xyz
    match = re.search(
        r"create(?:\s+a)?\s+file(?:\s+name)?\s+([\w\-]+\.\w+)",
        stripped,
        re.IGNORECASE
    )
    if match:
        filename = match.group(1)
        return filename, ""

    # Pattern 3: write xyz
    match = re.search(r"write\s+(.+)", stripped, re.IGNORECASE)
    if match:
        content = match.group(1).strip().strip("\"'")
        return None, content

    return None, None
