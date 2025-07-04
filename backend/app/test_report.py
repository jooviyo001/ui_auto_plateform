import jinja2
import yaml
from pathlib import Path
from reports_template.report_template import generate_report

# 生成报告
report_content = generate_report()

# 加载 Jinja2 模板
template_loader = jinja2.FileSystemLoader(searchpath=Path(__file__).parent / "reports_template")
template_env = jinja2.Environment(loader=template_loader)

# 渲染 HTML 报告
template = template_env.get_template("report_template.html")
html_report = template.render(report=report_content)

# 保存 HTML 报告
with open(Path(__file__).parent / "test_report.html", "w", encoding="utf-8") as f:
    f.write(html_report)

print("HTML 报告已生成，文件路径: test_report.html")