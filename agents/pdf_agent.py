from pdfminer.high_level import extract_text

def parse_pdf(file_path):
    text = extract_text(file_path)
    flags = []

    if "invoice" in text.lower():
        if "10000" in text:
            flags.append("Invoice > 10,000")

    if "GDPR" in text or "FDA" in text:
        flags.append("Mentions regulation")

    return {
        "text": text[:300],
        "flags": flags
    }
