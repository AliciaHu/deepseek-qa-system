import re

class InputProcessor:
    
    @staticmethod
    def sanitize_input(text: str) -> str:
        """
        清理并限制输入文本的长度。

        该方法用于清理输入文本中的特殊字符，并将文本长度限制在512个字符以内。

        参数:
            text (str): 需要清理和限制长度的输入文本。

        返回:
            str: 清理后的文本，长度不超过512个字符。
        """
        # 清理特殊字符
        text = re.sub(r'[<>\\\'\"]', '', text)
        # 限制最大长度
        return text[:512]
    
    @staticmethod
    def format_history(history: list) -> str:
        """将对话历史记录格式化为特定字符串格式
        
        参数:
        history -- 对话历史记录，每个元素为包含用户问题和助手回答的二元组/列表
            （格式：[("用户问题1", "助手回答1"), ("用户问题2", "助手回答2"), ...]）
            
        返回值:
        str -- 格式化后的对话字符串，每段对话格式为：
            "用户：{用户问题}\n助手：{助手回答}"，不同对话间用换行符分隔
        """
        # 使用列表推导式将每条问答转换为特定格式字符串，并用换行符连接
        return "\n".join([f"用户：{q}\n助手：{a}" for q, a in history])