"""
基础测试
"""

import pytest
from echarts_for_ai import EChartsAI

class TestEChartsAI:
    """EChartsAI测试类"""
    
    def setup_method(self):
        """测试设置"""
        self.viz = EChartsAI()
        self.sample_data = {
            "categories": ["A", "B", "C", "D"],
            "values": [10, 20, 30, 40]
        }
    
    def test_initialization(self):
        """测试初始化"""
        assert self.viz is not None
        assert hasattr(self.viz, 'create_chart')
        assert hasattr(self.viz, 'generate_dashboard')
    
    def test_create_chart_basic(self):
        """测试基础图表创建"""
        result = self.viz.create_chart(
            data=self.sample_data,
            chart_type="bar",
            title="测试图表"
        )
        
        assert result["success"] is True
        assert "content" in result or "html" in result
        assert "metadata" in result
        assert result["metadata"]["processing_time_ms"] > 0
    
    def test_auto_chart_recommendation(self):
        """测试自动图表推荐"""
        result = self.viz.create_chart(
            data=self.sample_data,
            chart_type="auto"
        )
        
        assert result["success"] is True
    
    def test_data_analysis(self):
        """测试数据分析"""
        analysis = self.viz.analyze_data(self.sample_data)
        assert analysis["success"] is True
        assert "analysis" in analysis
    
    def test_error_handling(self):
        """测试错误处理"""
        # 测试无效数据
        result = self.viz.create_chart(
            data="invalid data",
            chart_type="bar"
        )
        
        # 错误时应该返回错误信息
        assert "error" in result or result.get("success") is False
    
    def test_batch_processing(self):
        """测试批量处理"""
        datasets = [self.sample_data, self.sample_data]
        results = self.viz.batch_process(datasets, parallel=False)
        
        assert len(results) == 2
        for result in results:
            assert result["success"] is True

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
