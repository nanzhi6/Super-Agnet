import openai
import os
from typing import List
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
class AgentCall:
    """LLM调用类，支持多种大语言模型"""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.client = self._create_client()
    
    def _create_client(self):
        if 'gpt' in self.model_name.lower():
            api_key = os.getenv('OPENAI_API_KEY')
            base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
            if not api_key or api_key == 'your_openai_api_key_here':
                raise ValueError("请在.env文件中设置正确的OPENAI_API_KEY")
            return openai.OpenAI(api_key=api_key, base_url=base_url)
        elif 'deepseek' in self.model_name.lower():
            api_key = os.getenv('deepseek_API_KEY')
            base_url = "https://api.deepseek.com/v1"
            if not api_key:
                raise ValueError("请在.env文件中设置正确的deepseek_API_KEY")
            return openai.OpenAI(api_key=api_key, base_url=base_url)
        else:
            raise ValueError(f"不支持的模型名称: {self.model_name}")

    def infomation_prompts_analysis(self, prompt_list: List[str]) -> List[str]:
        """
        分析提示词列表，直接返回AI的完整分析结果文本
        """
        results = []
        for i, prompt in enumerate(prompt_list):
            try:
                print(f"正在分析第 {i+1}/{len(prompt_list)} 只股票的信息...")
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "你是一个专业的股票分析师，请根据提供的信息进行股票分析。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                analysis_text = response.choices[0].message.content
                results.append(analysis_text)
            except Exception as e:
                print(f"分析第 {i+1} 只股票的信息时出现错误: {e}")
                results.append(f"分析过程中出现错误: {str(e)}")
        return results
    
    def history_prompts_analysis(self, prompt_list: List[str]) -> List[str]:
        """
        分析提示词列表，直接返回AI的完整分析结果文本
        """
        results = []
        for i, prompt in enumerate(prompt_list):
            try:
                print(f"正在总结第 {i+1}/{len(prompt_list)} 只股票的历史数据...")
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "你是一个专业的股票分析师，请根据提供的信息对这支股票的历史信息进行总结。"},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                analysis_text = response.choices[0].message.content
                results.append(analysis_text)
            except Exception as e:
                print(f"总结第 {i+1} 只股票的历史数据时出现错误: {e}")
                results.append(f"分析过程中出现错误: {str(e)}")
        return results

def create_agent_call(model_name: str) -> AgentCall:
    return AgentCall(model_name)

if __name__ == "__main__":
    # 测试代码
    try:
        agent = create_agent_call("gpt-3.5-turbo")
        test_prompts = ["请分析股票AAPL的投资价值"]
        results = agent.analyze_prompts(test_prompts)
        print("OpenAI测试结果:", results)
    except Exception as e:
        print(f"测试失败: {e}")
        print("请确保在.env文件中设置了正确的API密钥") 