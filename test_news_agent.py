# test_news_agent.py
from news_agent import analyze_stocks_simple

if __name__ == "__main__":
    # 股票代码
    stock_list = ["AAPL"]
    # 分析风格
    analysis_styles = ["network_effect_analysis"]
    # 自定义今日新闻
    today_info_list = [
        {
            "news_summary":"""2025年7月10日：中国区AI功能删除引发信任危机
新闻摘要
苹果中国官网删除所有“Apple智能（Apple Intelligence）”描述，包括iPhone 16系列“为AI预备好”的标注。此前多次跳票，因监管审批（数据跨境限制）及技术缺陷（端侧模型正确率仅66%-70%）导致国行AI功能缺席1。
过往信息
2024年WWDC承诺国行AI功能，但全球版上线时排除中国用户1。

网络效应分析

用户增长分析：负增长

用户增长率：-8%（Q2中国销量跌至第五，同比下滑8%）

生态价值分析

ARPU变化：-6%（高端机型降价2500元仍难挽市场，国产手机AI渗透率40%挤压溢价空间）1。

跨边效应分析

开发者与监管协同断裂：百度/阿里AI合作方案卡在审批，开发者转向华为/小米生态开发适配功能1。
关键指标

网络效应强度：强→弱

关键证据：用户吐槽“花同样的钱，凭什么我们用不上AI？”登热搜，阅读量4.2亿1。

"""
        }
    ]
    # 调用分析
    results = analyze_stocks_simple(
        model_name="gpt-4o-mini",
        stock_list=stock_list,
        analysis_styles=analysis_styles,
        today_info_list=today_info_list
    )
    print("分析结果:")
    for res in results:
        print(res) 