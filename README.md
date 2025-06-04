# Multi-Agent AI System

This project is a modular, multi-agent AI system that processes and classifies incoming data (Email, JSON, PDF), extracts structured information, flags anomalies, and maintains a shared memory for traceability and downstream actions.
The 'data' file contains sample data.

---

## Features

- **Classifier Agent:**  
  Detects input format (Email, JSON, PDF) and business intent (RFQ, Complaint, Invoice, Regulation, Fraud Risk) using few-shot examples and schema matching.

- **Email Agent:**  
  Extracts sender, urgency, tone, and issue/request from emails. Triggers escalation or routine actions based on content.

- **JSON Agent:**  
  Validates incoming JSON/webhook data against required schema fields, flags anomalies (missing fields, type errors), and logs alerts.

- **PDF Agent:**  
  Extracts fields from PDF invoices or policy documents, parses totals and regulatory mentions, and flags high-value invoices or compliance keywords.

- **Shared Memory Store:**  
  All agents read/write to a shared in-memory store, logging input metadata, extracted fields, actions, and agent decision traces.

- **FastAPI Web Interface:**
  - `/upload/` endpoint for uploading files (Email, JSON, PDF)
  - `/memory/` endpoint to view raw shared memory as JSON
  - `/memory/table` endpoint to view memory as HTML tables

---

## Getting Started

### Prerequisites

- Python 3.8+
- Setup virtual environment
- Install dependencies:
  ```
  pip install -r requirements.txt
  ```

### Running the Server

1. Start the FastAPI server:

   ```
   uvicorn mcp.main:app --reload
   ```

2. Open your browser to:
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive API docs
   - [http://127.0.0.1:8000/memory/](http://127.0.0.1:8000/memory/) for raw memory view
   - [http://127.0.0.1:8000/memory/table](http://127.0.0.1:8000/memory/table) for a human-friendly table view

---

## Project Structure

```
agents/
    classifier_agent.py
    email_agent.py
    json_agent.py
    pdf_agent.py
memory/
    memory_store.py
    db.py
mcp/
    main.py
```

---

## Usage

- **Upload a file:**  
  Use the `/upload/` endpoint (via Swagger UI or API client) to upload an Email, JSON, or PDF file. The system will classify, process, and store results in shared memory.

- **View memory:**  
  Access `/memory/` for a JSON dump or `/memory/table` for a table view of all processed data, actions, and traces.

---

## Authors

- Shruti Shirdhankar
