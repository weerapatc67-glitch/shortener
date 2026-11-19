"""interface ของ repository

ชั้น service คุยกับ LinkRepository เท่านั้น ไม่รู้ว่าข้างหลังเป็น SQLite หรืออะไร
บทที่ 4 เราจะเพิ่ม RedisLinkRepository โดยไม่ต้องแก้ service เลย
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Link:
    code: str
    url: str
    clicks: int
    created_at: str


class LinkRepository(ABC):
    @abstractmethod
    def add(self, link: Link) -> None:
        """บันทึกลิงก์ใหม่"""

    @abstractmethod
    def get(self, code: str) -> Link | None:
        """หาลิงก์จากรหัส ถ้าไม่พบคืน None"""

    @abstractmethod
    def increment_clicks(self, code: str) -> None:
        """เพิ่มจำนวนคลิกของลิงก์ขึ้น 1"""

    @abstractmethod
    def ping(self) -> None:
        """เช็คว่าที่เก็บข้อมูลใช้งานได้ ถ้าใช้ไม่ได้ให้โยน exception"""
