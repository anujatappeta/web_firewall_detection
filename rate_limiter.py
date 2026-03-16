request_counts = {}

def check_rate(ip):
    request_counts[ip] = request_counts.get(ip, 0) + 1

    if request_counts[ip] > 100:
        return True

    return False