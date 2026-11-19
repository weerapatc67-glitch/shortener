"""แอปลิงก์สั้น (URL shortener) เวอร์ชัน v0 สำหรับบทที่ 1

รันด้วย:  uvicorn app:app --reload --port 8000
ข้อมูลเก็บในไฟล์ SQLite ชื่อ links.db ในโฟลเดอร์ที่รันคำสั่ง

TODO (lab บทที่ 2): ไฟล์นี้คือ solution ของบทที่ 1 ที่ทุกอย่างรวมอยู่ในไฟล์เดียว
  ย้ายโค้ดไปแยกชั้นในโฟลเดอร์ app/ (ดู app/README.md) แล้วลบไฟล์นี้ทิ้ง
  จุดที่ต้องเปลี่ยน: DB_PATH, short_url ที่ใช้ request.base_url, และ /healthz ที่ยังไม่ตรวจฐานข้อมูล
"""

import secrets
import sqlite3
import string
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel

DB_PATH = "links.db"
ALPHABET = string.ascii_letters + string.digits  # ตัวอักษรที่ใช้สร้างรหัสลิงก์
CODE_LENGTH = 6

app = FastAPI(title="ลิงก์สั้น")


# ---------- ส่วนจัดการฐานข้อมูล ----------

def get_db() -> sqlite3.Connection:
    """เปิดการเชื่อมต่อ SQLite และสร้างตารางถ้ายังไม่มี"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # ให้อ่านคอลัมน์ด้วยชื่อได้ เช่น row["url"]
    conn.execute(
        """CREATE TABLE IF NOT EXISTS links (
               code TEXT PRIMARY KEY,
               url TEXT NOT NULL,
               clicks INTEGER NOT NULL DEFAULT 0,
               created_at TEXT NOT NULL
           )"""
    )
    return conn


def new_code() -> str:
    """สุ่มรหัสลิงก์ยาว 6 ตัวอักษร"""
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


# ---------- API ----------

class LinkIn(BaseModel):
    url: str


@app.get("/healthz")
def healthz():
    """ใช้เช็คว่าแอปยังทำงานอยู่"""
    return {"status": "ok"}


@app.post("/api/links", status_code=201)
def create_link(data: LinkIn, request: Request):
    """รับ URL ยาว แล้วคืนรหัสและลิงก์สั้น"""
    # ฟีเจอร์ของ lab บทที่ 1: ยอมรับเฉพาะ URL ที่ขึ้นต้นด้วย http:// หรือ https://
    if not data.url.startswith(("http://", "https://")):
        raise HTTPException(
            status_code=422,
            detail="URL ต้องขึ้นต้นด้วย http:// หรือ https://",
        )

    code = new_code()
    created_at = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        conn.execute(
            "INSERT INTO links (code, url, created_at) VALUES (?, ?, ?)",
            (code, data.url, created_at),
        )
    return {"code": code, "short_url": f"{request.base_url}{code}"}


@app.get("/api/links/{code}")
def link_info(code: str, request: Request):
    """ดูข้อมูลของลิงก์สั้น พร้อมจำนวนคลิก"""
    with get_db() as conn:
        row = conn.execute("SELECT * FROM links WHERE code = ?", (code,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="ไม่พบลิงก์นี้")
    return {
        "code": row["code"],
        "url": row["url"],
        "short_url": f"{request.base_url}{row['code']}",
        "clicks": row["clicks"],
        "created_at": row["created_at"],
    }


# ---------- หน้าเว็บ ----------

PAGE = """<!doctype html>
<html lang="th">
<head><meta charset="utf-8"><title>ลิงก์สั้น</title></head>
<body style="font-family: sans-serif; max-width: 40rem; margin: 2rem auto;">
  <h1>ย่อลิงก์</h1>
  <form id="f">
    <input id="url" placeholder="https://example.com/ลิงก์ยาวๆ" size="40" required>
    <button>ย่อ</button>
  </form>
  <p id="out"></p>
  <script>
    document.getElementById("f").onsubmit = async (e) => {
      e.preventDefault();
      const res = await fetch("/api/links", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({url: document.getElementById("url").value}),
      });
      const data = await res.json();
      const out = document.getElementById("out");
      if (res.ok) {
        out.innerHTML = `ลิงก์สั้น: <a href="${data.short_url}">${data.short_url}</a>`;
      } else {
        out.textContent = "ผิดพลาด: " + JSON.stringify(data.detail);
      }
    };
  </script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def index():
    return PAGE


# route นี้ต้องอยู่ท้ายสุด เพราะ /{code} จับทุก path ที่มีหนึ่งช่วง
@app.get("/{code}")
def follow(code: str):
    """พาผู้ใช้ไปยัง URL จริง และนับคลิกเพิ่ม 1"""
    with get_db() as conn:
        row = conn.execute("SELECT url FROM links WHERE code = ?", (code,)).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="ไม่พบลิงก์นี้")
        conn.execute("UPDATE links SET clicks = clicks + 1 WHERE code = ?", (code,))
    return RedirectResponse(row["url"], status_code=307)
