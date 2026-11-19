"""จุดเริ่มของแอป: อ่าน config → ตั้ง log → ประกอบ repository + service + api

รันด้วย:  uvicorn app.main:app --port 8000 --no-access-log   (หรือ make run)
"""

import time

from fastapi import FastAPI, Request

from app.api import links, web
from app.config import load_settings
from app.logging_setup import setup_logging
from app.repository import SQLiteLinkRepository
from app.service import LinkService


def create_app() -> FastAPI:
    settings = load_settings()
    log = setup_logging(settings.log_level)

    repo = SQLiteLinkRepository(settings.database_path)
    app = FastAPI(title="ลิงก์สั้น")
    app.state.service = LinkService(repo, settings.base_url)

    # ลำดับสำคัญ: web มี /{code} ที่จับทุก path จึงต้องมาหลังสุด
    app.include_router(links.router)
    app.include_router(web.router)

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """เขียน log หนึ่งบรรทัดต่อหนึ่ง request"""
        start = time.perf_counter()
        response = await call_next(request)
        log.info(
            "request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": round((time.perf_counter() - start) * 1000, 1),
            },
        )
        return response

    log.info(
        "แอปพร้อมทำงาน",
        extra={"base_url": settings.base_url, "database_path": settings.database_path},
    )
    return app


app = create_app()
