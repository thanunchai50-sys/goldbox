[app.py](https://github.com/user-attachments/files/28055204/app.py)
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

latest = {
    "symbol":     "XAUUSD",
    "top_high":   None,
    "top_low":    None,
    "bot_high":   None,
    "bot_low":    None,
    "close":      None,
    "in_top":     False,
    "in_bot":     False,
    "updated_at": None,
}

HTML = """<!DOCTYPE html>
<html lang="th">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gold K Box Monitor</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0d0d0d;color:#eee;font-family:'Segoe UI',sans-serif;min-height:100vh;display:flex;flex-direction:column;align-items:center;padding:24px 16px}
h1{font-size:1.3rem;letter-spacing:2px;color:#ffd700;margin-bottom:6px}
#symbol{font-size:.85rem;color:#aaa;margin-bottom:20px}
#dot{display:inline-block;width:10px;height:10px;border-radius:50%;background:#555;margin-right:6px;vertical-align:middle;transition:background .3s}
#dot.live{background:#00e676;box-shadow:0 0 8px #00e676}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:16px;width:100%;max-width:600px;margin-bottom:20px}
.card{border-radius:12px;padding:20px 16px;border:2px solid;position:relative}
.card.top{border-color:#ffd700;background:#1a1700}
.card.bot{border-color:#00b4ff;background:#001a22}
.card-title{font-size:.75rem;font-weight:700;letter-spacing:2px;margin-bottom:14px}
.card.top .card-title{color:#ffd700}
.card.bot .card-title{color:#00b4ff}
.price-row{display:flex;justify-content:space-between;align-items:center;margin-bottom:10px}
.price-label{font-size:.7rem;color:#888;text-transform:uppercase;letter-spacing:1px}
.price-value{font-size:1.25rem;font-weight:700;cursor:pointer;transition:opacity .15s}
.price-value:hover{opacity:.7}
.card.top .price-value{color:#ffd700}
.card.bot .price-value{color:#00b4ff}
.copy-hint{font-size:.65rem;color:#555;text-align:right;margin-top:4px}
.badge{position:absolute;top:12px;right:12px;font-size:.65rem;padding:3px 8px;border-radius:20px;font-weight:700}
.badge.on{background:#00e676;color:#000;animation:pulse 1.2s infinite}
.badge.off{background:#333;color:#666}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
.close-row{width:100%;max-width:600px;background:#1a1a1a;border-radius:10px;padding:14px 20px;display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.close-row .lbl{font-size:.8rem;color:#888}
.close-row .val{font-size:1.4rem;font-weight:700}
#updated{font-size:.72rem;color:#555;margin-bottom:20px}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%) translateY(80px);background:#00e676;color:#000;font-weight:700;font-size:.85rem;padding:10px 24px;border-radius:30px;transition:transform .3s;pointer-events:none}
.toast.show{transform:translateX(-50%) translateY(0)}
.webhook-box{width:100%;max-width:600px;background:#111;border:1px solid #222;border-radius:10px;padding:16px 20px}
.webhook-box h2{font-size:.8rem;color:#ffd700;margin-bottom:8px}
.webhook-box code{display:block;background:#1e1e1e;color:#ffd700;padding:10px;border-radius:6px;font-size:.78rem;word-break:break-all}
</style>
</head>
<body>
<h1>⬛ Gold K Box Monitor</h1>
<div id="symbol"><span id="dot"></span><span id="sym">รอรับข้อมูลจาก TradingView...</span></div>

<div class="close-row">
  <span class="lbl">CLOSE</span>
  <span class="val" id="close">—</span>
</div>

<div class="cards">
  <div class="card top">
    <div class="card-title">▲ TOP BOX</div>
    <span class="badge off" id="badge-top">IN BOX</span>
    <div class="price-row"><span class="price-label">High</span><span class="price-value" id="top-high" onclick="cp('top-high')">—</span></div>
    <div class="price-row"><span class="price-label">Low</span><span class="price-value" id="top-low" onclick="cp('top-low')">—</span></div>
    <div class="copy-hint">👆 แตะเพื่อ copy</div>
  </div>
  <div class="card bot">
    <div class="card-title">▼ BOT BOX</div>
    <span class="badge off" id="badge-bot">IN BOX</span>
    <div class="price-row"><span class="price-label">High</span><span class="price-value" id="bot-high" onclick="cp('bot-high')">—</span></div>
    <div class="price-row"><span class="price-label">Low</span><span class="price-value" id="bot-low" onclick="cp('bot-low')">—</span></div>
    <div class="copy-hint">👆 แตะเพื่อ copy</div>
  </div>
</div>

<div id="updated">อัปเดตล่าสุด: —</div>

<div class="webhook-box">
  <h2>Webhook URL สำหรับ TradingView</h2>
  <code id="wh-url"></code>
</div>

<div class="toast" id="toast"></div>

<script>
document.getElementById('wh-url').textContent = window.location.origin + '/webhook';

async function poll(){
  try{
    const d = await (await fetch('/data')).json();
    if(d.updated_at){
      document.getElementById('dot').className='live';
      document.getElementById('sym').textContent=(d.symbol||'XAUUSD')+' · live';
    }
    const f=v=>v!=null?Number(v).toFixed(2):'—';
    document.getElementById('close').textContent=f(d.close);
    document.getElementById('top-high').textContent=f(d.top_high);
    document.getElementById('top-low').textContent=f(d.top_low);
    document.getElementById('bot-high').textContent=f(d.bot_high);
    document.getElementById('bot-low').textContent=f(d.bot_low);
    document.getElementById('updated').textContent='อัปเดตล่าสุด: '+(d.updated_at||'—');
    document.getElementById('badge-top').className='badge '+(d.in_top?'on':'off');
    document.getElementById('badge-bot').className='badge '+(d.in_bot?'on':'off');
  }catch(e){}
}

async function cp(id){
  const v=document.getElementById(id).textContent;
  if(v==='—')return;
  try{await navigator.clipboard.writeText(v)}catch(e){
    const t=document.createElement('textarea');t.value=v;document.body.appendChild(t);t.select();document.execCommand('copy');document.body.removeChild(t);
  }
  const t=document.getElementById('toast');
  t.textContent='✅ Copy '+v+' แล้ว!';t.classList.add('show');
  setTimeout(()=>t.classList.remove('show'),2000);
}

poll();setInterval(poll,3000);
</script>
</body>
</html>"""

@app.route("/", methods=["GET"])
def index():
    return HTML

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "invalid json"}), 400
    latest["symbol"]     = data.get("symbol",  latest["symbol"])
    latest["top_high"]   = float(data.get("top_high",  0) or 0) or None
    latest["top_low"]    = float(data.get("top_low",   0) or 0) or None
    latest["bot_high"]   = float(data.get("bot_high",  0) or 0) or None
    latest["bot_low"]    = float(data.get("bot_low",   0) or 0) or None
    latest["close"]      = float(data.get("close",     0) or 0) or None
    latest["in_top"]     = bool(data.get("in_top",  False))
    latest["in_bot"]     = bool(data.get("in_bot",  False))
    latest["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{latest['updated_at']}] {json.dumps(data)}")
    return jsonify({"status": "ok"}), 200

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(latest)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
