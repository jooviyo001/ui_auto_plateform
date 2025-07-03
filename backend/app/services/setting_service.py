from app.models.setting import Setting, Base
from app.schemas.setting import Setting
from sqlalchemy.orm import Session
import json

class SettingService:
    @staticmethod
    def get_by_key(db: Session, key: str):
        # 查询时直接获取Setting实例的实际值
        setting = db.query(Setting).filter(Setting.key == key).first()
        if setting:
            # 确保返回的是带有实际值的Setting实例
            return SettingService.parse_value(setting)
        return None

    @staticmethod
    def get_all(db: Session, group: str | None = None):
        query = db.query(Setting)
        if group:
            query = query.filter(Setting.group == group)
        settings = query.all()
        return [SettingService.parse_value(s) for s in settings]

    @staticmethod
    def set_setting(db: Session, setting: Setting):
        db_setting = SettingService.get_by_key(db, setting.key)
        if db_setting:
            # 确保我们处理的是实际的Setting实例，避免直接操作Column对象
            db_setting.value = str(setting.value) if setting.value is not None else ''  # type: ignore
            db_setting.type = str(setting.type) if setting.type is not None else ''  # type: ignore
            db_setting.group = str(setting.group) if setting.group is not None else ''  # type: ignore
            db_setting.description = str(setting.description) if setting.description is not None else ''  # type: ignore
        else:
            db_setting = Setting(**setting.dict())
            db.add(db_setting)
        db.commit()
        db.refresh(db_setting)
        return db_setting

    @staticmethod
    def delete_setting(db: Session, key: str):
        db_setting = SettingService.get_by_key(db, key)
        if db_setting:
            db.delete(db_setting)
            db.commit()
            return True
        return False

    @staticmethod
    def parse_value(setting: Setting):
        # 确保我们获取的是实际的值而不是SQLAlchemy Column对象
        value = setting.value if hasattr(setting, 'value') else None
        data_type = setting.type if hasattr(setting, 'type') else None
        # 确保 data_type 是字符串类型
        if isinstance(data_type, str):
            data_type = data_type.lower()
        else:
            data_type = str(data_type).lower() if data_type is not None else None
        value = str(value) if isinstance(value, str) or (isinstance(value, object) and not isinstance(value, str)) else value

        if data_type == 'int':
            try:
                return int(str(value)) if value is not None else None
            except ValueError:
                return None
        elif data_type == 'bool':
            return str(value).lower() in ('1', 'true', 'yes') if value is not None else None
        elif data_type == 'json':
            try:
                return json.loads(str(value)) if value is not None else None
            except json.JSONDecodeError:
                return None
        return str(value) if value is not None else None
