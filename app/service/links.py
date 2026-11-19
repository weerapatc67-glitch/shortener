"""กฎทางธุรกิจของลิงก์สั้น: ตรวจ URL, สร้างรหัส, นับคลิก"""

import secrets
import string
from datetime import datetime, timezone

from app.repository import Link, LinkRepository

ALPHABET = string.ascii_letters + string.digits  # ตัวอักษรที่ใช้สร้างรหัสลิงก์
CODE_LENGTH = 6


class InvalidUrlError(Exception):
    """URL ที่ส่งมาไม่ถูกรูปแบบ"""


class LinkNotFoundError(Exception):
    """ไม่พบลิงก์ตามรหัสที่ขอ"""


class LinkService:
    def __init__(self, repo: LinkRepository, base_url: str):
        self.repo = repo
        self.base_url = base_url

    def short_url(self, code: str) -> str:
        return f"{self.base_url}/{code}"

    def create(self, url: str) -> Link:
        """ตรวจ URL แล้วสร้างลิงก์ใหม่"""
        # TODO: ถ้า url ไม่ขึ้นต้นด้วย http:// หรือ https:// ให้
        #       raise InvalidUrlError("URL ต้องขึ้นต้นด้วย http:// หรือ https://")
        # TODO: สร้าง Link(code=self._new_code(), url=url, clicks=0,
        #       created_at=datetime.now(timezone.utc).isoformat()) แล้ว self.repo.add(link) และ return link
        raise NotImplementedError

    def get(self, code: str) -> Link:
        # TODO: link = self.repo.get(code) ถ้าเป็น None ให้ raise LinkNotFoundError("ไม่พบลิงก์นี้")
        raise NotImplementedError

    def follow(self, code: str) -> str:
        """คืน URL จริงของรหัสนี้ และนับคลิกเพิ่ม 1"""
        # TODO: ใช้ self.get(code) (จะได้ข้อผิดพลาดเดียวกันเมื่อไม่พบ) แล้วเรียก repo.increment_clicks
        raise NotImplementedError

    def check_storage(self) -> None:
        """ใช้โดย /healthz: โยน exception ถ้าที่เก็บข้อมูลใช้งานไม่ได้"""
        self.repo.ping()

    def _new_code(self) -> str:
        """สุ่มรหัสยาว 6 ตัวอักษร ถ้าบังเอิญซ้ำกับที่มีอยู่ก็สุ่มใหม่"""
        while True:
            code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
            if self.repo.get(code) is None:
                return code
