# example_usage.py - 展示如何使用重构后的news_agent函数
from news_agent import analyze_stocks_simple, analyze_stocks_advanced, AgentState
from typing import List, Dict, Optional

def example_simple_usage():
    """简单使用示例"""
    print("=== 简单使用示例 ===")
    
    # 基本参数
    model_name = "gpt-4o-mini"
    stock_list = ["AAPL", "MSFT", "GOOGL"]
    analysis_styles = ["network_effect", "network_effect", "network_effect"]
    
    # 调用分析函数
    results = analyze_stocks_simple(
        model_name=model_name,
        stock_list=stock_list,
        analysis_styles=analysis_styles
    )
    
    # 输出结果
    for i, result in enumerate(results):
        print(f"\n股票 {stock_list[i]} 分析结果:")
        print(result)
        print("-" * 50)

def example_advanced_usage():
    """高级使用示例"""
    print("\n=== 高级使用示例 ===")
    
    # 基本参数
    model_name = "gpt-4o-mini"
    stock_list = ["TSLA", "NVDA"]
    analysis_styles = ["network_effect", "network_effect"]
    
    # 自定义今日信息
    today_info_list = [
        {
            "symbol": "TSLA",
            "shortName": "Tesla, Inc.",
            "marketCap": 800000000000,
            "currentPrice": 250.0,
            "news_summary": "特斯拉发布新款Model S，销量增长强劲"
        },
        None  # 第二个股票使用API获取
    ]
    
    # 自定义提示词参数
    prompt_params_list = [
        {
            "custom_param": "重点关注电动汽车市场表现",
            "analysis_focus": "技术创新和市场份额"
        },
        None  # 第二个股票使用默认参数
    ]
    
    # 调用高级分析函数
    state = analyze_stocks_advanced(
        model_name=model_name,
        stock_list=stock_list,
        analysis_styles=analysis_styles,
        today_info_list=today_info_list,
        prompt_params_list=prompt_params_list
    )
    
    # 输出完整结果
    print(f"分析结果数量: {len(state.analysis_results)}")
    print(f"历史结果数量: {len(state.history_results)}")
    
    for i, (symbol, analysis_result, history_result) in enumerate(
        zip(stock_list, state.analysis_results, state.history_results)
    ):
        print(f"\n股票 {symbol} 完整分析:")
        print("今日分析:")
        print(analysis_result)
        print("\n历史总结:")
        print(history_result)
        print("=" * 60)

def example_langgraph_workflow():
    """LangGraph工作流使用示例"""
    print("\n=== LangGraph工作流示例 ===")
    
    from news_agent import create_analysis_workflow
    
    # 创建初始状态
    initial_state = AgentState(
        model_name="gpt-4o-mini",
        stock_list=["META", "AMZN"],
        analysis_styles=["network_effect", "network_effect"],
        today_info_list=None,
        prompt_params_list=None
    )
    
    # 创建并运行工作流
    workflow = create_analysis_workflow()
    final_state = workflow.invoke(initial_state)
    
    # 输出工作流结果
    print("工作流执行完成!")
    print(f"股票列表: {final_state.stock_list}")
    print(f"分析结果数量: {len(final_state.analysis_results)}")
    print(f"历史结果数量: {len(final_state.history_results)}")
    
    # 显示第一个股票的分析结果
    if final_state.analysis_results:
        print(f"\n{final_state.stock_list[0]} 分析结果:")
        print(final_state.analysis_results[0])

def example_error_handling():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    try:
        # 使用不存在的股票代码测试错误处理
        results = analyze_stocks_simple(
            model_name="gpt-4o-mini",
            stock_list=["INVALID_STOCK", "AAPL"],
            analysis_styles=["network_effect", "network_effect"]
        )
        
        print("错误处理测试完成")
        for i, result in enumerate(results):
            print(f"股票 {i+1} 结果: {result[:100]}...")
            
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    # 运行所有示例
    example_simple_usage()
    example_advanced_usage()
    example_langgraph_workflow()
    example_error_handling()
    
    print("\n=== 所有示例运行完成 ===") 