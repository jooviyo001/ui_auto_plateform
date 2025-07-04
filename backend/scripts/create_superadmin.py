import sys
import os

# 计算 backend 的上一级目录（项目根目录），并插入 sys.path[0]
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file)
project_root = os.path.dirname(backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.core.database import engine, SessionLocal
from app.models.user import User
from app.models import Base
import bcrypt

def create_tables():
    Base.metadata.create_all(bind=engine)

def create_superadmin():
    session = SessionLocal()
    username = "admin"
    password = "123456"
    role = "superadmin"
    
    # 检查是否已存在
    user = session.query(User).filter_by(username=username).first()
    if user:
        print("超级管理员已存在，无需重复创建。")
        session.close()
        return
    # 密码加密
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user = User(username=username, hashed_password=hashed_password, role=role, is_active=True)
    session.add(user)
    session.commit()
    session.close()
    print("超级管理员创建成功，账号：admin，密码：123456")

def print_users_passwords():
    session = SessionLocal()
    users = session.query(User).all()
    for user in users:
        print(f"用户名: {user.username}, 密码: {user.hashed_password}, 是否激活: {user.is_active}")
    session.close()

if __name__ == "__main__":
    create_tables()
    create_superadmin()
    print_users_passwords()