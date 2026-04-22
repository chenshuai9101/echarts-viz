#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ECharts图表模板库
功能：预置各类图表模板配置
"""

from typing import Dict, Any, List

# ==================== 折线图模板 ====================

def line_chart_template(
    title: str,
    x_data: List,
    series_data: List[Dict],
    smooth: bool = True,
    show_area: bool = False,
    theme: str = "default"
) -> Dict:
    """折线图模板"""
    colors = get_colors(theme)
    
    series = []
    for i, item in enumerate(series_data):
        series_item = {
            'name': item.get('name', f'系列{i+1}'),
            'type': 'line',
            'data': item.get('data', []),
            'smooth': smooth,
            'symbol': 'circle',
            'symbolSize': 6,
            'lineStyle': {'width': 2},
            'itemStyle': {'color': colors[i % len(colors)]}
        }
        if show_area:
            series_item['areaStyle'] = {
                'color': {
                    'type': 'linear',
                    'x': 0, 'y': 0, 'x2': 0, 'y2': 1,
                    'colorStops': [
                        {'offset': 0, 'color': colors[i % len(colors)] + '99'},
                        {'offset': 1, 'color': colors[i % len(colors)] + '10'}
                    ]
                }
            }
        series.append(series_item)
    
    return {
        'title': {
            'text': title,
            'left': 'center',
            'textStyle': {'fontSize': 16, 'fontWeight': 'normal'}
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {'type': 'cross'}
        },
        'legend': {
            'data': [item.get('name', f'系列{i+1}') for i, item in enumerate(series_data)],
            'bottom': 0
        },
        'grid': {
            'left': '3%', 'right': '4%', 'bottom': '15%', 'containLabel': True
        },
        'xAxis': {
            'type': 'category',
            'data': x_data,
            'boundaryGap': False,
            'axisLabel': {}
        },
        'yAxis': {'type': 'value'},
        'series': series,
        'colors': colors
    }

# ==================== 柱状图模板 ====================

def bar_chart_template(
    title: str,
    x_data: List,
    series_data: List[Dict],
    theme: str = "default",
    orientation: str = "vertical"
) -> Dict:
    """柱状图模板"""
    colors = get_colors(theme)
    
    series = []
    for i, item in enumerate(series_data):
        series.append({
            'name': item.get('name', f'系列{i+1}'),
            'type': 'bar',
            'data': item.get('data', []),
            'itemStyle': {
                'color': {
                    'type': 'linear',
                    'x': 0 if orientation == 'vertical' else 0,
                    'y': 0 if orientation == 'vertical' else 0,
                    'x2': 0 if orientation == 'vertical' else 1,
                    'y2': 1 if orientation == 'vertical' else 0,
                    'colorStops': [
                        {'offset': 0, 'color': colors[i % len(colors)]},
                        {'offset': 1, 'color': colors[i % len(colors)] + 'cc'}
                    ]
                },
                'borderRadius': [4, 4, 0, 0] if orientation == 'vertical' else [0, 4, 4, 0]
            },
            'barWidth': '60%'
        })
    
    config = {
        'title': {
            'text': title,
            'left': 'center',
            'textStyle': {'fontSize': 16, 'fontWeight': 'normal'}
        },
        'tooltip': {
            'trigger': 'axis',
            'axisPointer': {'type': 'shadow'}
        },
        'legend': {
            'data': [item.get('name', f'系列{i+1}') for i, item in enumerate(series_data)],
            'bottom': 0
        },
        'grid': {
            'left': '3%', 'right': '4%', 'bottom': '15%', 'containLabel': True
        },
        'series': series,
        'colors': colors
    }
    
    if orientation == 'vertical':
        config['xAxis'] = {
            'type': 'category',
            'data': x_data,
            'axisLabel': {}
        }
        config['yAxis'] = {'type': 'value'}
    else:
        config['xAxis'] = {'type': 'value'}
        config['yAxis'] = {
            'type': 'category',
            'data': x_data,
            'axisLabel': {}
        }
    
    return config

# ==================== 饼图模板 ====================

def pie_chart_template(
    title: str,
    data: List[Dict],
    theme: str = "default",
    radius: List = None,
    show_label: bool = True
) -> Dict:
    """饼图模板"""
    colors = get_colors(theme)
    
    if radius is None:
        radius = ['40%', '70%']
    
    pie_data = []
    for i, item in enumerate(data):
        pie_data.append({
            'name': item.get('name', f'项目{i+1}'),
            'value': item.get('value', 0)
        })
    
    return {
        'title': {
            'text': title,
            'left': 'center',
            'textStyle': {'fontSize': 16, 'fontWeight': 'normal'}
        },
        'tooltip': {
            'trigger': 'item',
            'formatter': '{b}: {c} ({d}%)'
        },
        'legend': {
            'orient': 'vertical',
            'right': '5%',
            'top': 'center',
            'data': [item.get('name', f'项目{i+1}') for i, item in enumerate(data)]
        },
        'color': colors,
        'series': [{
            'name': title,
            'type': 'pie',
            'radius': radius,
            'center': ['40%', '50%'],
            'avoidLabelOverlap': False,
            'itemStyle': {
                'borderRadius': 8,
                'borderColor': '#fff',
                'borderWidth': 2
            },
            'label': {
                'show': show_label,
                'formatter': '{b}: {d}%',
                'fontSize': 12
            },
            'labelLine': {
                'show': show_label,
                'lineStyle': {'color': '#999'}
            },
            'data': pie_data
        }]
    }

# ==================== 散点图模板 ====================

def scatter_chart_template(
    title: str,
    data: List[List],
    x_name: str = "",
    y_name: str = "",
    theme: str = "default"
) -> Dict:
    """散点图模板"""
    colors = get_colors(theme)
    
    return {
        'title': {
            'text': title,
            'left': 'center',
            'textStyle': {'fontSize': 16, 'fontWeight': 'normal'}
        },
        'tooltip': {
            'trigger': 'item',
            'formatter': lambda params: f'{params.value[0]}, {params.value[1]}'
        },
        'grid': {
            'left': '3%', 'right': '10%', 'bottom': '10%', 'containLabel': True
        },
        'xAxis': {
            'type': 'value',
            'name': x_name,
            'scale': True
        },
        'yAxis': {
            'type': 'value',
            'name': y_name,
            'scale': True
        },
        'series': [{
            'type': 'scatter',
            'symbolSize': 12,
            'data': data,
            'itemStyle': {
                'color': colors[0],
                'opacity': 0.7
            }
        }],
        'colors': colors
    }

# ==================== 雷达图模板 ====================

def radar_chart_template(
    title: str,
    indicators: List[Dict],
    series_data: List[Dict],
    theme: str = "default"
) -> Dict:
    """雷达图模板"""
    colors = get_colors(theme)
    
    series = []
    for i, item in enumerate(series_data):
        series.append({
            'name': item.get('name', f'系列{i+1}'),
            'type': 'radar',
            'data': [{'value': item.get('data', []), 'name': item.get('name', '')}],
            'lineStyle': {'color': colors[i % len(colors)]},
            'areaStyle': {'color': colors[i % len(colors)] + '40'},
            'itemStyle': {'color': colors[i % len(colors)]}
        })
    
    return {
        'title': {
            'text': title,
            'left': 'center',
            'textStyle': {'fontSize': 16, 'fontWeight': 'normal'}
        },
        'tooltip': {},
        'legend': {
            'data': [item.get('name', f'系列{i+1}') for i, item in enumerate(series_data)],
            'bottom': 0
        },
        'radar': {
            'indicator': indicators,
            'center': ['50%', '50%'],
            'radius': '65%'
        },
        'series': series,
        'colors': colors
    }

# ==================== 工具函数 ====================

def get_colors(theme: str) -> List[str]:
    """获取主题配色"""
    palettes = {
        'default': ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
        'light': ['#66b3ff', '#99ccff', '#cce0ff', '#ffe6cc', '#ffd9b3', '#d4f4dd', '#e8d5f2'],
        'dark': ['#5b8def', '#37d39b', '#f5b942', '#ff7b7b', '#a78bfa', '#fbbf24', '#34d399'],
        'infographic': ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff', '#5f27cd', '#00d2d3'],
        'business': ['#2c3e50', '#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', '#1abc9c'],
        'nature': ['#27ae60', '#2ecc71', '#1abc9c', '#16a085', '#3498db', '#2980b9', '#9b59b6']
    }
    return palettes.get(theme, palettes['default'])

def get_chart_template(chart_type: str) -> callable:
    """获取图表模板"""
    templates = {
        'line': line_chart_template,
        'bar': bar_chart_template,
        'pie': pie_chart_template,
        'scatter': scatter_chart_template,
        'radar': radar_chart_template
    }
    return templates.get(chart_type, line_chart_template)

if __name__ == "__main__":
    # 测试
    config = line_chart_template(
        title="销售趋势",
        x_data=["1月", "2月", "3月", "4月"],
        series_data=[
            {'name': '2024年', 'data': [120, 135, 128, 145]}
        ],
        show_area=True
    )
    print("折线图模板配置已生成")
