"""ฟังก์ชันที่ FastAPI ใช้ส่ง LinkService ให้แต่ละ endpoint (dependency)"""

from fastapi import Request

from app.service import LinkService


def get_service(request: Request) -> LinkService:
    # main.py สร้าง service ไว้ครั้งเดียวตอนเริ่มแอป แล้วเก็บใน app.state
    return request.app.state.service
