# 股票分析AI Agent系统

基于LangGraph框架的股票分析系统，支持多模型、多风格分析，具备实时数据获取、历史信息管理和智能提示词编译功能。

## 功能特性

- 🚀 **LangGraph框架**: 基于LangGraph的状态管理，支持复杂工作流
- 🤖 **多模型支持**: 支持OpenAI GPT系列和DeepSeek模型
- 📊 **实时数据**: 通过yfinance获取实时股票数据
- 📈 **多风格分析**: 支持技术分析、基本面分析、网络效应分析等
- 💾 **历史管理**: 自动保存和管理历史分析数据
- 🔧 **灵活配置**: 支持自定义提示词参数和模板

## 文件结构

```
├── news_agent.py          # 主分析函数文件（LangGraph格式）
├── llm_call.py           # LLM调用模块
├── prompt.py             # 提示词模板文件
├── config.py             # 配置文件
├── example_usage.py      # 使用示例
└── README.md            # 说明文档
```

## 快速开始

### 1. 环境配置

确保已安装必要的依赖：

```bash
pip install langgraph openai yfinance python-dotenv
```

### 2. 配置API密钥

在项目根目录创建 `.env` 文件：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai-proxy.org/v1
deepseek_API_KEY=your_deepseek_api_key_here
```

### 3. 基本使用

#### 简单调用

```python
from news_agent import analyze_stocks_simple

# 基本分析
results = analyze_stocks_simple(
    model_name="gpt-4o-mini",
    stock_list=["AAPL", "MSFT"],
    analysis_styles=["network_effect", "network_effect"]
)

for i, result in enumerate(results):
    print(f"股票 {stock_list[i]} 分析结果:")
    print(result)
```

#### 高级调用

```python
from news_agent import analyze_stocks_advanced

# 自定义参数的高级分析
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
print("分析结果:", state.analysis_results)
print("历史结果:", state.history_results)
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
print("分析结果:", final_state.analysis_results)
```

## API参考

### 主要函数

#### `analyze_stocks_simple()`

简化版分析函数，直接返回分析结果列表。

**参数:**
- `model_name` (str): 模型名称，如 "gpt-4o-mini"
- `stock_list` (List[str]): 股票代码列表
- `analysis_styles` (List[str]): 分析风格列表
- `today_info_list` (Optional[List[Optional[Dict]]]): 可选的今日信息列表
- `prompt_params_list` (Optional[List[Optional[Dict]]]): 可选的提示词参数列表

**返回:**
- `List[str]`: 分析结果列表

#### `analyze_stocks_advanced()`

高级分析函数，返回完整的状态对象。

**参数:** 同 `analyze_stocks_simple()`

**返回:**
- `AgentState`: 包含所有分析数据的完整状态对象

#### `create_analysis_workflow()`

创建LangGraph工作流。

**返回:**
- `StateGraph`: 编译后的工作流对象

### 状态对象 (AgentState)

状态对象包含以下属性：

- `model_name`: 模型名称
- `stock_list`: 股票代码列表
- `analysis_styles`: 分析风格列表
- `today_info`: 今日股票信息列表
- `history_info`: 历史信息列表
- `analysis_prompts`: 编译后的分析提示词列表
- `history_prompts`: 编译后的历史总结提示词列表
- `analysis_results`: 分析结果列表
- `history_results`: 历史总结结果列表

## 分析风格

系统支持以下分析风格（模板名称）：

- `network_effect`: 网络效应分析
- `network_effect_analysis`: 网络效应智能分析
- `network_effect_history`: 历史网络效应分析

## 错误处理

系统具备完善的错误处理机制：

- API调用失败时会返回错误信息
- 股票数据获取失败时会使用空数据继续处理
- 提示词编译失败时会返回默认错误信息
- 文件操作失败时会打印错误信息

## 示例运行

运行示例文件查看完整的使用方法：

```bash
python example_usage.py
```

## 注意事项

1. **API密钥**: 确保在 `.env` 文件中正确配置API密钥
2. **网络连接**: 需要稳定的网络连接获取股票数据
3. **模型选择**: 根据需求选择合适的模型，GPT-4o-mini适合一般分析，GPT-4o适合复杂分析
4. **数据限制**: yfinance API可能有请求频率限制
5. **文件权限**: 确保程序有权限创建和写入 `data/` 目录

## 扩展开发

### 添加新的分析风格

1. 在 `prompt.py` 中添加新的模板
2. 在 `PROMPT_TEMPLATES` 字典中注册模板
3. 在调用时使用新的模板名称

### 自定义数据源

可以修改 `fetch_today_info()` 函数来集成其他数据源，如：
- Alpha Vantage API
- IEX Cloud API
- 自定义数据源

### 集成其他模型

在 `llm_call.py` 中添加新的模型支持，遵循现有的模式。 