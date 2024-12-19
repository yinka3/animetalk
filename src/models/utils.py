import re

def parse_mentions(content):
    return re.findall(r"@(\w+)", content)