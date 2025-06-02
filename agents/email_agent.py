def process_email(email_text):
    sender = "John Doe"  # use regex or NLP to extract
    urgency = "High" if "asap" in email_text.lower() else "Low"

    if "angry" in email_text.lower() or "not happy" in email_text.lower():
        tone = "Escalated"
    else:
        tone = "Neutral"

    return {
        "sender": sender,
        "urgency": urgency,
        "tone": tone,
        "text": email_text
    }
