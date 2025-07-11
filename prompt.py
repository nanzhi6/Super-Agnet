"""
股票分析提示词模板文件
包含各种分析类型的模板，支持通过名称提取和占位符替换
"""

网络效应分析新闻模板 = """
作为平台经济专家，请基于**2024年公司新闻**评估该公司的网络效应：

【新闻摘要】
{news_summary}
【过往信息】
{history_info}

【分析要求】
1. **用户增长分析**：从新闻中推断用户增长趋势（正增长/负增长/稳定）
2. **生态价值分析**：分析新闻中提到的用户互动或ARPU相关变化
3. **跨边效应分析**：识别新闻中描述的不同用户群体间的协同关系

【分析框架】
- 用户增长率：%（根据新闻推断）
- ARPU变化：%（根据新闻推断）
- 网络效应强度：（弱/中/强）

【输出格式】
- 用户增长率：[数值或趋势描述]
- ARPU变化：[+/- 数值或趋势描述]%
- 网络效应强度：[弱/中/强]
- 关键证据：[引用新闻中的关键语句]
"""

网络效应智能分析模板 = """
作为金融AI分析师，请从以下该公司的2024年新闻中提取网络效应相关信息：

【原始新闻文本】
{raw_news_text}

【分析任务】
1. 用户增长指标提取：找出用户增长率相关数据
2. ARPU变化分析：识别ARPU值变动信息
3. 群体协同证据：发现不同用户群体互动的描述

【输出要求】
按以下JSON格式输出分析结果：
{{
  "user_growth": {{
    "value": "增长率数值或描述",
    "source": "新闻原文引用"
  }},
  "arpu_change": {{
    "value": "变化数值或描述",
    "source": "新闻原文引用"
  }},
  "network_effect_strength": "弱/中/强",
  "cross_group_synergy": "协同效应描述",
  "key_evidence": ["关键语句1", "关键语句2"]
}}
"""

过往信息新闻模板 = """
作为平台经济专家，请基于历史数据和今日新闻，全面分析该公司的网络效应演进情况：

【核心任务】
1. 识别网络效应的关键变化点
2. 评估当前网络效应的强度

【输入信息】
📰 今日新闻摘要 :
{news_summary}

📊 历史网络效应数据:
{history_info}

"""

# 模板字典，用于通过名称提取
PROMPT_TEMPLATES = {
    "network_effect": 网络效应分析新闻模板,
    "network_effect_analysis": 网络效应智能分析模板,
    "network_effect_history": 过往信息新闻模板

}

def get_prompt_template(template_name: str) -> str:
    """
    通过模板名称获取提示词模板
    
    Args:
        template_name: 模板名称
        
    Returns:
        提示词模板字符串
    """
    if template_name not in PROMPT_TEMPLATES:
        raise ValueError(f"不支持的模板名称: {template_name}")
    
    return PROMPT_TEMPLATES[template_name]

def format_prompt(template_name: str, **kwargs) -> str:
    """
    格式化提示词模板，填充占位符
    
    Args:
        template_name: 模板名称
        **kwargs: 要填充的参数
        
    Returns:
        格式化后的提示词
    """
    template = get_prompt_template(template_name)
    return template.format(**kwargs)

def get_available_templates() -> list:
    """
    获取所有可用的模板名称
    
    Returns:
        模板名称列表
    """
    return list(PROMPT_TEMPLATES.keys())

