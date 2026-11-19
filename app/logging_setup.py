"""ตั้งค่า log ให้พิมพ์เป็น JSON บรรทัดละหนึ่งเหตุการณ์ ออกทาง stdout

แอปไม่เขียนไฟล์ log เอง (12-factor: log คือสายธารของเหตุการณ์)
ส่วนการเก็บ/รวม log เป็นหน้าที่ของสภาพแวดล้อมที่รันแอป เช่น Docker หรือ Kubernetes
"""

import json
import logging
import sys
from datetime import datetime, timezone

# ชื่อ attribute มาตรฐานของ LogRecord ที่เราไม่ต้องการพิมพ์ซ้ำ
_STANDARD_FIELDS = set(vars(logging.makeLogRecord({}))) | {"message", "asctime"}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        data = {
            "time": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # ค่าที่ส่งมาทาง extra={...} เช่น method, path, status
        for key, value in vars(record).items():
            if key not in _STANDARD_FIELDS:
                data[key] = value
        if record.exc_info:
            data["error"] = self.formatException(record.exc_info)
        return json.dumps(data, ensure_ascii=False, default=str)


def setup_logging(level: str) -> logging.Logger:
    """คืน logger ชื่อ "shortener" ที่พิมพ์ JSON ไป stdout"""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    logger = logging.getLogger("shortener")
    logger.handlers = [handler]  # กันไม่ให้มี handler ซ้ำถ้าเรียกหลายครั้ง
    logger.setLevel(level)
    logger.propagate = False
    return logger
