import pandas as pd
import json
from app.models.case import Case
from app.schemas.case import Step
from sqlalchemy.orm import Session

def export_cases_to_excel(cases, file_path):
    data = []
    for c in cases:
        steps = json.loads(c.steps)
        data.append({
            'id': c.id,
            'name': c.name,
            'project_id': c.project_id,
            'group': c.group,
            'description': c.description,
            'steps': json.dumps(steps, ensure_ascii=False)
        })
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)

def import_cases_from_excel(file_path, db: Session):
    df = pd.read_excel(file_path)
    from app.models.case import Case
    for _, row in df.iterrows():
        steps = json.loads(row['steps']) if isinstance(row['steps'], str) else []
        case = Case(
            name=row['name'],
            project_id=row['project_id'],
            group=row.get('group'),
            description=row.get('description'),
            steps=json.dumps(steps, ensure_ascii=False)
        )
        db.add(case)
    db.commit()

def export_cases_to_json(cases, file_path):
    data = []
    for c in cases:
        steps = json.loads(c.steps)
        data.append({
            'id': c.id,
            'name': c.name,
            'project_id': c.project_id,
            'group': c.group,
            'description': c.description,
            'steps': steps
        })
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def import_cases_from_json(file_path, db: Session):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for row in data:
        case = Case(
            name=row['name'],
            project_id=row['project_id'],
            group=row.get('group'),
            description=row.get('description'),
            steps=json.dumps(row['steps'], ensure_ascii=False)
        )
        db.add(case)
    db.commit() 