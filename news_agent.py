# news_agent.py - LangGraph格式的股票分析函数
import yfinance as yf
import json
import os
from datetime import datetime
from llm_call import create_agent_call
from prompt import format_prompt
from typing import List, Optional, Dict, Any
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# 定义状态类型
class AgentState(BaseModel):
    """LangGraph状态类，包含所有分析所需的数据"""
    model_name: str
    stock_list: List[str]
    analysis_styles: List[str]
    today_info_list: Optional[List[Optional[Dict]]] = None
    prompt_params_list: Optional[List[Optional[Dict]]] = None
    date: Optional[str] = None
    today_info: Optional[List[Dict]] = None
    history_info: Optional[List[Optional[str]]] = None
    analysis_prompts: Optional[List[str]] = None
    history_prompts: Optional[List[str]] = None
    analysis_results: Optional[List[str]] = None
    history_results: Optional[List[str]] = None

def fetch_today_info(stock_list: List[str], date: Optional[str] = None) -> List[Dict[str, Any]]:
    today_info = []
    for symbol in stock_list:
        try:
            ticker = yf.Ticker(symbol)
            if date is None or date == datetime.now().strftime('%Y-%m-%d'):
                info = ticker.info
            else:
                # 获取指定日期的历史数据
                hist = ticker.history(start=date, end=date)
                if not hist.empty:
                    row = hist.iloc[0]
                    info = {
                        "symbol": symbol,
                        "date": date,
                        "close": row["Close"],
                        "open": row["Open"],
                        "high": row["High"],
                        "low": row["Low"],
                        "volume": row["Volume"]
                    }
                else:
                    info = {"symbol": symbol, "date": date, "error": "无该日数据"}
            today_info.append(info)
        except Exception as e:
            today_info.append({"symbol": symbol, "date": date, "error": str(e)})
    return today_info

def fetch_history(stock_list: List[str], history_file: str = 'data/stock_history.json') -> List[Optional[Dict]]:
    """获取历史信息"""
    if not os.path.exists(history_file):
        history_data = {}
    else:
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        except Exception as e:
            print(f"读取历史文件失败: {e}")
            history_data = {}
    
    history_list = [history_data.get(symbol) for symbol in stock_list]
    return history_list

def compile_analysis_prompts(
    today_info: List[Dict], 
    history_info: List[Optional[Dict]], 
    analysis_styles: List[str], 
    prompt_params_list: Optional[List[Optional[Dict]]] = None
) -> List[str]:
    """编译分析提示词"""
    prompts = []
    for i, info in enumerate(today_info):
        style = analysis_styles[i] if i < len(analysis_styles) else 'network_effect'
        params = info.copy()  # 使用copy避免修改原始数据
        params['history_info'] = history_info[i] or ""
        
        if prompt_params_list and i < len(prompt_params_list) and prompt_params_list[i]:
            params.update(prompt_params_list[i])
        
        try:
            prompt = format_prompt(style, **params)
            prompts.append(prompt)
        except Exception as e:
            print(f"编译提示词失败: {e}")
            prompts.append("分析失败")
    
    return prompts

def compile_history_prompts(
    today_info: List[Dict], 
    history_info: List[Optional[Dict]]
) -> List[str]:
    """编译历史总结提示词"""
    prompts = []
    for i, info in enumerate(today_info):
        try:
            prompt = format_prompt('network_effect_history', **info, history_info=history_info[i] or "")
            prompts.append(prompt)
        except Exception as e:
            print(f"编译历史提示词失败: {e}")
            prompts.append("历史总结失败")
    return prompts

def update_history(
    stock_list: List[str], 
    history_results: List[str], 
    history_file: str = 'data/stock_history.json'
) -> None:
    """更新历史信息文件"""
    try:
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        else:
            history_data = {}
        
        for i, symbol in enumerate(stock_list):
            history_data[symbol] = history_results[i]
        
        # 确保目录存在
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"更新历史文件失败: {e}")

# LangGraph节点函数
def prepare_data(state: AgentState) -> AgentState:
    """准备数据节点"""
    stock_list = state.stock_list
    today_info_list = state.today_info_list
    date = state.date
    
    # 获取今日信息
    if today_info_list is None:
        today_info = fetch_today_info(stock_list, date)
    else:
        today_info = []
        for i, symbol in enumerate(stock_list):
            if today_info_list[i] is not None:
                today_info.append(today_info_list[i])
            else:
                info = fetch_today_info([symbol], date)[0]
                today_info.append(info)
    
    # 获取历史信息
    history_info = fetch_history(stock_list)
    
    # 更新状态
    state.today_info = today_info
    state.history_info = history_info
    return state

