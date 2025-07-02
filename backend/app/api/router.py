from fastapi import APIRouter
from app.api.v1 import project, case, execution, report, user, settings

api_router = APIRouter()

api_router.include_router(project.router, prefix='/project', tags=['项目管理'])
api_router.include_router(case.router, prefix='/case', tags=['用例管理'])
api_router.include_router(execution.router, prefix='/execution', tags=['执行中心'])
api_router.include_router(report.router, prefix='/report', tags=['报告中心'])
api_router.include_router(user.router, prefix='/user', tags=['用户管理'])
api_router.include_router(settings.router, prefix='/settings', tags=['系统设置']) 