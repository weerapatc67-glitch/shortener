# โครงแอปใหม่ของบทที่ 2

โฟลเดอร์นี้คือที่ที่เราย้ายโค้ดจาก `../app.py` มาแยกเป็นชั้น (layer)
ไฟล์ส่วนใหญ่ให้มาครบแล้ว ส่วนที่ต้องเขียนเองมีคำว่า `TODO` และบรรทัด `raise NotImplementedError` กำกับไว้

```
app/
  __init__.py          ยังไม่มี: สร้าง "หลังสุด" ในขั้นที่ 8 (ดูหมายเหตุด้านล่าง)
  main.py              ประกอบทุกชั้นเข้าด้วยกัน (ให้มาครบ)
  config.py            อ่าน BASE_URL, DATABASE_PATH, LOG_LEVEL จาก env var (TODO: load_settings)
  logging_setup.py     log แบบ JSON ออก stdout (ให้มาครบ)
  api/                 ชั้น api: รับ/ตอบ HTTP (TODO: /healthz ใน links.py)
  service/             ชั้น service: กฎทางธุรกิจ (TODO: create, get, follow ใน links.py)
  repository/          ชั้น repository: interface + SQLite (TODO: get, increment_clicks, ping ใน sqlite.py)
```

ดูรายการ TODO ทั้งหมดได้ด้วย `grep -rn --include='*.py' NotImplementedError app`

หมายเหตุ: ตอนนี้ยังไม่มี `app/__init__.py` จึงทำให้ `uvicorn app:app` ยังรัน `../app.py` ตัวเดิมได้
เมื่อเขียน TODO ครบแล้ว ให้สร้าง `app/__init__.py` ลบ `app.py` เดิมทิ้ง แล้วเปลี่ยนไปรันด้วย `make run`
(หรือ `uvicorn app.main:app --no-access-log`)
