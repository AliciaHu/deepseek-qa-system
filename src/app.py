import chainlit as cl
from core.response_gen import ResponseGenerator
from utils.input_processor import InputProcessor
from typing import Optional
import logging

# 初始化组件
MODEL_READY_MSG = "模型已就绪，请输入您的问题..."
ERR_MSG = "处理请求时发生错误，请稍后重试或联系管理员。"

# 初始化系统组件（单例模式）
qa_system = ResponseGenerator()
processor = InputProcessor()  # Initialize the processor

@cl.on_chat_start
async def start_chat() -> None:
    """处理聊天会话启动事件
     
    功能：
    - 发送系统就绪提示消息
    - 初始化聊天会话上下文
    """
    await cl.Message(MODEL_READY_MSG).send()

@cl.on_message
async def main(message: cl.Message):
    """处理用户消息的核心业务逻辑
    
    Args:
        message: 用户消息对象，包含消息内容等元数据
    
    Process:
        1. 输入清洗 -> 2. 响应生成 -> 3. 结果返回
    """
    try:
        # 输入预处理
        question: str = message.content
        clean_question: Optional[str] = processor.sanitize_input(question)
        
        if not clean_question:
            await cl.Message(content="输入内容无效，请重新输入").send()
            return

        # 异步生成响应
        response, gen_time = await qa_system.async_generate(clean_question)
        logging.info(f"生成耗时 {gen_time:.2f}s");
        
        # 返回格式化响应
        await cl.Message(content=response).send()

    except Exception as e:
        logging.error(f"消息处理失败: {str(e)}", exc_info=True)
        await cl.Message(content=ERR_MSG).send()
