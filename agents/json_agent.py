import json

def validate_json(json_data):
    required_keys = ["id", "status", "amount"]
    missing = [k for k in required_keys if k not in json_data]
    anomalies = []

    for key in required_keys:
        if key in json_data and not isinstance(json_data[key], (int, str)):
            anomalies.append(f"Field {key} has type error")

    return {
        "valid": len(missing) == 0 and not anomalies,
        "missing_fields": missing,
        "anomalies": anomalies
    }
