"""Utils module - with real validation"""
class ErrorHandler:
    def handle(self, error):
        return {"error": str(error), "success": False}
    def handle_error(self, error, data=None, chart_type=None):
        return {"error": str(error), "success": False}

class Logger:
    def __init__(self, name=None):
        self.name = name or __name__
    def info(self, msg, *args): pass
    def error(self, msg, *args): pass
    def debug(self, msg, *args): pass
    def warning(self, msg, *args): pass

class Validator:
    def validate(self, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dict")
        return True
    def validate_data(self, data):
        if not isinstance(data, dict):
            raise ValueError("Data must be a dict")
        return True, data
