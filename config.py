import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置类，用于管理API密钥和其他配置"""
    
    # OpenAI配置
    OPENAI_API_KEY = 'sk-FMYDZNnHzaFzA11Z1yCH74yBE3yUbcZE6UPmxXJz2kX60WbY'
    OPENAI_BASE_URL = 'https://api.openai-proxy.org/v1'
    
    # 其他API配置
    deepseek_API_KEY = 'sk-4e63e2e8dd6f4d54a0dfc6a05d565325'

    YAHOO_FINANCE_API_KEY = os.getenv('YAHOO_FINANCE_API_KEY', 'your_yahoo_finance_api_key_here')
    
    # 文件路径配置
    STOCK_HISTORY_FILE = "data/stock_history.json"
    ANALYSIS_RESULTS_FILE = "data/analysis_results.json"
    PROMPT_TEMPLATES_DIR = "prompts/"
    
    # 分析风格配置
    ANALYSIS_STYLES = {
        "technical": "技术分析",
        "fundamental": "基本面分析", 
        "sentiment": "情绪分析",
        "momentum": "动量分析",
        "value": "价值分析"
    } 