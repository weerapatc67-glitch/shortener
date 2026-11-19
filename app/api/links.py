"""endpoint ของ REST API: /healthz และ /api/links"""

import logging

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.api.deps import get_service
from app.service import InvalidUrlError, LinkNotFoundError, LinkService

router = APIRouter()
log = logging.getLogger("shortener")


class LinkIn(BaseModel):
    url: str


@router.get("/healthz")
def healthz(service: LinkService = Depends(get_service)):
    """เช็คว่าแอปทำงานและเปิดฐานข้อมูลได้ ถ้าฐานข้อมูลเสียจะตอบ 503"""
    # TODO: ลองเรียก service.check_storage() ใน try
    #   ถ้าเกิด Exception: log.error("ตรวจฐานข้อมูลไม่ผ่าน", extra={"error": str(exc)})
    #     แล้วคืน JSONResponse(status_code=503, content={"status": "error", "database": "ใช้งานไม่ได้"})
    #   ถ้าผ่าน: คืน {"status": "ok", "database": "ok"}
    raise NotImplementedError


@router.post("/api/links", status_code=201)
def create_link(data: LinkIn, service: LinkService = Depends(get_service)):
    """รับ URL ยาว แล้วคืนรหัสและลิงก์สั้น"""
    try:
        link = service.create(data.url)
    except InvalidUrlError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    log.info("สร้างลิงก์ใหม่", extra={"code": link.code})
    return {"code": link.code, "short_url": service.short_url(link.code)}


@router.get("/api/links/{code}")
def link_info(code: str, service: LinkService = Depends(get_service)):
    """ดูข้อมูลของลิงก์สั้น พร้อมจำนวนคลิก"""
    try:
        link = service.get(code)
    except LinkNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return {
        "code": link.code,
        "url": link.url,
        "short_url": service.short_url(link.code),
        "clicks": link.clicks,
        "created_at": link.created_at,
    }
