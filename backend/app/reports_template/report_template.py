import importlib
import yaml
from pathlib import Path

def load_report_modules(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    modules = config.get('modules', [])
    module_functions = []

    for module in modules:
        try:
            # 假设每个模块都在 report_modules 包中
            mod = importlib.import_module(f'report_modules.{module}')
            # 假设每个模块都有一个 register 函数用于注册或初始化
            if hasattr(mod, 'register'):
                module_functions.append(mod.register)
        except ImportError as e:
            print(f"Error importing module {module}: {e}")

    return module_functions


def generate_report():
    config_path = Path(__file__).parent / 'template_config.yaml'
    register_functions = load_report_modules(config_path)

    # 初始化报告内容
    report_content = {}

    # 执行各个模块的注册函数以生成报告内容
    for func in register_functions:
        content = func()
        report_content.update(content)

    # 这里可以添加将 report_content 渲染为最终报告的逻辑，如 HTML 或 PDF
    return report_content