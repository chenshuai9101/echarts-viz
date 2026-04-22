# ECharts Viz - 数据可视化Skill

> 将数据转化为专业图表的AI Agent技能

## 简介

`echarts-viz` 是一个为AI Agent打造的数据可视化技能，能够将结构化数据自动转换为专业的ECharts图表。支持折线图、柱状图、饼图、散点图、雷达图等多种图表类型，自动适配数据格式并生成高质量可视化输出。

## 特性

- 🎯 **智能图表推荐**：根据数据特征自动推荐最适合的图表类型
- 📊 **多图表支持**：折线图、柱状图、饼图、散点图、雷达图、热力图
- 🔄 **多数据格式**：支持JSON、CSV、表格文本等多种数据输入
- 🎨 **专业样式**：内置商务、科技、信息图等多种配色方案
- 📱 **响应式设计**：自动适配不同屏幕尺寸
- 🌐 **免费开源**：基于Apache 2.0协议，完全免费可商用

## 快速开始

### 在扣子(Coze)中使用

1. 访问 [扣子技能商店](https://www.coze.cn/skills)
2. 搜索 `echarts-viz` 或从GitHub导入
3. 在Agent中调用技能

### 基本使用

```
用户：请生成一个展示月度销售额的柱状图
数据：[{"月份":"1月","销售额":120000},{"月份":"2月","销售额":135000}]
```

### 图表类型指定

```
用户：生成2024年Q1-Q4收入对比的柱状图
```

## 项目结构

```
echarts-viz/
├── SKILL.md                    # 技能主文件
├── scripts/
│   ├── generate_chart.py       # 图表生成核心脚本
│   ├── data_parser.py         # 数据解析工具
│   └── chart_templates.py     # 图表模板库
├── references/
│   └── echarts-guide.md       # ECharts官方文档参考
└── assets/
    ├── template-bar.html      # 柱状图模板
    └── template-pie.html      # 饼图模板
```

## 技术栈

- **图表库**：ECharts 5.4.3
- **语言**：Python 3.x
- **协议**：Apache 2.0

## 图表类型

| 图表类型 | 适用场景 |
|---------|---------|
| 折线图 | 时间序列、趋势展示 |
| 柱状图 | 分类对比、数量统计 |
| 饼图 | 占比分析、比例展示 |
| 散点图 | 关联分析、分布展示 |
| 雷达图 | 多维对比、能力评估 |
| 热力图 | 密度展示、矩阵数据 |

## 配色方案

| 主题 | 说明 |
|------|------|
| default | 默认蓝色商务风格 |
| light | 浅色清新风格 |
| dark | 深色科技风格 |
| infographic | 信息图表风格 |
| business | 商务专业风格 |
| nature | 自然绿色风格 |

## 使用示例

### Python脚本使用

```python
from scripts.generate_chart import generate_html, detect_chart_type, extract_chart_config

# 示例数据
data = [
    {"月份": "1月", "销售额": 120000},
    {"月份": "2月", "销售额": 135000},
    {"月份": "3月", "销售额": 128000}
]

# 检测图表类型
chart_type = detect_chart_type(data, "月度销售额趋势")['chart_type']

# 生成配置
config = extract_chart_config(data, chart_type, title="月度销售额")

# 生成HTML
html = generate_html(config)

# 保存
with open('chart.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## 开发

### 本地测试

```bash
cd scripts
python generate_chart.py
```

### 依赖

- Python 3.7+
- echarts (通过CDN引入)

## 贡献

欢迎提交Issue和Pull Request！

## 许可

本项目采用 Apache 2.0 许可证。

## 相关资源

- [ECharts官网](https://echarts.apache.org/)
- [ECharts文档](https://echarts.apache.org/zh/option.html)
- [ECharts示例](https://echarts.apache.org/examples/zh/)

---

**由 Skill工厂·牧云野店 提供**
