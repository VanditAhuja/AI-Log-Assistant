from parser.parser import parse_log_file
from collections import Counter

logs = parse_log_file("logs/sample.log")

print("=== LOG SUMMARY ===")
levels = [log["level"] for log in logs]
count = Counter(levels)

for level, total in count.items():
    print(f"{level}: {total}")

print(f"\nTotal logs: {len(logs)}")

errors = [log for log in logs if log["level"] == "ERROR"]
print("\n=== ERRORS ===")
for error in errors:
    print(f"[{error['date']}] {error['message']}")