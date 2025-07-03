from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from app.utils.response import success, fail
from app.schemas.common import ResponseModel
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services import report_service

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/download/{task_id}')
def download_report(task_id: str):
    file_path = os.path.join(REPORT_DIR, f'{task_id}.html')
    if not os.path.exists(file_path):
        return fail('报告不存在', code=404)
    return FileResponse(file_path, filename=f'report_{task_id}.html', media_type='text/html')

@router.get('/list')
def list_reports():
    files = [f for f in os.listdir(REPORT_DIR) if f.endswith('.html')]
    return [{
        'task_id': f.replace('.html', ''),
        'filename': f
    } for f in sorted(files, reverse=True)]

@router.get('/detail/{task_id}')
def report_detail(task_id: str):
    file_path = os.path.join(REPORT_DIR, f'{task_id}.html')
    if not os.path.exists(file_path):
        return fail('报告不存在', code=404)
    # 解析嵌入的 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    import re, json
    m = re.search(r'<script type="application/json" id="report-data">(.*?)</script>', html, re.S)
    if not m:
        return fail('报告数据缺失', code=500)
    data = json.loads(m.group(1))
    return data

@router.get('/', response_model=ResponseModel)
def get_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = report_service.get_reports(db, skip, limit)
    return success(data)

@router.get('/{report_id}', response_model=ResponseModel)
def get_report(report_id: int, db: Session = Depends(get_db)):
    data = report_service.get_report(db, report_id)
    if not data:
        return fail("报告不存在", code=404)
    return success(data) 