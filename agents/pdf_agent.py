import re
from PyPDF2 import PdfReader
from datetime import datetime
from memory.memory_store import store_output,store_input, store_action, store_trace

def parse_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    clean_text = re.sub(r'\s+', ' ', text)

    flags = []

    match = re.search(r"Total Amount[:\s]+(\d+)", clean_text, re.IGNORECASE)
    if match:
        total_amount = int(match.group(1))
        if total_amount > 10000:
            flags.append("Invoice total > 10000")

    regulations = ["GDPR", "FDA"]
    for reg in regulations:
        if reg.lower() in text.lower():
            flags.append(f"Mentions regulation: {reg}")
    
    result = {
        "status": "processed",
        "result": {
            "text": clean_text,
            "flags": flags
        }
    }

    store_input(source="PDF", classification="Invoice or Policy")
    store_output(agent="PDF Agent", data={"text": clean_text, "flags": flags})
    if flags:
        for flag in flags:
            store_action(action=flag, reason="Flagged by PDF Agent")
    store_trace(agent="PDF Agent", decision=f"Processed {file} at {datetime.now().isoformat()} with flags: {flags}")

    return result
