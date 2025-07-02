import sys
sys.path.append('..')
from app.core.database import SessionLocal
from app.services.user_service import UserService
from app.schemas.user import UserCreate

def main():
    db = SessionLocal()
    username = input('请输入超管用户名: ')
    password = input('请输入超管密码: ')
    if UserService.get_user_by_username(db, username):
        print('用户已存在')
        return
    user = UserCreate(username=username, password=password, role='superadmin')
    UserService.create_user(db, user)
    print('超管创建成功')
    db.close()

if __name__ == '__main__':
    main() 