from flask import Flask, request, Response
import requests
from rules_engine import detect_attack
from logger import log_attack
from rate_limiter import check_rate

TARGET = "http://localhost:5001"

app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=["GET","POST","PUT","DELETE","PATCH"])
@app.route('/<path:path>', methods=["GET","POST","PUT","DELETE","PATCH"])
def proxy(path):

    ip = request.remote_addr

    if check_rate(ip):
        return "Too many requests", 429

    payload = request.url + str(request.args) + str(request.data)

    if detect_attack(payload):
        log_attack(request.remote_addr, payload)
        return "Blocked by WAF", 403

    # 🔹 Step 2: Forward request to backend server
    url = f"{TARGET}/{path}"
    params = request.args

    resp = requests.request(
    method=request.method,
    url=url,
    params=params,
    headers={key: value for key, value in request.headers if key != 'Host'},
    data=request.get_data(),
    cookies=request.cookies,
    allow_redirects=False
)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, headers)

if __name__ == "__main__":
    app.run(port=8080)