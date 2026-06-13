from fastapi.responses import StreamingResponse
from backend.pdf_generator import generate_pdf_report
from backend.database import save_to_history, load_history
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/app")
def serve_frontend():
    return FileResponse("frontend/index.html")  

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
    save_to_history(file.filename, len(logs), dict(count), errors, ai_analysis)
    return {
       
        "filename": file.filename,
        "total_logs": len(logs),
        "summary": count,
        "errors": errors,
        "ai_analysis": ai_analysis
    }
from pydantic import BaseModel

class ChatRequest(BaseModel):
    question: str
    filename: str

@app.post("/chat")
async def chat_with_logs(request: ChatRequest):
    filepath = f"logs/{request.filename}"
    
    if not os.path.exists(filepath):
        return {"answer": "Log file not found. Please upload a file first."}
    
    logs = parse_log_file(filepath)
    from ai.ai_engine import chat_about_logs
    answer = chat_about_logs(logs, request.question)
    return {"answer": answer}
@app.get("/history")
def get_history():
    return load_history()
@app.get("/export/{filename}")
def export_pdf(filename: str):
    filepath = f"logs/{filename}"
    if not os.path.exists(filepath):
        return {"error": "File not found"}

    logs = parse_log_file(filepath)
    from collections import Counter
    levels = [log["level"] for log in logs]
    count = Counter(levels)
    errors = [log for log in logs if log["level"] in ["ERROR", "CRITICAL"]]
    ai_analysis = analyze_logs(errors)

    pdf_buffer = generate_pdf_report(filename, len(logs), dict(count), errors, ai_analysis)

    report_name = filename.replace('.log', '').replace('.txt', '')
    headers = {"Content-Disposition": f'attachment; filename="{report_name}_report.pdf"'}
    return StreamingResponse(pdf_buffer, media_type="application/pdf", headers=headers)