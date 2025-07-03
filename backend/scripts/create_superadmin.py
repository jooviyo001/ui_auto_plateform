import sys
import os

# 将backend目录添加到系统路径中
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal, engine
from app.models.user import User, Base
from app.schemas.user import UserCreate
from app.services.user_service import UserService

# 自动建表，确保users表存在
Base.metadata.create_all(bind=engine)

# 创建数据库连接
db = SessionLocal()

# 超级管理员信息
superadmin_data = {
    "username": "admin01",
    "password": "123456",
    "role": "superadmin",
    "is_active": True
}

# 检查是否已存在admin用户
if UserService.get_user_by_username(db, "admin"):
    print("admin 用户已存在，无需重复创建。")
else:
    # 创建超级管理员
    user_in = UserCreate(**superadmin_data)
    UserService.create_user(db, user_in)
    print("Superadmin(admin/123456) created successfully!")