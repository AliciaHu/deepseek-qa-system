from core.response_gen import ResponseGenerator
from utils.input_processor import InputProcessor
import time
import asyncio


async def main():
    """主异步函数，控制问答系统的交互流程
    
    功能：
        - 初始化系统组件并显示启动耗时
        - 持续接收用户输入问题
        - 对输入进行安全清洗处理
        - 异步生成并格式化输出回答及耗时统计
        - 支持安全退出机制
    
    流程说明：
        1. 初始化问答系统核心组件
        2. 进入交互式命令行界面循环
        3. 支持普通文本问答和退出指令两种模式
        4. 捕获键盘中断实现安全退出
    
    参数：无
    返回值：无
    """
    # 系统初始化模块
    print("初始化问答系统...")
    start = time.time()    
    qa_system = ResponseGenerator()  # 回答生成器实例
    processor = InputProcessor()     # 输入预处理模块
    
    print(f"系统已就绪，初始化耗时：{time.time()-start:.2f}s")
    
    # 主交互循环
    while True:
        try:
            # 用户输入处理模块
            question = input("\n请输入问题（输入q退出）: ")
            if question.lower() == 'q':
                break
            
            # 输入清洗与安全检查
            clean_question = processor.sanitize_input(question)
            print("生成回答中...")
            
            # 异步回答生成模块
            start_time = time.time()
            response, gen_time = await qa_system.async_generate(clean_question)
            
            # 格式化输出模块
            print(f"\n回答（生成耗时 {gen_time:.2f}s）：")
            print("-"*30)
            print(response)
            print("-"*30)
            
        # 安全退出处理模块
        except KeyboardInterrupt:
            print("\n系统安全退出")
            break

if __name__ == "__main__":
    asyncio.run(main())