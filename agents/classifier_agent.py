def classify_input(input_text, filename=None):
    if filename and filename.endswith(".pdf"):
        format_type = "PDF"
    elif filename and filename.endswith(".json"):
        format_type = "JSON"
    else:
        format_type = "Email"

    # Dummy intent detection (replace with LLM / regex-based logic)
    if "invoice" in input_text.lower():
        intent = "Invoice"
    elif "rfq" in input_text.lower():
        intent = "RFQ"
    elif "complaint" in input_text.lower():
        intent = "Complaint"
    else:
        intent = "General"

    return {"format": format_type, "intent": intent}
