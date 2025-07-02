import os
from jinja2 import Template
import json
from collections import Counter, defaultdict

REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
os.makedirs(REPORT_DIR, exist_ok=True)

REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang='zh-CN'>
<head>
    <meta charset='UTF-8'>
    <title>测试报告 - {{ task_id }}</title>
    <style>
        body { font-family: Arial; margin: 20px; background: #f7f9fa; }
        .summary { margin-bottom: 20px; }
        .stat { font-size: 16px; margin-bottom: 10px; }
        .charts { display: flex; gap: 40px; margin-bottom: 30px; }
        .chart-box { background: #fff; border-radius: 8px; box-shadow: 0 2px 8px #eee; padding: 20px; }
        table { border-collapse: collapse; width: 100%; background: #fff; }
        th, td { border: 1px solid #ccc; padding: 8px; }
        th { background: #eaf1fb; }
        .success { color: #52c41a; font-weight: bold; }
        .fail { color: #f5222d; font-weight: bold; }
        .collapsible { cursor: pointer; background: #f9f9f9; border: none; outline: none; width: 100%; text-align: left; }
        .content { display: none; padding: 0 18px; }
        .group-stat { margin: 10px 0 20px 0; }
    </style>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
</head>
<body>
    <h2>测试报告 - 任务ID: {{ task_id }}</h2>
    <div class='summary'>
        <div class='stat'>开始时间: {{ start_time }} | 结束时间: {{ end_time }} | 耗时: {{ duration }} 秒</div>
        <div class='stat'>总用例数: {{ total }} | 成功: <span class='success'>{{ success }}</span> | 失败: <span class='fail'>{{ fail }}</span></div>
    </div>
    <div class='charts'>
        <div class='chart-box' style='width:320px;'>
            <div id='pie' style='width: 300px; height: 240px;'></div>
        </div>
        <div class='chart-box' style='flex:1;'>
            <div id='bar' style='width: 100%; height: 240px;'></div>
        </div>
    </div>
    <div class='group-stat'>
        <b>分组统计：</b>
        {% for group, stat in group_stats.items() %}
            <span style='margin-right:20px;'>{{ group }}：<span class='success'>{{ stat.success }}</span> / <span class='fail'>{{ stat.fail }}</span> / {{ stat.total }}</span>
        {% endfor %}
    </div>
    <table>
        <tr><th>用例ID</th><th>分组</th><th>执行结果</th><th>步骤详情</th><th>错误信息</th></tr>
        {% for r in results %}
        <tr>
            <td>{{ r.case_id }}</td>
            <td>{{ r.group or '-' }}</td>
            <td class='{{ 'success' if r.success else 'fail' }}'>{{ '成功' if r.success else '失败' }}</td>
            <td>
                <button class='collapsible'>查看步骤</button>
                <div class='content'>
                    {% if r.steps_result %}{{ r.steps_result|join('<br>') }}{% endif %}
                </div>
            </td>
            <td>{% if r.error %}<span class='fail'>{{ r.error }}</span>{% endif %}</td>
        </tr>
        {% endfor %}
    </table>
    <button onclick="window.print()" style="margin:20px 0 0 0; padding:8px 20px; font-size:16px;">导出PDF</button>
    <script>
    var coll = document.getElementsByClassName('collapsible');
    for (var i = 0; i < coll.length; i++) {
      coll[i].addEventListener('click', function() {
        this.classList.toggle('active');
        var content = this.nextElementSibling;
        if (content.style.display === 'block') {
          content.style.display = 'none';
        } else {
          content.style.display = 'block';
        }
      });
    }
    // 图表渲染
    var stat = JSON.parse(document.getElementById('report-data').textContent);
    var pie = echarts.init(document.getElementById('pie'));
    pie.setOption({
      title: { text: '成功/失败分布', left: 'center', top: 10, textStyle: { fontSize: 16 } },
      tooltip: { trigger: 'item' },
      legend: { bottom: 0 },
      series: [{
        type: 'pie', radius: '60%',
        data: [
          { value: stat.success, name: '成功' },
          { value: stat.fail, name: '失败' }
        ],
        label: { fontSize: 14 }
      }]
    });
    var bar = echarts.init(document.getElementById('bar'));
    bar.setOption({
      title: { text: '分组成功/失败统计', left: 'center', textStyle: { fontSize: 16 } },
      tooltip: { trigger: 'axis' },
      legend: { data: ['成功', '失败'] },
      xAxis: { type: 'category', data: stat.group_bar.groups },
      yAxis: { type: 'value' },
      series: [
        { name: '成功', type: 'bar', data: stat.group_bar.success },
        { name: '失败', type: 'bar', data: stat.group_bar.fail }
      ]
    });
    </script>
    <script type="application/json" id="report-data">{{ stat_json }}</script>
</body>
</html>
"""

def generate_html_report(task_id, results, start_time, end_time):
    success = sum(1 for r in results if r.get('success'))
    fail = len(results) - success
    total = len(results)
    duration = round((end_time - start_time).total_seconds(), 2) if start_time and end_time else ''
    # 分组统计
    group_stats = defaultdict(lambda: {'success': 0, 'fail': 0, 'total': 0})
    for r in results:
        group = r.get('group') or '未分组'
        group_stats[group]['total'] += 1
        if r.get('success'):
            group_stats[group]['success'] += 1
        else:
            group_stats[group]['fail'] += 1
    group_bar = {
        'groups': list(group_stats.keys()),
        'success': [group_stats[g]['success'] for g in group_stats],
        'fail': [group_stats[g]['fail'] for g in group_stats]
    }
    stat_json = json.dumps({
        'task_id': task_id,
        'start_time': str(start_time),
        'end_time': str(end_time),
        'duration': duration,
        'total': total,
        'success': success,
        'fail': fail,
        'group_stats': group_stats,
        'group_bar': group_bar,
        'results': results
    }, ensure_ascii=False)
    template = Template(REPORT_TEMPLATE)
    html = template.render(
        task_id=task_id,
        results=results,
        start_time=start_time,
        end_time=end_time,
        duration=duration,
        total=total,
        success=success,
        fail=fail,
        group_stats=group_stats,
        stat_json=stat_json
    )
    report_path = os.path.join(REPORT_DIR, f'{task_id}.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return report_path 