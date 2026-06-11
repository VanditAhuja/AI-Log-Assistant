from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_logs(errors):
    if not errors:
        return "No errors found in the log file."

    error_text = "\n".join([
        f"[{e['date']} {e.get('time', '')}] {e['level']}: {e['message']}"
        for e in errors
    ])

    prompt = f"""You are an expert DevOps engineer analyzing application logs.

Here are the errors found in the log file:

{error_text}

Please provide:
1. Root Cause Analysis - What is the most likely root cause?
2. Impact Assessment - What systems or users were affected?
3. Suggested Fixes - How can this be resolved?
4. Prevention - How to prevent this in future?

Keep your response clear and concise."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"


def chat_about_logs(logs, question):
    log_text = "\n".join([
        f"[{l['date']} {l.get('time','')}] {l['level']}: {l['message']}"
        for l in logs
    ])

    prompt = f"""You are an expert DevOps engineer. Here are the application logs:

{log_text}

Answer this question about the logs: {question}

Be concise and helpful."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Chat unavailable: {str(e)}"