"""ชั้น repository: รู้วิธีเก็บและอ่านข้อมูล แต่ไม่รู้กฎทางธุรกิจ"""

from app.repository.base import Link, LinkRepository
from app.repository.sqlite import SQLiteLinkRepository

__all__ = ["Link", "LinkRepository", "SQLiteLinkRepository"]
