"""
工具模块 - 通用工具函数
"""

class Logger:
    """简单日志器"""
    def __init__(self, name):
        self.name = name
    
    def info(self, msg):
        print(f"[INFO] {self.name}: {msg}")
    
    def error(self, msg):
        print(f"[ERROR] {self.name}: {msg}")
    
    def warning(self, msg):
        print(f"[WARNING] {self.name}: {msg}")


class Validator:
    """数据验证器"""
    def validate_data(self, data):
        """验证数据（简化版）"""
        if data is None:
            raise ValueError("数据不能为空")
        return True


class ErrorHandler:
    """错误处理器"""
    def handle_error(self, error, data, chart_type):
        """处理错误"""
        return {
            "success": False,
            "error": str(error),
            "data_type": type(data).__name__,
            "chart_type": chart_type,
            "message": "图表生成失败，请检查数据和配置"
        }
