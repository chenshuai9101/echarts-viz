# ECharts官方文档参考

## 快速开始

### 引入ECharts
```html
<script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>
```

### 基本使用
```javascript
// 准备DOM
<div id="main" style="width: 600px;height:400px;"></div>

// 初始化
var myChart = echarts.init(document.getElementById('main'));

// 配置项
var option = {
    title: { text: '标题' },
    tooltip: {},
    xAxis: { data: ['A', 'B', 'C'] },
    yAxis: {},
    series: [{
        type: 'bar',
        data: [5, 20, 36]
    }]
};

// 设置并渲染
myChart.setOption(option);
```

---

## 图表类型

### 折线图 (line)
```javascript
{
    type: 'line',
    data: [820, 932, 901],
    smooth: true,           // 平滑曲线
    areaStyle: {},          // 面积填充
    symbol: 'circle',       // 数据点标记
    symbolSize: 8           // 标记大小
}
```

### 柱状图 (bar)
```javascript
{
    type: 'bar',
    data: [23, 45, 67],
    barWidth: '50%',        // 柱宽
    itemStyle: {
        borderRadius: [4, 4, 0, 0]  // 圆角
    }
}
```

### 饼图 (pie)
```javascript
{
    type: 'pie',
    radius: ['40%', '70%'], // 环形饼图
    data: [
        { value: 1048, name: '搜索引擎' },
        { value: 735, name: '直接访问' }
    ],
    label: {
        formatter: '{b}: {d}%'
    }
}
```

### 散点图 (scatter)
```javascript
{
    type: 'scatter',
    data: [[3.4, 45.6], [12.3, 67.8]],
    symbolSize: 12
}
```

### 雷达图 (radar)
```javascript
{
    type: 'radar',
    indicator: [
        { name: '销售', max: 6500 },
        { name: '管理', max: 16000 },
        { name: '技术', max: 30000 }
    ],
    data: [{
        value: [4300, 10000, 28000],
        name: '预算分配'
    }]
}
```

---

## 常用配置

### 标题配置
```javascript
title: {
    text: '主标题',
    subtext: '副标题',
    left: 'center',     // left/center/right
    top: 10,
    textStyle: {
        fontSize: 18,
        fontWeight: 'bold'
    }
}
```

### 提示框配置
```javascript
tooltip: {
    trigger: 'axis',    // axis/item
    axisPointer: {
        type: 'cross'   // line/shadow/cross
    },
    formatter: function(params) {
        return params[0].name + '<br/>' +
               params[0].marker + params[0].value;
    }
}
```

### 图例配置
```javascript
legend: {
    data: ['系列1', '系列2'],
    bottom: 0,
    icon: 'circle',    // 标记形状
    itemWidth: 14,
    itemHeight: 14
}
```

### 坐标轴配置
```javascript
xAxis: {
    type: 'category',  // category/value/time/log
    data: ['Mon', 'Tue', 'Wed'],
    axisLabel: {
        rotate: 45,     // 标签旋转
        interval: 0     // 标签间隔
    },
    axisLine: {
        lineStyle: { color: '#999' }
    }
}

yAxis: {
    type: 'value',
    name: '单位',
    nameLocation: 'middle',
    nameGap: 50,
    splitLine: {
        lineStyle: { type: 'dashed' }
    }
}
```

### 颜色配置
```javascript
color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de']
```

---

## 数据格式

### 单系列数据
```javascript
series: [{
    data: [120, 200, 150]
}]
```

### 多系列数据
```javascript
series: [
    { name: '2023', data: [120, 200, 150] },
    { name: '2024', data: [180, 250, 200] }
]
```

### 饼图数据
```javascript
series: [{
    data: [
        { value: 1048, name: '搜索引擎' },
        { value: 735, name: '直接访问' },
        { value: 580, name: '邮件营销' }
    ]
}]
```

### 散点图数据
```javascript
series: [{
    data: [
        [3.4, 45.6],    // [x, y]
        [12.3, 67.8],
        [8.9, 34.2]
    ]
}]
```

---

## 响应式

```javascript
// 监听窗口变化
window.addEventListener('resize', function() {
    myChart.resize();
});

// 或者自动吸附
myChart.setOption(option, true);
```

---

## 导出图片

```javascript
// 获取图片URL
var url = myChart.getDataURL({
    type: 'png',
    pixelRatio: 2,
    backgroundColor: '#fff'
});

// 下载图片
var link = document.createElement('a');
link.download = 'chart.png';
link.href = url;
link.click();
```

---

## 更多资源

- 官网文档：https://echarts.apache.org/zh/option.html
- 示例库：https://echarts.apache.org/examples/zh/
- GitHub：https://github.com/apache/echarts
