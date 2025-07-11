# 📈 股票分析AI Agent系统

> 基于LangGraph框架的智能股票分析系统，支持多模型、多风格分析，具备实时数据获取、历史信息管理和智能提示词编译功能。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.2.0+-green.svg)](https://langchain-ai.github.io/langgraph/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange.svg)](https://openai.com)

## ✨ 核心特性

- 🚀 **LangGraph框架**: 基于LangGraph的状态管理，支持复杂工作流和状态持久化
- 🤖 **多模型支持**: 支持OpenAI GPT系列和DeepSeek模型，灵活切换
- 📊 **实时数据**: 通过yfinance获取实时股票数据和市场信息
- 📈 **多风格分析**: 支持网络效应分析、技术分析、基本面分析等
- 💾 **智能历史管理**: 自动保存和管理历史分析数据，支持趋势分析
- 🔧 **灵活配置**: 支持自定义提示词参数和模板，易于扩展
- 🎯 **精准分析**: 基于新闻事件和财务数据的深度网络效应分析

## 📁 项目结构

```
├── news_agent.py          # 主分析函数文件（LangGraph格式）
├── llm_call.py           # LLM调用模块，支持多模型
├── prompt.py             # 提示词模板文件
├── test_news_agent.py    # 测试示例文件
├── requirements.txt       # 依赖包列表
├── create_env.py         # 环境配置脚本
├── data/                 # 数据存储目录
│   └── stock_history.json # 历史分析数据
└── README.md            # 项目说明文档
```

## 🚀 快速开始

### 1. 环境准备

确保您的系统已安装Python 3.8+，然后克隆项目：

```bash
git clone <repository-url>
cd stock-analysis-agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

创建 `.env` 文件并配置您的API密钥：

```env
# OpenAI配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# DeepSeek配置（可选）
deepseek_API_KEY=your_deepseek_api_key_here
```

### 4. 运行测试

```bash
python test_news_agent.py
```

## 📖 使用指南

### 基础使用

#### 简单分析调用

```python
from news_agent import analyze_stocks_simple

# 基本股票分析
results = analyze_stocks_simple(
    model_name="gpt-4o-mini",
    stock_list=["AAPL", "MSFT"],
    analysis_styles=["network_effect", "network_effect"]
)

for i, result in enumerate(results):
    print(f"📊 {stock_list[i]} 分析结果:")
    print(result)
    print("-" * 50)
```

#### 自定义新闻分析

```python
from news_agent import analyze_stocks_simple

# 使用自定义新闻数据进行分析
custom_news = [
    {
        "news_summary": """2025年7月10日：中国区AI功能删除引发信任危机
        苹果中国官网删除所有"Apple智能（Apple Intelligence）"描述，
        包括iPhone 16系列"为AI预备好"的标注。此前多次跳票，
        因监管审批及技术缺陷导致国行AI功能缺席。"""
    }
]

results = analyze_stocks_simple(
    model_name="gpt-4o-mini",
    stock_list=["AAPL"],
    analysis_styles=["network_effect_analysis"],
    today_info_list=custom_news
)

print("🔍 自定义新闻分析结果:")
print(results[0])
```

### 高级使用

#### 完整状态分析

```python
from news_agent import analyze_stocks_advanced

# 获取完整的分析状态
state = analyze_stocks_advanced(
    model_name="gpt-4o-mini",
    stock_list=["TSLA", "NVDA"],
    analysis_styles=["network_effect", "network_effect"],
    today_info_list=[
        {
            "symbol": "TSLA",
            "shortName": "Tesla, Inc.",
            "marketCap": 800000000000,
            "currentPrice": 250.0,
            "news_summary": "特斯拉发布新款Model S，销量增长强劲"
        },
        None  # 第二个股票使用API获取
    ],
    prompt_params_list=[
        {
            "custom_param": "重点关注电动汽车市场表现",
            "analysis_focus": "技术创新和市场份额"
        },
        None
    ]
)

# 访问完整结果
print("📈 分析结果:", state.analysis_results)
print("📚 历史结果:", state.history_results)
print("🔧 编译的提示词:", state.analysis_prompts)
```

#### LangGraph工作流

```python
from news_agent import create_analysis_workflow, AgentState

# 创建初始状态
initial_state = AgentState(
    model_name="gpt-4o-mini",
    stock_list=["META", "AMZN"],
    analysis_styles=["network_effect", "network_effect"]
)

# 创建并运行工作流
workflow = create_analysis_workflow()
final_state = workflow.invoke(initial_state)

# 获取结果
print("🎯 工作流分析结果:", final_state.analysis_results)
```

## 🔧 API参考

### 核心函数

#### `analyze_stocks_simple()`

简化版分析函数，直接返回分析结果列表。

**参数:**
- `model_name` (str): 模型名称，如 "gpt-4o-mini", "deepseek-chat"
- `stock_list` (List[str]): 股票代码列表，如 ["AAPL", "MSFT"]
- `analysis_styles` (List[str]): 分析风格列表
- `today_info_list` (Optional[List[Optional[Dict]]]): 可选的今日信息列表
- `prompt_params_list` (Optional[List[Optional[Dict]]]): 可选的提示词参数列表
- `date` (Optional[str]): 可选的日期，格式为 "YYYY-MM-DD"

**返回:**
- `List[str]`: 分析结果列表

**示例:**
```python
results = analyze_stocks_simple(
    model_name="gpt-4o-mini",
    stock_list=["AAPL"],
    analysis_styles=["network_effect"],
    date="2024-06-01"
)
```

#### `analyze_stocks_advanced()`

高级分析函数，返回完整的状态对象。

**参数:** 同 `analyze_stocks_simple()`

**返回:**
- `AgentState`: 包含所有分析数据的完整状态对象

### 状态对象 (AgentState)

状态对象包含以下属性：

| 属性 | 类型 | 描述 |
|------|------|------|
| `model_name` | str | 使用的模型名称 |
| `stock_list` | List[str] | 股票代码列表 |
| `analysis_styles` | List[str] | 分析风格列表 |
| `today_info` | List[Dict] | 今日股票信息列表 |
| `history_info` | List[Optional[Dict]] | 历史信息列表 |
| `analysis_prompts` | List[str] | 编译后的分析提示词列表 |
| `history_prompts` | List[str] | 编译后的历史总结提示词列表 |
| `analysis_results` | List[str] | 分析结果列表 |
| `history_results` | List[str] | 历史总结结果列表 |

## 📊 分析风格

系统支持以下分析风格：

### 网络效应分析 (`network_effect`)
- **功能**: 基于新闻事件分析公司的网络效应
- **输出**: 用户增长率、ARPU变化、网络效应强度
- **适用**: 平台型公司、社交网络、电商平台

### 网络效应智能分析 (`network_effect_analysis`)
- **功能**: 智能提取新闻中的网络效应相关信息
- **输出**: JSON格式的结构化分析结果
- **适用**: 需要结构化数据的深度分析

### 历史网络效应分析 (`network_effect_history`)
- **功能**: 结合历史数据和今日新闻进行趋势分析
- **输出**: 网络效应演进情况和当前强度评估
- **适用**: 长期投资决策和趋势分析

## 🛠️ 配置说明

### 环境变量

| 变量名 | 必需 | 描述 | 示例 |
|--------|------|------|------|
| `OPENAI_API_KEY` | 是 | OpenAI API密钥 | sk-... |
| `OPENAI_BASE_URL` | 否 | OpenAI API基础URL | https://api.openai.com/v1 |
| `deepseek_API_KEY` | 否 | DeepSeek API密钥 | sk-... |

### 模型选择建议

| 模型 | 适用场景 | 特点 |
|------|----------|------|
| `gpt-4o-mini` | 一般分析 | 快速、经济、适合批量处理 |
| `gpt-4o` | 复杂分析 | 高质量、适合深度分析 |
| `deepseek-chat` | 中文分析 | 中文理解能力强 |

## 🔍 错误处理

系统具备完善的错误处理机制：

- **API调用失败**: 返回错误信息，不影响其他股票分析
- **数据获取失败**: 使用空数据继续处理，记录错误日志
- **提示词编译失败**: 返回默认错误信息
- **文件操作失败**: 打印详细错误信息，确保数据安全

## 📝 示例运行

### 运行测试示例

```bash
python test_news_agent.py
```

### 自定义测试

```python
# 创建自定义测试文件
from news_agent import analyze_stocks_simple

# 测试自定义新闻分析
custom_news = [
    {
        "news_summary": "您的自定义新闻内容..."
    }
]

results = analyze_stocks_simple(
    model_name="gpt-4o-mini",
    stock_list=["AAPL"],
    analysis_styles=["network_effect_analysis"],
    today_info_list=custom_news
)

print("分析结果:", results[0])
```

## 🚨 注意事项

1. **API密钥安全**: 确保在 `.env` 文件中正确配置API密钥，不要提交到版本控制
2. **网络连接**: 需要稳定的网络连接获取股票数据和调用AI模型
3. **模型选择**: 根据需求选择合适的模型，考虑成本和性能平衡
4. **数据限制**: yfinance API可能有请求频率限制，建议合理控制请求频率
5. **文件权限**: 确保程序有权限创建和写入 `data/` 目录

## 🔧 扩展开发

### 添加新的分析风格

1. 在 `prompt.py` 中添加新的模板：

```python
新分析模板 = """
您的分析模板内容...
"""

PROMPT_TEMPLATES["new_analysis"] = 新分析模板
```

2. 在调用时使用新的模板名称：

```python
results = analyze_stocks_simple(
    model_name="gpt-4o-mini",
    stock_list=["AAPL"],
    analysis_styles=["new_analysis"]
)
```

### 集成其他数据源

可以修改 `fetch_today_info()` 函数来集成其他数据源：

```python
def fetch_today_info(stock_list: List[str], date: Optional[str] = None) -> List[Dict[str, Any]]:
    # 集成Alpha Vantage、IEX Cloud等数据源
    # 返回标准化的数据格式
    pass
```

### 添加新的模型支持

在 `llm_call.py` 中添加新的模型支持：

```python
def _create_client(self):
    if 'your_model' in self.model_name.lower():
        # 添加新模型的配置
        pass
```

## 📞 支持与反馈

如果您在使用过程中遇到问题或有改进建议，欢迎：

- 📧 提交Issue
- 💬 参与讨论
- ⭐ 给项目点赞

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

**🎯 让AI为您的投资决策提供智能支持！** 