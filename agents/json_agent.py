import json
from datetime import datetime
from memory.memory_store import store_output, store_input, store_action, store_trace

def validate_json(json_data):
    required_keys = ["id", "status", "amount"]
    missing = [k for k in required_keys if k not in json_data]
    anomalies = []

    for key in required_keys:
        if key in json_data and not isinstance(json_data[key], (int, str)):
            anomalies.append(f"Field {key} has type error")

    flags = []
    if missing:
        flags.append(f"Missing fields: {', '.join(missing)}")
    if anomalies:
        flags.extend(anomalies)

    result = {
        "valid": len(missing) == 0 and not anomalies,
        "missing_fields": missing,
        "anomalies": anomalies,
        "input": json_data  
    }

    # Store in memory
    store_input(source="JSON", classification="Data Validation")
    store_output(agent="JSON Agent", data=result)

    if flags:
        for flag in flags:
            store_action(action=flag, reason="Flagged by JSON Agent")

    store_trace(agent="JSON Agent", decision=f"Processed JSON at {datetime.now().isoformat()} with flags: {flags}")

    return result
