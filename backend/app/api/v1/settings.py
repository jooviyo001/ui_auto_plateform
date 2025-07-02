from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.setting import SettingBase, SettingOut
from app.services.setting_service import SettingService
from app.api.v1.user import require_roles, ROLE_SUPERADMIN, get_current_user
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/', response_model=List[SettingOut])
def list_settings(group: str = None, db: Session = Depends(get_db), _: str = Depends(require_roles([ROLE_SUPERADMIN]))):
    return SettingService.get_all(db, group)

@router.post('/', response_model=SettingOut)
def set_setting(setting: SettingBase, db: Session = Depends(get_db), _: str = Depends(require_roles([ROLE_SUPERADMIN]))):
    return SettingService.set_setting(db, setting)

@router.delete('/{key}')
def delete_setting(key: str, db: Session = Depends(get_db), _: str = Depends(require_roles([ROLE_SUPERADMIN]))):
    ok = SettingService.delete_setting(db, key)
    if not ok:
        raise HTTPException(status_code=404, detail='配置不存在')
    return {"msg": "删除成功"} 