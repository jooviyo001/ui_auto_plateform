from app.core.celery_app import celery_app
from app.services.drission_executor import DrissionExecutor
from app.services.case_service import CaseService
from app.services.execution_service import ExecutionService
from app.schemas.case import Step
from app.core.database import SessionLocal
from app.services.report_service import generate_html_report
import json, datetime

@celery_app.task(bind=True)
def batch_run_cases_task(self, case_ids):
    db = SessionLocal()
    results = []
    start_time = datetime.datetime.utcnow()
    for case_id in case_ids:
        db_case = CaseService.get_case(db, case_id)
        if not db_case:
            results.append({"case_id": case_id, "success": False, "error": "用例不存在"})
            continue
        try:
            steps = [Step(**step) for step in json.loads(db_case.steps)]
            executor = DrissionExecutor()
            step_dicts = [step.dict() for step in steps]
            step_results = executor.run_steps(step_dicts)
            results.append({"case_id": case_id, "success": True, "steps_result": step_results})
        except Exception as e:
            results.append({"case_id": case_id, "success": False, "error": str(e)})
    end_time = datetime.datetime.utcnow()
    # 生成报告
    generate_html_report(self.request.id, results, start_time, end_time)
    db.close()
    return results 