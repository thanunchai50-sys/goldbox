from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# เก็บค่าล่าสุดในหน่วยความจำ
latest = {
    "symbol":        "XAUUSD",
    "top_high":      None,   # topBoxTop
    "top_low":       None,   # topBoxBottom
    "bot_high":      None,   # botBoxTop
    "bot_low":       None,   # botBoxBottom
    "close":         None,
    "in_top":        False,
    "in_bot":        False,
    "updated_at":    None,
    "raw":           {}
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/webhook", methods=["POST"])
def webhook():
    """รับ alert จาก TradingView"""
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "invalid json"}), 400

    # TradingView ส่งมาเป็น JSON ตาม format ที่กำหนดใน alert message
    latest["symbol"]     = data.get("symbol",   latest["symbol"])
    latest["top_high"]   = float(data.get("top_high",  0) or 0) or None
    latest["top_low"]    = float(data.get("top_low",   0) or 0) or None
    latest["bot_high"]   = float(data.get("bot_high",  0) or 0) or None
    latest["bot_low"]    = float(data.get("bot_low",   0) or 0) or None
    latest["close"]      = float(data.get("close",     0) or 0) or None
    latest["in_top"]     = bool(data.get("in_top",  False))
    latest["in_bot"]     = bool(data.get("in_bot",  False))
    latest["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest["raw"]        = data

    print(f"[{latest['updated_at']}] Webhook received: {json.dumps(data, indent=2)}")
    return jsonify({"status": "ok", "received": data}), 200

@app.route("/data", methods=["GET"])
def get_data():
    """Web UI poll ข้อมูลล่าสุด"""
    return jsonify(latest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
