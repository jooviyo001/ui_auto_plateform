from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')

router = APIRouter()

@router.get('/download/{task_id}')
def download_report(task_id: str):
    file_path = os.path.join(REPORT_DIR, f'{task_id}.html')
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='报告不存在')
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
        raise HTTPException(status_code=404, detail='报告不存在')
    # 解析嵌入的 JSON 数据
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()
    import re, json
    m = re.search(r'<script type="application/json" id="report-data">(.*?)</script>', html, re.S)
    if not m:
        raise HTTPException(status_code=500, detail='报告数据缺失')
    data = json.loads(m.group(1))
    return data 