import threading
import os
from flask import Flask, jsonify
from .main import run  # your existing worker loop

app = Flask(__name__)

@app.get("/")
def health():
    return jsonify(status="ok")

# optional: expose minimal status endpoint
@app.get("/status")
def status():
    return jsonify(service="us-stocks-filter-bot", mode="web+worker", env=dict(
        MARKETDATA_MOCK=os.getenv("MARKETDATA_MOCK", "false"),
    ))

def _bg():
    # run the existing loop in a daemon thread so the web server stays responsive
    run()

def start():
    t = threading.Thread(target=_bg, daemon=True)
    t.start()
    port = int(os.getenv("PORT", "8000"))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    start()
