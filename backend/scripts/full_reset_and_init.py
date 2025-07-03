import sys
import os

# 计算 backend 的上一级目录（项目根目录），并插入 sys.path[0]
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(current_file)
project_root = os.path.dirname(backend_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 可选：调试用，打印 sys.path
print("sys.path:", sys.path)

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
    script_path = os.path.join(os.path.dirname(__file__), "create_superadmin.py")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("创建超级管理员时出错：", result.stderr)

if __name__ == "__main__":
    reset_database()
    # create_superadmin()
    print("全部完成！") 