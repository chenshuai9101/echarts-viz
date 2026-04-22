#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据解析工具
功能：解析各种格式的数据（JSON、CSV、表格文本）
"""

import json
import re
from typing import Dict, List, Any, Union, Optional
from datetime import datetime

def parse_json(data_str: str) -> Optional[List[Dict]]:
    """解析JSON格式数据"""
    try:
        data = json.loads(data_str)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return [data]
        return None
    except json.JSONDecodeError:
        return None

def parse_csv(data_str: str, delimiter: str = ',') -> Optional[List[Dict]]:
    """解析CSV格式数据"""
    lines = [line.strip() for line in data_str.strip().split('\n') if line.strip()]
    if len(lines) < 2:
        return None
    
    # 解析表头
    headers = [h.strip().strip('"') for h in lines[0].split(delimiter)]
    
    # 解析数据行
    result = []
    for line in lines[1:]:
        values = [v.strip().strip('"') for v in line.split(delimiter)]
        if len(values) == len(headers):
            row = dict(zip(headers, values))
            result.append(row)
    
    return result if result else None

def parse_text_table(data_str: str) -> Optional[List[Dict]]:
    """解析文本表格数据（使用空格或制表符分隔）"""
    lines = [line.strip() for line in data_str.strip().split('\n') if line.strip()]
    if len(lines) < 2:
        return None
    
    # 尝试用制表符分隔
    if '\t' in lines[0]:
        return parse_csv(data_str, '\t')
    
    # 使用多个空格分隔
    parts = lines[0].split()
    if len(parts) >= 2:
        headers = parts
        result = []
        for line in lines[1:]:
            values = line.split()
            if len(values) == len(headers):
                row = dict(zip(headers, values))
                result.append(row)
        return result if result else None
    
    return None

def parse_markdown_table(data_str: str) -> Optional[List[Dict]]:
    """解析Markdown表格格式"""
    lines = [line.strip() for line in data_str.strip().split('\n') if line.strip()]
    result = []
    
    header_parsed = False
    headers = []
    
    for line in lines:
        # 跳过分隔行
        if re.match(r'^\|[\s\-:|]+\|$', line):
            continue
        
        # 解析表格行
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        
        if not header_parsed:
            headers = cells
            header_parsed = True
        else:
            if len(cells) == len(headers):
                row = dict(zip(headers, cells))
                result.append(row)
    
    return result if result else None

def auto_parse(data_str: str) -> Optional[List[Dict]]:
    """自动识别并解析数据格式"""
    data_str = data_str.strip()
    
    # 尝试JSON
    if data_str.startswith('[') or data_str.startswith('{'):
        result = parse_json(data_str)
        if result:
            return result
    
    # 尝试Markdown表格
    if '|' in data_str and ('---' in data_str or re.search(r'\|[\s\-]+\|', data_str)):
        result = parse_markdown_table(data_str)
        if result:
            return result
    
    # 尝试CSV
    result = parse_csv(data_str)
    if result:
        return result
    
    # 尝试文本表格
    result = parse_text_table(data_str)
    if result:
        return result
    
    return None

def convert_value(value: str) -> Union[str, int, float]:
    """转换值为合适的数据类型"""
    value = value.strip()
    
    # 空值
    if not value or value.lower() in ['null', 'none', 'nan', '']:
        return 0
    
    # 尝试转换为数字
    try:
        if '.' in value:
            return float(value)
        return int(value)
    except ValueError:
        pass
    
    # 尝试解析百分比
    percent_match = re.match(r'^(-?\d+\.?\d*)%$', value)
    if percent_match:
        return float(percent_match.group(1))
    
    # 尝试解析带单位的数字
    num_match = re.match(r'^(-?\d+\.?\d*)\s*(万|亿|千|百)?$', value)
    if num_match:
        num = float(num_match.group(1))
        unit = num_match.group(2)
        multipliers = {'万': 10000, '亿': 100000000, '千': 1000, '百': 100}
        return num * multipliers.get(unit, 1)
    
    return value

def normalize_data(data: List[Dict]) -> List[Dict]:
    """标准化数据"""
    if not data:
        return []
    
    result = []
    for item in data:
        normalized_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                normalized_item[key] = convert_value(value)
            else:
                normalized_item[key] = value
        result.append(normalized_item)
    
    return result

def get_data_summary(data: List[Dict]) -> Dict[str, Any]:
    """获取数据摘要"""
    if not data:
        return {}
    
    keys = list(data[0].keys())
    summary = {
        'row_count': len(data),
        'column_count': len(keys),
        'columns': keys,
        'column_types': {}
    }
    
    # 分析每列的数据类型
    for key in keys:
        values = [str(item.get(key, '')) for item in data[:10]]
        
        # 检测是否为数值列
        numeric_count = 0
        for v in values:
            try:
                float(v)
                numeric_count += 1
            except ValueError:
                pass
        
        if numeric_count > len(values) * 0.7:
            summary['column_types'][key] = 'numeric'
        else:
            summary['column_types'][key] = 'categorical'
    
    return summary

def filter_data(data: List[Dict], conditions: Dict) -> List[Dict]:
    """根据条件过滤数据"""
    if not data or not conditions:
        return data
    
    result = []
    for item in data:
        match = True
        for key, value in conditions.items():
            if item.get(key) != value:
                match = False
                break
        if match:
            result.append(item)
    
    return result

def aggregate_data(data: List[Dict], group_by: str, agg_field: str, agg_func: str = 'sum') -> List[Dict]:
    """聚合数据"""
    if not data or not group_by or not agg_field:
        return data
    
    groups = {}
    for item in data:
        key_value = item.get(group_by)
        if key_value not in groups:
            groups[key_value] = []
        groups[key_value].append(item.get(agg_field, 0))
    
    result = []
    for key, values in groups.items():
        if agg_func == 'sum':
            agg_value = sum(values)
        elif agg_func == 'avg':
            agg_value = sum(values) / len(values) if values else 0
        elif agg_func == 'count':
            agg_value = len(values)
        elif agg_func == 'max':
            agg_value = max(values) if values else 0
        elif agg_func == 'min':
            agg_value = min(values) if values else 0
        else:
            agg_value = sum(values)
        
        result.append({group_by: key, f'{agg_func}_{agg_field}': agg_value})
    
    return result

if __name__ == "__main__":
    # 测试
    test_json = '[{"月份":"1月","销售额":120000},{"月份":"2月","销售额":135000}]'
    result = auto_parse(test_json)
    print("JSON解析结果:", result)
    
    summary = get_data_summary(result)
    print("数据摘要:", summary)
