"""
ECharts for AI - 专业的AI Agent数据可视化库

版本: 2.0.0
作者: Skill工厂·牧云野店
许可证: MIT/Commercial
"""

__version__ = "2.0.0"
__author__ = "Skill工厂·牧云野店"
__license__ = "MIT/Commercial"

from .core import EChartsAI
from .engines import (
    EChartsEngine,
    MatplotlibEngine,
    D3Engine,
    MermaidEngine,
    PlaywrightEngine
)
from .analyzers import DataAnalyzer, ChartRecommender
from .optimizers import CacheManager, PerformanceOptimizer
from .utils import ErrorHandler, Logger, Validator

__all__ = [
    "EChartsAI",
    "EChartsEngine",
    "MatplotlibEngine",
    "D3Engine",
    "MermaidEngine",
    "PlaywrightEngine",
    "DataAnalyzer",
    "ChartRecommender",
    "CacheManager",
    "PerformanceOptimizer",
    "ErrorHandler",
    "Logger",
    "Validator",
]

# 初始化默认配置
DEFAULT_CONFIG = {
    "default_engine": "echarts",
    "enable_cache": True,
    "cache_size": 100,
    "timeout": 30,
    "output_format": "html",
    "theme": "business",
    "responsive": True,
}

def get_version():
    """获取当前版本号"""
    return __version__

def create_viz(config=None):
    """
    快速创建可视化实例
    
    Args:
        config: 配置字典，可选
        
    Returns:
        EChartsAI实例
    """
    from .core import EChartsAI
    return EChartsAI(config=config)

# 导出快捷函数
create_chart = lambda data, **kwargs: create_viz().create_chart(data, **kwargs)
generate_dashboard = lambda data, **kwargs: create_viz().generate_dashboard(data, **kwargs)
analyze_data = lambda data, **kwargs: create_viz().analyze_data(data, **kwargs)