import re

import re

patterns = [
    r"or\s+1=1",
    r"union\s+select",
    r"and\s+\d+=\d+",
    r"sleep\(",
    r"drop\s+table",
    r"insert\s+into",
    r"update\s+.*set",
    r"--",
]

def detect_attack(payload):
    payload = payload.lower()
    for pattern in patterns:
        if re.search(pattern, payload):
            return True
    return False
