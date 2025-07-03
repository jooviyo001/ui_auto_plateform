import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models import Base
from app.core.database import engine
from app.models import user, project, case, execution, setting  # 确保导入所有 models
import subprocess


def reset_database():
    print("正在删除所有表...")
    Base.metadata.drop_all(bind=engine)
    print("正在根据 models 重新创建所有表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表结构已重置。")

def create_superadmin():
    print("正在创建超级管理员账户...")
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    script_path = os.path.join(project_root, "backend", "scripts", "create_superadmin.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("创建超级管理员时出错：", result.stderr)

if __name__ == "__main__":
    reset_database()
    create_superadmin()
    print("全部完成！") 