def compile_prompts(state: AgentState) -> AgentState:
    """编译提示词节点"""
    analysis_styles = state.analysis_styles
    prompt_params_list = state.prompt_params_list
    
    # 编译分析提示词
    analysis_prompts = compile_analysis_prompts(
        state.today_info, 
        state.history_info, 
        analysis_styles,
        prompt_params_list
    )
    
    # 编译历史总结提示词
    history_prompts = compile_history_prompts(state.today_info, state.history_info)
    
    # 更新状态
    state.analysis_prompts = analysis_prompts
    state.history_prompts = history_prompts
    return state

def analyze_stocks(state: AgentState) -> AgentState:
    """分析股票节点"""
    model_name = state.model_name
    agent = create_agent_call(model_name)
    
    # 进行今日分析
    analysis_results = agent.infomation_prompts_analysis(state.analysis_prompts)
    
    # 进行历史总结
    history_results = agent.history_prompts_analysis(state.history_prompts)
    
    # 更新状态
    state.analysis_results = analysis_results
    state.history_results = history_results
    return state

def save_results(state: AgentState) -> AgentState:
    """保存结果节点"""
    update_history(state.stock_list, state.history_results)
    return state

# 创建LangGraph工作流
def create_analysis_workflow() -> StateGraph:
    """创建分析工作流"""
    workflow = StateGraph(AgentState)
    
    # 添加节点
    workflow.add_node("prepare_data", prepare_data)
    workflow.add_node("compile_prompts", compile_prompts)
    workflow.add_node("analyze_stocks", analyze_stocks)
    workflow.add_node("save_results", save_results)
    
    # 设置流程
    workflow.set_entry_point("prepare_data")
    workflow.add_edge("prepare_data", "compile_prompts")
    workflow.add_edge("compile_prompts", "analyze_stocks")
    workflow.add_edge("analyze_stocks", "save_results")
    workflow.add_edge("save_results", END)
    
    return workflow.compile()

# 便捷函数，用于外部直接调用
def analyze_stocks_simple(
    model_name: str,
    stock_list: List[str],
    analysis_styles: List[str],
    today_info_list: Optional[List[Optional[Dict]]] = None,
    prompt_params_list: Optional[List[Optional[Dict]]] = None,
    date: Optional[str] = None
) -> List[str]:
    """
    简化的分析函数，用于外部直接调用
    
    Args:
        model_name: 模型名称
        stock_list: 股票代码列表
        analysis_styles: 分析风格列表
        today_info_list: 可选的今日信息列表
        prompt_params_list: 可选的提示词参数列表
        date: 可选的日期，用于指定获取哪一天的数据
    
    Returns:
        分析结果列表
    """
    # 创建初始状态
    initial_state = AgentState(
        model_name=model_name,
        stock_list=stock_list,
        analysis_styles=analysis_styles,
        today_info_list=today_info_list,
        prompt_params_list=prompt_params_list,
        date=date
    )
    
    # 创建并运行工作流
    workflow = create_analysis_workflow()
    final_state = workflow.invoke(initial_state)
    
    return final_state["analysis_results"]

# 高级函数，返回完整状态
def analyze_stocks_advanced(
    model_name: str,
    stock_list: List[str],
    analysis_styles: List[str],
    today_info_list: Optional[List[Optional[Dict]]] = None,
    prompt_params_list: Optional[List[Optional[Dict]]] = None,
    date: Optional[str] = None
) -> AgentState:
    """
    高级分析函数，返回完整状态对象
    
    Args:
        model_name: 模型名称
        stock_list: 股票代码列表
        analysis_styles: 分析风格列表
        today_info_list: 可选的今日信息列表
        prompt_params_list: 可选的提示词参数列表
        date: 可选的日期，用于指定获取哪一天的数据
    
    Returns:
        包含所有分析数据的AgentState对象
    """
    # 创建初始状态
    initial_state = AgentState(
        model_name=model_name,
        stock_list=stock_list,
        analysis_styles=analysis_styles,
        today_info_list=today_info_list,
        prompt_params_list=prompt_params_list,
        date=date
    )
    
    # 创建并运行工作流
    workflow = create_analysis_workflow()
    final_state = workflow.invoke(initial_state)
    
    return final_state

if __name__ == "__main__":
    # 示例调用
    model_name = "gpt-4o-mini"
    stock_list = ["AAPL", "MSFT"]
    analysis_styles = ["network_effect", "network_effect"]
    
    # 简单调用
    results = analyze_stocks_simple(
        model_name="gpt-4o-mini",
        stock_list=["AAPL"],
        analysis_styles=["network_effect"],
        date="2024-06-01"
    )
    print("分析结果:", results)
    
    # 高级调用
    state = analyze_stocks_advanced(
        model_name="gpt-4o-mini",
        stock_list=["AAPL"],
        analysis_styles=["network_effect"],
        date="2024-06-01"
    )
    print("完整状态:", state.analysis_results)
    print("历史结果:", state.history_results)

