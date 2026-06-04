from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from parser.parser import parse_log_file
from ai.ai_engine import analyze_logs
from collections import Counter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "AI Log Assistant is running!"}

@app.post("/upload")
async def upload_log(file: UploadFile = File(...)):
    filepath = f"logs/{file.filename}"
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    logs = parse_log_file(filepath)
    levels = [log["level"] for log in logs]
    count = Counter(levels)
    errors = [log for log in logs if log["level"] in ["ERROR", "CRITICAL"]]

    ai_analysis = analyze_logs(errors)

    return {
        "filename": file.filename,
        "total_logs": len(logs),
        "summary": count,
        "errors": errors,
        "ai_analysis": ai_analysis
    }