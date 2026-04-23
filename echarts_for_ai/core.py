"""
ECharts for AI 核心接口
提供统一的API供AI Agent调用
"""

import json
import time
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

from .engines import EngineFactory
from .analyzers import DataAnalyzer, ChartRecommender
from .optimizers import CacheManager, PerformanceOptimizer
from .utils import ErrorHandler, Logger, Validator


class ChartType(Enum):
    """图表类型枚举"""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    SCATTER = "scatter"
    HEATMAP = "heatmap"
    RADAR = "radar"
    CANDLESTICK = "candlestick"
    BOXPLOT = "boxplot"
    HISTOGRAM = "histogram"
    AREA = "area"
    WATERFALL = "waterfall"
    DASHBOARD = "dashboard"
    AUTO = "auto"  # 自动推荐


class OutputFormat(Enum):
    """输出格式枚举"""
    HTML = "html"
    PNG = "png"
    SVG = "svg"
    JSON = "json"
    BASE64 = "base64"


class Theme(Enum):
    """主题风格枚举"""
    BUSINESS = "business"
    TECHNICAL = "technical"
    ACADEMIC = "academic"
    MINIMAL = "minimal"
    DARK = "dark"
    CUSTOM = "custom"


@dataclass
class ChartConfig:
    """图表配置"""
    chart_type: ChartType = ChartType.AUTO
    title: str = ""
    width: int = 800
    height: int = 600
    theme: Theme = Theme.BUSINESS
    output_format: OutputFormat = OutputFormat.HTML
    interactive: bool = True
    responsive: bool = True
    show_legend: bool = True
    show_tooltip: bool = True
    animation: bool = True
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "chart_type": self.chart_type.value,
            "title": self.title,
            "width": self.width,
            "height": self.height,
            "theme": self.theme.value,
            "output_format": self.output_format.value,
            "interactive": self.interactive,
            "responsive": self.responsive,
            "show_legend": self.show_legend,
            "show_tooltip": self.show_tooltip,
            "animation": self.animation,
        }


