import json
import os
from datetime import datetime

HISTORY_FILE = "logs/history.json"

def save_to_history(filename, total_logs, summary, errors, ai_analysis):
    history = load_history()
    
    entry = {
        "id": len(history) + 1,
        "filename": filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_logs": total_logs,
        "summary": summary,
        "error_count": len(errors),
        "ai_analysis": ai_analysis
    }
    
    history.append(entry)
    
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)