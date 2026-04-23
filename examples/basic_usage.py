"""
ECharts for AI 基础使用示例
"""

import json
from echarts_for_ai import EChartsAI, create_chart

def demo_basic_chart():
    """基础图表示例"""
    print("=== 基础图表示例 ===")
    
    # 创建实例
    viz = EChartsAI()
    
    # 准备数据
    data = {
        "categories": ["苹果", "香蕉", "橙子", "葡萄", "西瓜"],
        "values": [120, 200, 150, 80, 70]
    }
    
    # 生成柱状图
    result = viz.create_chart(
        data=data,
        chart_type="bar",
        title="水果销售统计",
        width=600,
        height=400
    )
    
    print(f"生成成功: {result['metadata']}")
    print(f"图表大小: {len(result.get('content', ''))} 字符")
    
    # 保存到文件
    viz.save_chart(result, "fruit_sales.html")
    print("图表已保存到 fruit_sales.html")
    
    return result

def demo_auto_recommendation():
    """自动推荐示例"""
    print("\n=== 自动推荐示例 ===")
    
    # 使用快捷函数
    time_series_data = {
        "dates": ["2026-01", "2026-02", "2026-03", "2026-04"],
        "sales": [100, 150, 120, 180],
        "profit": [60, 90, 70, 110]
    }
    
    result = create_chart(
        data=time_series_data,
        chart_type="auto",  # 自动推荐
        title="销售趋势分析"
    )
    
    print(f"自动推荐的图表类型: {result['metadata'].get('chart_type', '未知')}")
    
    return result

def demo_data_analysis():
    """数据分析示例"""
    print("\n=== 数据分析示例 ===")
    
    viz = EChartsAI()
    
    complex_data = [
        {"category": "A", "value": 30, "group": "X"},
        {"category": "B", "value": 45, "group": "X"},
        {"category": "C", "value": 25, "group": "Y"},
        {"category": "D", "value": 60, "group": "Y"},
        {"category": "E", "value": 35, "group": "Z"},
    ]
    
    # 分析数据
    analysis = viz.analyze_data(complex_data)
    print(f"数据分析结果:")
    print(f"  数据维度: {analysis.get('analysis', {}).get('dimensions', '未知')}")
    print(f"  推荐图表: {analysis.get('recommendations', [])[:3]}")
    
    # 根据分析生成图表
    result = viz.create_chart(
        data=complex_data,
        chart_type="auto",
        title="分组数据可视化"
    )
    
    return result

def demo_dashboard():
    """仪表盘示例"""
    print("\n=== 仪表盘示例 ===")
    
    viz = EChartsAI()
    
    # 多个数据集
    datasets = [
        {
            "categories": ["Q1", "Q2", "Q3", "Q4"],
            "sales": [120, 200, 150, 180],
            "title": "季度销售"
        },
        {
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 6, 8, 10],
            "title": "线性关系"
        },
        {
            "labels": ["产品A", "产品B", "产品C", "产品D"],
            "values": [30, 25, 20, 25],
            "title": "产品占比"
        }
    ]
    
    # 生成仪表盘
    result = viz.generate_dashboard(
        datasets=datasets,
        layout="grid",
        title="业务仪表盘"
    )
    
    print(f"仪表盘包含 {result['metadata'].get('chart_count', 0)} 个图表")
    viz.save_chart(result, "business_dashboard.html")
    print("仪表盘已保存到 business_dashboard.html")
    
    return result

if __name__ == "__main__":
    print("ECharts for AI 示例程序")
    print("=" * 50)
    
    # 运行所有示例
    demo_basic_chart()
    demo_auto_recommendation()
    demo_data_analysis()
    demo_dashboard()
    
    print("\n" + "=" * 50)
    print("所有示例运行完成！")
    print("生成的图表文件:")
    print("  - fruit_sales.html")
    print("  - business_dashboard.html")
