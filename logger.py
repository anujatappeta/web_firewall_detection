import json
import time

def log_attack(ip, payload):
    log = {
        "time": time.ctime(),
        "ip": ip,
        "payload": payload
    }

    with open("attacks.log","a") as f:
        f.write(json.dumps(log) + "\n")