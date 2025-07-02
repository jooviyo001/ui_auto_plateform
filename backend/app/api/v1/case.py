from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Response
from sqlalchemy.orm import Session
from app.schemas.case import Case, Step
from app.services.case_service import CaseService
from app.core.database import SessionLocal
from typing import List
import json
from app.services.case_import_export import (
    export_cases_to_excel, import_cases_from_excel,
    export_cases_to_json, import_cases_from_json
)
import tempfile, os

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=Case)
def create_case(case: Case, db: Session = Depends(get_db)):
    return CaseService.create_case(db, case)

@router.get('/{case_id}', response_model=Case)
def get_case(case_id: int, db: Session = Depends(get_db)):
    db_case = CaseService.get_case(db, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="用例不存在")
    # 反序列化 steps
    case_dict = db_case.__dict__.copy()
    case_dict['steps'] = [Step(**step) for step in json.loads(db_case.steps)]
    return case_dict

@router.get('/', response_model=List[Case])
def get_cases(project_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_cases = CaseService.get_cases(db, project_id, skip, limit)
    result = []
    for db_case in db_cases:
        case_dict = db_case.__dict__.copy()
        case_dict['steps'] = [Step(**step) for step in json.loads(db_case.steps)]
        result.append(case_dict)
    return result

@router.put('/{case_id}', response_model=Case)
def update_case(case_id: int, case: Case, db: Session = Depends(get_db)):
    db_case = CaseService.update_case(db, case_id, case)
    if not db_case:
        raise HTTPException(status_code=404, detail="用例不存在")
    case_dict = db_case.__dict__.copy()
    case_dict['steps'] = [Step(**step) for step in json.loads(db_case.steps)]
    return case_dict

@router.delete('/{case_id}', response_model=Case)
def delete_case(case_id: int, db: Session = Depends(get_db)):
    db_case = CaseService.delete_case(db, case_id)
    if not db_case:
        raise HTTPException(status_code=404, detail="用例不存在")
    case_dict = db_case.__dict__.copy()
    case_dict['steps'] = [Step(**step) for step in json.loads(db_case.steps)]
    return case_dict

@router.get('/export')
def export_cases(format: str = 'excel', project_id: int = None, db: Session = Depends(get_db)):
    cases_query = db.query(Case)
    if project_id:
        cases_query = cases_query.filter(Case.project_id == project_id)
    cases = cases_query.all()
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx' if format=='excel' else '.json') as tmp:
        file_path = tmp.name
    if format == 'excel':
        export_cases_to_excel(cases, file_path)
        filename = 'cases.xlsx'
        media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        export_cases_to_json(cases, file_path)
        filename = 'cases.json'
        media_type = 'application/json'
    with open(file_path, 'rb') as f:
        content = f.read()
    os.remove(file_path)
    return Response(content, media_type=media_type, headers={
        'Content-Disposition': f'attachment; filename={filename}'
    })

@router.post('/import')
def import_cases(format: str = 'excel', file: UploadFile = File(...), db: Session = Depends(get_db)):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx' if format=='excel' else '.json') as tmp:
        file_path = tmp.name
        tmp.write(file.file.read())
    if format == 'excel':
        import_cases_from_excel(file_path, db)
    else:
        import_cases_from_json(file_path, db)
    os.remove(file_path)
    return {"msg": "导入成功"} 