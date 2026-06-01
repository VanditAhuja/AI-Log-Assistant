import re

def parse_log_line(line):
    pattern = r'(\d{4}-\d{2}-\d{2}) (\w+) (.+)'
    match = re.match(pattern, line.strip())
    if match:
        return {
            "date": match.group(1),
            "level": match.group(2),
            "message": match.group(3)
        }
    return None

def parse_log_file(filepath):
    results = []
    with open(filepath, "r") as f:
        for line in f.readlines():
            parsed = parse_log_line(line)
            if parsed:
                results.append(parsed)
    return results