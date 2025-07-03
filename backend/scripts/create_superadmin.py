import sys
import os

# 保证可以找到 app 包
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

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

if __name__ == "__main__":
    create_tables()
    create_superadmin()