class EChartsAI:
    """ECharts for AI 主类"""
    
    def __init__(self, config: Optional[Dict] = None):
        """
        初始化EChartsAI
        
        Args:
            config: 配置字典
        """
        self.config = self._merge_config(config or {})
        self.logger = Logger(__name__)
        self.validator = Validator()
        self.error_handler = ErrorHandler()
        self.cache_manager = CacheManager(self.config.get("cache_size", 100))
        self.performance_optimizer = PerformanceOptimizer()
        self.data_analyzer = DataAnalyzer()
        self.chart_recommender = ChartRecommender()
        self.engine_factory = EngineFactory()
        
        self.logger.info(f"EChartsAI initialized with config: {self.config}")
    
    def _merge_config(self, user_config: Dict) -> Dict:
        """合并默认配置和用户配置"""
        default_config = {
            "default_engine": "echarts",
            "enable_cache": True,
            "cache_size": 100,
            "timeout": 30,
            "output_format": "html",
            "theme": "business",
            "responsive": True,
            "debug": False,
        }
        
        # 合并配置
        merged = default_config.copy()
        merged.update(user_config)
        return merged
    
    def create_chart(
        self,
        data: Union[Dict, List, str],
        chart_type: Union[str, ChartType] = "auto",
        title: str = "",
        config: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """
        创建图表
        
        Args:
            data: 输入数据
            chart_type: 图表类型
            title: 图表标题
            config: 额外配置
            **kwargs: 其他参数
            
        Returns:
            包含图表结果和元数据的字典
        """
        start_time = time.time()
        
        try:
            # 验证输入
            self.validator.validate_data(data)
            
            # 合并配置
            chart_config = self._prepare_chart_config(chart_type, title, config, kwargs)
            
            # 分析数据
            analysis = self.data_analyzer.analyze(data)
            
            # 推荐图表类型（如果是auto）
            if chart_config.chart_type == ChartType.AUTO:
                recommended = self.chart_recommender.recommend(analysis, chart_config)
                chart_config.chart_type = recommended
                self.logger.info(f"Auto recommended chart type: {recommended.value}")
            
            # 检查缓存
            cache_key = self._generate_cache_key(data, chart_config)
            if self.config["enable_cache"]:
                cached = self.cache_manager.get(cache_key)
                if cached:
                    self.logger.info("Cache hit")
                    return self._format_result(cached, start_time, from_cache=True)
            
            # 选择引擎
            engine = self.engine_factory.get_engine(
                chart_config.chart_type,
                chart_config.output_format,
                self.config
            )
            
            # 性能优化
            optimized_data = self.performance_optimizer.optimize_data(data, analysis)
            
            # 生成图表
            chart_result = engine.render(
                data=optimized_data,
                config=chart_config.to_dict(),
                analysis=analysis
            )
            
            # 缓存结果
            if self.config["enable_cache"]:
                self.cache_manager.set(cache_key, chart_result)
            
            # 格式化结果
            result = self._format_result(chart_result, start_time)
            
            self.logger.info(f"Chart created successfully: {result['metadata']}")
            return result
            
        except Exception as e:
            error_result = self.error_handler.handle_error(e, data, chart_type)
            self.logger.error(f"Error creating chart: {str(e)}")
            return error_result
    
    def generate_dashboard(
        self,
        datasets: List[Dict],
        layout: str = "grid",
        title: str = "Dashboard",
        config: Optional[Dict] = None,
        **kwargs
    ) -> Dict:
        """
        生成仪表盘
        
        Args:
            datasets: 多个数据集
            layout: 布局方式 (grid, row, column, custom)
            title: 仪表盘标题
            config: 配置
            **kwargs: 其他参数
            
        Returns:
            仪表盘结果
        """
        start_time = time.time()
        
        try:
            # 验证所有数据集
            for i, data in enumerate(datasets):
                self.validator.validate_data(data)
            
            # 准备配置
            dashboard_config = {
                "layout": layout,
                "title": title,
                "charts": [],
                **(config or {}),
                **kwargs
            }
            
            # 并行生成所有图表
            charts = []
            for i, data in enumerate(datasets):
                chart_config = {
                    "title": f"Chart {i+1}",
                    "width": 400 if layout == "grid" else 800,
                    "height": 300,
                    **(config or {}),
                }
                
                chart_result = self.create_chart(
                    data=data,
                    chart_type="auto",
                    config=chart_config
                )
                charts.append(chart_result)
            
            # 组合仪表盘
            dashboard_result = {
                "type": "dashboard",
                "layout": layout,
                "title": title,
                "charts": charts,
                "html": self._combine_dashboard_html(charts, layout),
                "metadata": {
                    "chart_count": len(charts),
                    "layout": layout,
                }
            }
            
            result = self._format_result(dashboard_result, start_time)
            self.logger.info(f"Dashboard generated with {len(charts)} charts")
            return result
            
        except Exception as e:
            error_result = self.error_handler.handle_error(e, datasets, "dashboard")
            self.logger.error(f"Error generating dashboard: {str(e)}")
            return error_result
    
    def analyze_data(self, data: Any) -> Dict:
        """
        分析数据特征
        
        Args:
            data: 输入数据
            
        Returns:
            数据分析结果
        """
        try:
            analysis = self.data_analyzer.analyze(data)
            return {
                "success": True,
                "analysis": analysis,
                "recommendations": self.chart_recommender.get_recommendations(analysis),
                "insights": self.data_analyzer.get_insights(analysis),
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "analysis": {},
            }
    
    def batch_process(
        self,
        datasets: List[Any],
        chart_types: Optional[List[Union[str, ChartType]]] = None,
        parallel: bool = True,
        **kwargs
    ) -> List[Dict]:
        """
        批量处理多个数据集
        
        Args:
            datasets: 数据集列表
            chart_types: 图表类型列表（可选）
            parallel: 是否并行处理
            **kwargs: 其他参数
            
        Returns:
            处理结果列表
        """
        results = []
        
        if parallel and len(datasets) > 1:
            # 简单并行处理（实际实现可能需要线程池）
            for i, data in enumerate(datasets):
                chart_type = chart_types[i] if chart_types and i < len(chart_types) else "auto"
                result = self.create_chart(data, chart_type=chart_type, **kwargs)
                results.append(result)
        else:
            # 串行处理
            for i, data in enumerate(datasets):
                chart_type = chart_types[i] if chart_types and i < len(chart_types) else "auto"
                result = self.create_chart(data, chart_type=chart_type, **kwargs)
                results.append(result)
        
        return results
    
    def save_chart(self, result: Dict, filepath: str) -> bool:
        """
        保存图表到文件
        
        Args:
            result: 图表结果
            filepath: 文件路径
            
        Returns:
            是否保存成功
        """
        try:
            content = result.get("content", "")
            if not content:
                self.logger.warning("No content to save")
                return False
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.logger.info(f"Chart saved to {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving chart: {str(e)}")
            return False
    
    def _prepare_chart_config(
        self,
        chart_type: Union[str, ChartType],
        title: str,
        config: Optional[Dict],
        kwargs: Dict
    ) -> ChartConfig:
        """准备图表配置"""
        # 合并所有配置
        merged_config = {
            "chart_type": chart_type,
            "title": title,
            **(config or {}),
            **kwargs,
        }
        
        # 创建ChartConfig对象
        chart_config = ChartConfig()
        
        # 更新配置
        for key, value in merged_config.items():
            if hasattr(chart_config, key):
                # 处理枚举类型
                if key == "chart_type":
                    if isinstance(value, ChartType):
                        setattr(chart_config, key, value)
                    else:
                        setattr(chart_config, key, ChartType(value))
                elif key == "theme":
                    if isinstance(value, Theme):
                        setattr(chart_config, key, value)
                    else:
                        setattr(chart_config, key, Theme(value))
                elif key == "output_format":
                    if isinstance(value, OutputFormat):
                        setattr(chart_config, key, value)
                    else:
                        setattr(chart_config, key, OutputFormat(value))
                else:
                    setattr(chart_config, key, value)
        
        return chart_config
    
    def _generate_cache_key(self, data: Any, config: ChartConfig) -> str:
        """生成缓存键"""
        import hashlib
        
        # 将数据和配置序列化为字符串
        data_str = json.dumps(data, sort_keys=True) if isinstance(data, (dict, list)) else str(data)
        config_str = json.dumps(config.to_dict(), sort_keys=True)
        
        # 计算哈希
        key_str = f"{data_str}|{config_str}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _format_result(self, result: Any, start_time: float, from_cache: bool = False) -> Dict:
        """格式化结果"""
        processing_time = time.time() - start_time
        
        metadata = {
            "processing_time_ms": round(processing_time * 1000, 2),
            "from_cache": from_cache,
            "timestamp": time.time(),
            "version": "2.0.0",
        }
        
        if isinstance(result, dict):
            if "metadata" in result:
                result["metadata"].update(metadata)
            else:
                result["metadata"] = metadata
            return result
        else:
            return {
                "content": result,
                "metadata": metadata,
                "success": True,
            }
    
    def _combine_dashboard_html(self, charts: List[Dict], layout: str) -> str:
        """组合仪表盘HTML"""
        if layout == "grid":
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>ECharts Dashboard</title>
                <style>
                    .dashboard {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                        gap: 20px;
                        padding: 20px;
                    }
                    .chart-container {
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 15px;
                        background: white;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }
                </style>
            </head>
            <body>
                <div class="dashboard">
            """
            
            for chart in charts:
                chart_html = chart.get("content", chart.get("html", ""))
                html += f'<div class="chart-container">{chart_html}</div>'
            
            html += """
                </div>
            </body>
            </html>
            """
        else:
            # 简单行布局
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>ECharts Dashboard</title>
                <style>
                    .dashboard {
                        padding: 20px;
                    }
                    .chart-container {
                        margin-bottom: 30px;
                        border: 1px solid #e0e0e0;
                        border-radius: 8px;
                        padding: 15px;
                        background: white;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    }
                </style>
            </head>
            <body>
                <div class="dashboard">
            """
            
            for chart in charts:
                chart_html = chart.get("content", chart.get("html", ""))
                html += f'<div class="chart-container">{chart_html}</div>'
            
            html += """
                </div>
            </body>
            </html>
            """
        
        return html
    
    def __repr__(self):
        return f"EChartsAI(config={self.config})"