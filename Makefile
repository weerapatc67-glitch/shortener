# คำสั่งลัดของโปรเจกต์ ใช้ใน WSL:  make install / make run / make clean
# ค่าใน .env (ถ้ามี) จะถูกอ่านและส่งต่อเป็น env var ให้แอป

VENV ?= .venv
HOST ?= 127.0.0.1
PORT ?= 8000

-include .env
export

.PHONY: install run test lint clean

install:  ## สร้าง venv และติดตั้ง dependency ตาม requirements.txt
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

run:  ## รันแอป (log เป็น JSON ออก stdout)
	@$(VENV)/bin/uvicorn app.main:app --host $(HOST) --port $(PORT) --no-access-log

test:  ## ยังไม่มี: จะเพิ่มในบทที่ 3
	@echo "ยังไม่มีการทดสอบ: จะเพิ่ม pytest ในบทที่ 3"

lint:  ## ยังไม่มี: จะเพิ่มในบทที่ 3
	@echo "ยังไม่มีการตรวจโค้ด: จะเพิ่ม ruff ในบทที่ 3"

clean:  ## ลบ venv, cache และไฟล์ฐานข้อมูล
	rm -rf $(VENV)
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	rm -f *.db
