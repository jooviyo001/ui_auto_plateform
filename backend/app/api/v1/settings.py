from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.setting import Setting, SettingOut
from app.services.setting_service import SettingService
from app.api.v1.user import require_roles, ROLE_SUPERADMIN, get_current_user
from typing import List
from app.utils.response import success, fail
from app.schemas.common import ResponseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=ResponseModel)
def list_settings(group: str = "", db: Session = Depends(get_db), _: str = Depends(require_roles(ROLE_SUPERADMIN))):
    data = SettingService.get_all(db, group)
    return success(data)

@router.post('/', response_model=ResponseModel)
def set_setting(setting: Setting, db: Session = Depends(get_db), _: str = Depends(require_roles(ROLE_SUPERADMIN))):
    data = SettingService.set_setting(db, setting)
    return success(data, msg="设置成功")

@router.delete('/{key}', response_model=ResponseModel)
def delete_setting(key: str, db: Session = Depends(get_db), _: str = Depends(require_roles(ROLE_SUPERADMIN))):
    ok = SettingService.delete_setting(db, key)
    if not ok:
        return fail('配置不存在', code=404)
    return success(None, msg="删除成功")