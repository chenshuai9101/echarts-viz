#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECharts图表生成核心脚本
功能：根据数据自动生成ECharts图表的HTML文件
"""

import json
import sys
import re
from typing import Dict, List, Any, Optional

# 图表类型推荐规则
CHART_RECOMMENDATIONS = {
    'time_series': {
        'indicators': ['日期', '月份', '年份', '时间', 'date', 'month', 'year', 'time'],
        'chart_type': 'line',
        'reason': '检测到时间序列特征，推荐使用折线图展示趋势'
    },
    'category': {
        'indicators': ['部门', '产品', '类型', '分类', 'category', 'product', 'type'],
        'chart_type': 'bar',
        'reason': '检测到分类字段，推荐使用柱状图进行对比'
    },
    'proportion': {
        'indicators': ['占比', '比例', '百分比', 'proportion', 'percent', 'ratio'],
        'chart_type': 'pie',
        'reason': '检测到占比数据，推荐使用饼图展示构成'
    },
    'correlation': {
        'indicators': ['关联', '相关', 'correlation', 'relationship'],
        'chart_type': 'scatter',
        'reason': '检测到关联分析需求，推荐使用散点图'
    }
}

# 默认配色方案
COLOR_PALETTES = {
    'default': ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
    'light': ['#66b3ff', '#99ccff', '#cce0ff', '#ffe6cc', '#ffd9b3'],
    'dark': ['#5b8def', '#37d39b', '#f5b942', '#ff7b7b', '#a78bfa'],
    'infographic': ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff', '#5f27cd']
}

def parse_data(data_str: str) -> List[Dict]:
    """解析数据字符串"""
    # 尝试JSON格式
    try:
        if isinstance(data_str, str):
            return json.loads(data_str)
        return data_str
    except json.JSONDecodeError:
        pass
    
    # 尝试CSV格式
    lines = data_str.strip().split('\n')
    if len(lines) >= 2:
        headers = [h.strip() for h in lines[0].split(',')]
        result = []
        for line in lines[1:]:
            values = [v.strip() for v in line.split(',')]
            row = dict(zip(headers, values))
            result.append(row)
        return result
    
    return []

def detect_chart_type(data: List[Dict], user_hint: str = "") -> Dict[str, Any]:
    """根据数据特征和用户提示推荐图表类型"""
    if not data:
        return {'chart_type': 'line', 'reason': '默认使用折线图'}
    
    # 检查用户提示
    hint_lower = user_hint.lower()
    if any(word in hint_lower for word in ['饼图', 'pie', '占比', '比例', '构成']):
        return {'chart_type': 'pie', 'reason': '根据您的需求使用饼图'}
    if any(word in hint_lower for word in ['柱状图', '柱形', 'bar', '对比']):
        return {'chart_type': 'bar', 'reason': '根据您的需求使用柱状图'}
    if any(word in hint_lower for word in ['折线图', '趋势', 'line', '趋势图']):
        return {'chart_type': 'line', 'reason': '根据您的需求使用折线图'}
    if any(word in hint_lower for word in ['散点', 'scatter', '分布']):
        return {'chart_type': 'scatter', 'reason': '根据您的需求使用散点图'}
    
    # 分析数据特征
    keys = list(data[0].keys()) if data else []
    first_value = str(data[0][keys[1]]) if len(keys) > 1 else ""
    
    # 时间序列检测
    time_keywords = ['日期', '月份', '年份', '时间', 'date', 'month', 'year', 'time', '日', '周']
    for key in keys:
        if any(kw in key.lower() for kw in time_keywords):
            return CHART_RECOMMENDATIONS['time_series']
    
    # 占比数据检测
    if '%' in first_value or any(kw in str(keys) for kw in ['占比', '比例', 'percent']):
        return CHART_RECOMMENDATIONS['proportion']
    
    # 默认使用柱状图
    return CHART_RECOMMENDATIONS['category']

def extract_chart_config(data: List[Dict], chart_type: str, title: str = "", theme: str = "default") -> Dict:
    """提取图表配置"""
    if not data:
        return {}
    
    keys = list(data[0].keys())
    x_key = keys[0]
    y_key = keys[1] if len(keys) > 1 else keys[0]
    
    config = {
        'title': {
            'text': title or f'{y_key}分析',
            'left': 'center',
            'textStyle': {'fontSize': 16, 'fontWeight': 'normal'}
        },
        'tooltip': {
            'trigger': 'axis' if chart_type != 'pie' else 'item',
            'axisPointer': {'type': 'shadow'}
        },
        'legend': {
            'data': [y_key] if chart_type != 'pie' else [],
            'bottom': 0
        },
        'grid': {
            'left': '3%',
            'right': '4%',
            'bottom': '15%',
            'containLabel': True
        },
        'colors': COLOR_PALETTES.get(theme, COLOR_PALETTES['default'])
    }
    
    if chart_type in ['line', 'bar']:
        config['xAxis'] = {
            'type': 'category',
            'data': [str(item.get(x_key, '')) for item in data],
            'axisLabel': {'rotate': 0}
        }
        config['yAxis'] = {
            'type': 'value',
            'name': y_key
        }
    elif chart_type == 'pie':
        config['series'] = [{
            'name': y_key,
            'type': 'pie',
            'radius': ['40%', '70%'],
            'avoidLabelOverlap': False,
            'itemStyle': {
                'borderRadius': 10,
                'borderColor': '#fff',
                'borderWidth': 2
            },
            'label': {
                'show': True,
                'formatter': '{b}: {d}%'
            },
            'data': [
                {'name': item.get(x_key, ''), 'value': float(re.sub(r'[^\d.]', '', str(item.get(y_key, 0)))) or 0}
                for item in data
            ]
        }]
        return config
    elif chart_type == 'scatter':
        config['xAxis'] = {
            'type': 'value',
            'name': x_key
        }
        config['yAxis'] = {
            'type': 'value',
            'name': y_key
        }
    
    # 添加series
    config['series'] = [{
        'name': y_key,
        'type': chart_type,
        'data': [float(re.sub(r'[^\d.]', '', str(item.get(y_key, 0)))) or 0 for item in data],
        'smooth': chart_type == 'line',
        'areaStyle': {'opacity': 0.3} if chart_type == 'line' else None
    }]
    
    return config

def generate_html(config: Dict, chart_id: str = "chart") -> str:
    """生成HTML文件"""
    config_json = json.dumps(config, ensure_ascii=False)
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数据可视化图表</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            padding: 20px;
            min-height: 100vh;
        }}
        .chart-container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            padding: 20px;
            margin: 0 auto;
            max-width: 900px;
            height: 500px;
        }}
        #{chart_id} {{ width: 100%; height: 100%; }}
    </style>
</head>
<body>
    <div class="chart-container">
        <div id="{chart_id}"></div>
    </div>
    <script>
        var chartDom = document.getElementById('{chart_id}');
        var myChart = echarts.init(chartDom);
        var option = {config_json};
        option && myChart.setOption(option);
        
        // 响应式调整
        window.addEventListener('resize', function() {{
            myChart.resize();
        }});
    </script>
</body>
</html>'''
    
    return html

def main():
    """主函数"""
    # 示例数据
    sample_data = [
        {"月份": "1月", "销售额": 120000},
        {"月份": "2月", "销售额": 135000},
        {"月份": "3月", "销售额": 128000},
        {"月份": "4月", "销售额": 145000},
        {"月份": "5月", "销售额": 158000},
        {"月份": "6月", "销售额": 162000}
    ]
    
    # 检测图表类型
    chart_info = detect_chart_type(sample_data, "月度销售额趋势")
    chart_type = chart_info['chart_type']
    
    # 生成配置
    config = extract_chart_config(sample_data, chart_type, title="2024年月度销售额趋势", theme="default")
    
    # 生成HTML
    html = generate_html(config)
    
    # 输出
    output_path = "chart_output.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"图表已生成: {output_path}")
    print(f"图表类型: {chart_type}")
    print(f"推荐理由: {chart_info['reason']}")

if __name__ == "__main__":
    main()
