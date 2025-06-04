from fastapi import FastAPI, UploadFile
from agents import classifier_agent, email_agent, json_agent, pdf_agent
from memory.memory_store import get_memory
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import json

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")

    # Classify input format and intent and store metadata
    classification = classifier_agent.classify_input(text, file.filename)


    result = {}

    # Routing to correct agent
    if classification["format"] == "Email":
        result = email_agent.process_email(text)
        agent = "Email Agent"
    elif classification["format"] == "JSON":
        try:
            json_data = json.loads(text)
            result = json_agent.validate_json(json_data)
        except json.JSONDecodeError:
            result = {"error": "Invalid JSON format"}
        agent = "JSON Agent"
    elif classification["format"] == "PDF":
        path = f"data/{file.filename}"
        with open(path, "wb") as f:
            f.write(contents)
        result = pdf_agent.parse_pdf(path)
        agent = "PDF Agent"

    return {"result": result}

@app.get("/memory/")
def read_memory():
    return get_memory()

@app.get("/memory/table", response_class=HTMLResponse)
def read_memory_table():
    memory = get_memory()
    html = "<h2>Inputs</h2><table border='1'><tr><th>Source</th><th>Timestamp</th><th>Classification</th></tr>"
    for item in memory["inputs"]:
        html += f"<tr><td>{item['source']}</td><td>{item['timestamp']}</td><td>{item['classification']}</td></tr>"
    html += "</table>"

    html += "<h2>Extracted</h2><table border='1'><tr><th>Agent</th><th>Timestamp</th><th>Data</th></tr>"
    for item in memory["extracted"]:
        html += f"<tr><td>{item['agent']}</td><td>{item['timestamp']}</td><td>{item['data']}</td></tr>"
    html += "</table>"

    html += "<h2>Actions</h2><table border='1'><tr><th>Action</th><th>Timestamp</th><th>Reason</th></tr>"
    for item in memory["actions"]:
        html += f"<tr><td>{item['action']}</td><td>{item['timestamp']}</td><td>{item['reason']}</td></tr>"
    html += "</table>"

    html += "<h2>Traces</h2><table border='1'><tr><th>Agent</th><th>Timestamp</th><th>Decision</th></tr>"
    for item in memory["traces"]:
        html += f"<tr><td>{item['agent']}</td><td>{item['timestamp']}</td><td>{item['decision']}</td></tr>"
    html += "</table>"

    return html
