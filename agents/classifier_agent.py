def classify_input(input_text, filename=None):
    # Format detection
    if filename and filename.endswith(".pdf"):
        format_type = "PDF"
    elif filename and filename.endswith(".json"):
        format_type = "JSON"
    else:
        format_type = "Email"

    # Few-shot examples for intent
    examples = {
        "Invoice": ["invoice", "bill", "payment due", "amount payable"],
        "RFQ": ["rfq", "request for quote", "quotation", "quote request"],
        "Complaint": ["complaint", "not happy", "issue", "problem", "dissatisfied"],
        "Regulation": ["regulation", "compliance", "policy", "legal", "governance"],
        "Fraud Risk": ["fraud", "scam", "risk", "suspicious", "unauthorized"]
    }

    input_lower = input_text.lower()
    intent = "General"
    for key, phrases in examples.items():
        if any(phrase in input_lower for phrase in phrases):
            intent = key
            break

    # Simple schema matching for JSON
    if format_type == "JSON":
        if any(word in input_lower for word in ["invoice", "amount"]):
            intent = "Invoice"
        elif any(word in input_lower for word in ["rfq", "quote"]):
            intent = "RFQ"

    # Routing metadata
    routing = {
        "format": format_type,
        "intent": intent,
        "route": f"/process/{format_type.lower()}/{intent.lower()}"
    }
    return routing
