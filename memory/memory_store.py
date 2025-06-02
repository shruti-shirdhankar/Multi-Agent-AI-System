# memory/memory_store.py
shared_memory = {
    "inputs": [],
    "extracted": [],
    "actions": [],
    "traces": []
}

def store_input(data): shared_memory["inputs"].append(data)
def store_output(data): shared_memory["extracted"].append(data)
def store_action(data): shared_memory["actions"].append(data)
def store_trace(data): shared_memory["traces"].append(data)

def get_memory(): return shared_memory
