"""ชั้น service: กฎทางธุรกิจของแอป ไม่รู้เรื่อง HTTP และไม่รู้ว่าข้อมูลเก็บที่ไหน"""

from app.service.links import InvalidUrlError, LinkNotFoundError, LinkService

__all__ = ["InvalidUrlError", "LinkNotFoundError", "LinkService"]
