import re
from datetime import datetime
from email import message_from_string
from memory.memory_store import store_output, store_input, store_action, store_trace

def extract_plain_text(email_text):
    try:
        msg = message_from_string(email_text)
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode(part.get_content_charset() or "utf-8", errors="ignore")
        else:
            return msg.get_payload(decode=True).decode(msg.get_content_charset() or "utf-8", errors="ignore")
    except Exception:
        # fallback to original text if parsing fails
        return email_text

def process_email(email_text):
    clean_text = re.sub(r'\s+', ' ', extract_plain_text(email_text)).strip()

    # Extract sender
    sender_match = re.search(r"from:\s*([^\n<]+)", email_text, re.IGNORECASE)
    sender = sender_match.group(1).strip() if sender_match else "Unknown"

    # Detect urgency
    urgency_keywords = ["asap", "urgent", "immediately", "priority"]
    urgency = "High" if any(word in email_text.lower() for word in urgency_keywords) else "Low"

    # Determine tone
    tone_map = {
        "Escalated": ["angry", "not happy", "frustrated", "disappointed", "threaten", "complain"],
        "Polite": ["please", "kindly", "would you", "appreciate"],
        "Threatening": ["legal action", "lawsuit", "report", "sue"]
    }
    tone = "Neutral"
    for t, keywords in tone_map.items():
        if any(word in email_text.lower() for word in keywords):
            tone = t
            break

    # Action based on tone or urgency
    action = {}
    if tone == "Escalated" or urgency == "High":
        action = {"type": "POST /crm/escalate", "reason": f"{tone} email with {urgency} urgency"}
    else:
        action = {"type": "LOG", "reason": "Routine email, logged and closed"}

    result = {
        "sender": sender,
        "urgency": urgency,
        "tone": tone,
        "action": action,
        "text": clean_text
    }

    # Store into shared memory system
    store_input(source="Email", classification="Complaint or Request")
    store_output(agent="Email Agent", data=result)
    store_action(action=action["type"], reason=action["reason"])
    store_trace(agent="Email Agent", decision=f"Processed email at {datetime.now().isoformat()}")

    return result
