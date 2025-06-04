from datetime import datetime

shared_memory = {
    "inputs": [],
    "extracted": [],
    "actions": [],
    "traces": []
}

# Store input metadata: source, timestamp, classification
def store_input(source, classification):
    shared_memory["inputs"].append({
        "source": source,
        "timestamp": datetime.now().isoformat(),
        "classification": classification
    })

# Store extracted data (per agent)
def store_output(agent, data):
    shared_memory["extracted"].append({
        "agent": agent,
        "timestamp": datetime.now().isoformat(),
        "data": data
    })

# Store actions triggered
def store_action(action, reason):
    shared_memory["actions"].append({
        "action": action,
        "timestamp": datetime.now().isoformat(),
        "reason": reason
    })

# Store agent decision trace
def store_trace(agent, decision):
    shared_memory["traces"].append({
        "agent": agent,
        "timestamp": datetime.now().isoformat(),
        "decision": decision
    })

def get_memory():
    return shared_memory
