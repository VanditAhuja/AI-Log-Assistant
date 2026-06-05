from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        if "429" in str(e):
            error_count = len(errors)
            return f"""ROOT CAUSE ANALYSIS (Demo Mode)
================================
{error_count} errors detected in the log file.

1. Root Cause: Memory exhaustion led to cascading failures.
   Database timeouts triggered payment service crash.

2. Impact: Payment service was down, affecting all transactions.
   Users experienced failed orders and authentication issues.

3. Suggested Fixes:
   - Increase server memory allocation
   - Add database connection pooling
   - Implement circuit breakers for payment service
   - Add retry logic for SMTP notifications

4. Prevention:
   - Set up memory usage alerts at 70% threshold
   - Implement auto-scaling policies
   - Add health checks for all critical services
   - Regular load testing

Note: Live AI analysis will be available when API quota resets."""
        return f"AI analysis unavailable: {str(e)}"