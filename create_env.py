def create_env_file():
    content = """# OpenAI API配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
# deepseekAPI配置
deepseek_API_KEY = 'sk-4e63e2e8dd6f4d54a0dfc6a05d565325'

# 历史信息文件路径
STOCK_HISTORY_FILE=data/stock_history.json
ANALYSIS_RESULTS_FILE=data/analysis_results.json
ANALYSIS_HISTORY_FILE=data/analysis_history.json
"""
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(content)
    print(".env 文件已创建！")

if __name__ == "__main__":
    create_env_file() 