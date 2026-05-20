# 🥇 Gold K Box Monitor — คู่มือ Deploy บน Railway

## ไฟล์ในโปรเจคนี้
```
goldbox/
├── app.py                 ← Flask server รับ Webhook
├── requirements.txt       ← Python packages
├── Procfile               ← คำสั่งรัน server
├── templates/
│   └── index.html         ← Web UI แสดงค่า real-time
└── pine_plots_addon.pine  ← โค้ดที่ต้องเพิ่มใน TradingView
```

---

## ขั้นตอนที่ 1 — อัปโหลดขึ้น GitHub

1. ไปที่ https://github.com → สร้าง repo ใหม่ ชื่อ `goldbox`
2. อัปโหลดไฟล์ทั้งหมดใน folder นี้ขึ้นไป
   (ลาก & วาง หรือใช้ปุ่ม "Add file → Upload files")

---

## ขั้นตอนที่ 2 — Deploy บน Railway (ฟรี)

1. ไปที่ https://railway.app → Sign in ด้วย GitHub
2. กด **"New Project"** → **"Deploy from GitHub repo"**
3. เลือก repo `goldbox`
4. Railway จะ detect `Procfile` และ `requirements.txt` อัตโนมัติ
5. รอ deploy เสร็จ (~2 นาที) → กด **"Generate Domain"**
6. จะได้ URL เช่น `https://goldbox-production.up.railway.app`

---

## ขั้นตอนที่ 3 — แก้ Pine Script

เปิดไฟล์ `COMBO_fixed.pine` ใน TradingView Pine Editor
แล้วเพิ่มบรรทัดต่อไปนี้ที่ **ท้ายสุด** ของโค้ด:

```pine
plot(topBoxTop,    "Box TOP High", display=display.none)
plot(topBoxBottom, "Box TOP Low",  display=display.none)
plot(botBoxTop,    "Box BOT High", display=display.none)
plot(botBoxBottom, "Box BOT Low",  display=display.none)
```

กด **Save** และ **Add to Chart**

---

## ขั้นตอนที่ 4 — ตั้ง Alert ใน TradingView

1. กดปุ่ม **Alert** (นาฬิกา) → **Create Alert**
2. **Condition**: เลือก indicator COMBO → เลือก condition ตามชอบ
3. **Alert Message** — วาง JSON นี้:

```json
{
  "symbol":   "{{ticker}}",
  "close":    {{close}},
  "top_high": {{plot("Box TOP High")}},
  "top_low":  {{plot("Box TOP Low")}},
  "bot_high": {{plot("Box BOT High")}},
  "bot_low":  {{plot("Box BOT Low")}},
  "in_top":   false,
  "in_bot":   false
}
```

4. **Webhook URL**:
```
https://goldbox-production.up.railway.app/webhook
```
(เปลี่ยนเป็น URL จริงของคุณ)

5. **Frequency**: `Once Per Bar` หรือ `Once Per Bar Close`
6. กด **Create**

---

## ขั้นตอนที่ 5 — ใช้งาน

1. เปิด Web UI: `https://goldbox-production.up.railway.app`
2. หน้าจอจะอัปเดตทุก **3 วินาที** อัตโนมัติ
3. **แตะตัวเลข** เพื่อ copy ราคา
4. วางลงใน Pine input **Lock High Price / Lock Low Price**

---

## หมายเหตุ Railway Free Tier

- ฟรี $5/เดือน (เพียงพอสำหรับ server เล็กนี้)
- ไม่ต้องใส่บัตรเครดิต (ใช้ GitHub login)
- Server จะ sleep หลัง inactive 30 นาที → ตื่นขึ้นมาเองเมื่อมี request
