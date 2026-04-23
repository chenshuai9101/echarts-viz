"""
引擎工厂 - 根据需求创建合适的渲染引擎
"""

from typing import Dict, Any, Optional
from enum import Enum


class EngineType(Enum):
    """引擎类型枚举"""
    ECHARTS = "echarts"
    MATPLOTLIB = "matplotlib"
    D3 = "d3"
    MERMAID = "mermaid"
    PLAYWRIGHT = "playwright"
    HTML = "html"  # 基础HTML降级


class EngineFactory:
    """引擎工厂类"""
    
    def __init__(self):
        self.engines = {}
        self._register_default_engines()
    
    def _register_default_engines(self):
        """注册默认引擎"""
        # 这里会注册实际引擎，目前是占位
        pass
    
    def get_engine(self, chart_type, output_format, config: Dict) -> Any:
        """
        获取合适的引擎
        
        Args:
            chart_type: 图表类型
            output_format: 输出格式
            config: 配置
            
        Returns:
            引擎实例
        """
        # 简单的引擎选择逻辑
        if output_format == "html":
            return self._create_html_engine()
        else:
            return self._create_fallback_engine()
    
    def _create_html_engine(self):
        """创建HTML引擎（占位）"""
        class HtmlEngine:
            def render(self, data, config, analysis):
                return "<div>HTML Chart Placeholder</div>"
        return HtmlEngine()
    
    def _create_fallback_engine(self):
        """创建降级引擎（占位）"""
        class FallbackEngine:
            def render(self, data, config, analysis):
                return {
                    "type": "fallback",
                    "message": "Fallback engine - actual implementation needed",
                    "data": str(data)[:100]
                }
        return FallbackEngine()
    
    def register_engine(self, name: str, engine_class):
        """注册新引擎"""
        self.engines[name] = engine_class
    
    def list_engines(self):
        """列出所有可用引擎"""
        return list(self.engines.keys())
