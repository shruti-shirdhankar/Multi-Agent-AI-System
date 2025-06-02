from fastapi import FastAPI, UploadFile
from agents import classifier_agent, email_agent, json_agent, pdf_agent
from memory.memory_store import store_input, store_output, store_action

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # your frontend URL
    "http://127.0.0.1:3000",
    # add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload(file: UploadFile):
    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")

    classification = classifier_agent.classify_input(text, file.filename)
    store_input({"filename": file.filename, "classification": classification})

    result = {}
    if classification["format"] == "Email":
        result = email_agent.process_email(text)
    elif classification["format"] == "JSON":
        import json
        result = json_agent.validate_json(json.loads(text))
    elif classification["format"] == "PDF":
        path = f"data/{file.filename}"
        with open(path, "wb") as f:
            f.write(contents)
        result = pdf_agent.parse_pdf(path)

    store_output(result)

    # Simulate Action
    if "tone" in result and result["tone"] == "Escalated":
        action = {"type": "POST /crm/escalate", "reason": "angry email"}
        store_action(action)

    return {"status": "processed", "result": result}
