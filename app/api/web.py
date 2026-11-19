"""หน้าเว็บฟอร์มย่อลิงก์ และ route /{code} ที่พาไปยัง URL จริง"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.api.deps import get_service
from app.service import LinkNotFoundError, LinkService

router = APIRouter()

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


@router.get("/", response_class=HTMLResponse)
def index():
    return PAGE


# route นี้ต้องถูก include เป็นอันสุดท้าย เพราะ /{code} จับทุก path ที่มีหนึ่งช่วง
@router.get("/{code}")
def follow(code: str, service: LinkService = Depends(get_service)):
    """พาผู้ใช้ไปยัง URL จริง และนับคลิกเพิ่ม 1"""
    try:
        url = service.follow(code)
    except LinkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return RedirectResponse(url, status_code=307)
