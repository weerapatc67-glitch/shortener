"""อ่านค่าตั้งค่า (config) จาก environment variable ตามหลัก 12-factor app

โค้ดชุดเดียวกันใช้ได้ทุก environment (dev/staging/prod) แค่เปลี่ยนค่า env var
"""

import os
from dataclasses import dataclass

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR")


@dataclass(frozen=True)
class Settings:
    base_url: str       # ส่วนหน้าของลิงก์สั้น เช่น https://sho.rt
    database_path: str  # ที่อยู่ไฟล์ SQLite
    log_level: str      # ระดับ log ขั้นต่ำที่จะพิมพ์ออกมา


def load_settings() -> Settings:
    """อ่านค่าจาก env var ถ้าไม่ได้ตั้งไว้จะใช้ค่าเริ่มต้นสำหรับเครื่องนักพัฒนา"""
    # TODO: อ่าน LOG_LEVEL ด้วย os.getenv("LOG_LEVEL", "INFO") แปลงเป็นตัวพิมพ์ใหญ่
    #       ถ้าไม่อยู่ใน LOG_LEVELS ให้ raise ValueError พร้อมข้อความไทยที่บอกค่าที่ยอมรับและค่าที่ได้
    # TODO: คืน Settings(...) โดย
    #       base_url      = BASE_URL ค่าเริ่มต้น "http://localhost:8000" และตัด / ท้ายออกด้วย .rstrip("/")
    #       database_path = DATABASE_PATH ค่าเริ่มต้น "links.db"
    raise NotImplementedError
