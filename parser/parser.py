import re

def parse_log_line(line):
    # Handle format: 2026-06-01 08:00:01 INFO message
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    match = re.match(pattern, line.strip())
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2),
            "level": match.group(3),
            "message": match.group(4)
        }
    
    # Handle old format: 2026-06-01 INFO message
    pattern2 = r'(\d{4}-\d{2}-\d{2}) (\w+) (.+)'
    match2 = re.match(pattern2, line.strip())
    if match2:
        return {
            "date": match2.group(1),
            "time": "",
            "level": match2.group(2),
            "message": match2.group(3)
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