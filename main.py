from parser.parser import parse_log_file

logs = parse_log_file("logs/sample.log")

print("=== ALL LOGS ===")
for log in logs:
    print(log)

print("\n=== ERRORS ONLY ===")
errors = [log for log in logs if log["level"] == "ERROR"]
for error in errors:
    print(error)

print(f"\nTotal logs: {len(logs)}")
print(f"Total errors: {len(errors)}")