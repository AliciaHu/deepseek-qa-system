import os
import time
import logging
from dotenv import load_dotenv

class ConfigManager:
    """
    一个用于监控文件变更并触发操作的类，特别用于从 '.env' 文件重新加载环境变量。
    新增配置获取方法，支持通过键名获取环境变量值。
    """
    def __init__(self):
        """
        类实例初始化方法
        
        功能说明:
            初始化实例属性并加载环境变量。配置防抖机制相关参数，防止重复触发。
            自动加载.env文件中的环境变量供后续使用。

        属性说明:
            last_trigger (int): 记录最近一次有效触发的时间戳，单位秒
            debounce_interval (int): 防抖时间窗口长度，单位秒（默认1秒）
        
        环境配置:
            通过load_dotenv()实现环境变量加载，需保证.env文件在项目根目录
        
        参数:
            无参数（标准self参数除外）
        
        返回值:
            无返回值
        """
        self.last_trigger = 0
        self.debounce_interval = 1  # 防抖间隔1秒
        load_dotenv()  # 初始化时立即加载环境变量

    def get(self, key: str, default=None):
        """安全获取环境变量值
        参数:
            key: 要获取的配置键名
            default: 当键不存在时返回的默认值
        """
        return os.getenv(key, default)

    def on_modified(self, event):
        """处理文件修改事件的回调函数
        
        Args:
            event: 文件系统事件对象，包含被修改文件的路径信息
        
        Returns:
            无返回值
        """
        try:
            # 精确路径匹配
            file_name = os.path.basename(event.src_path)
            if file_name != '.env':
                return

            # 防抖检查
            current_time = time.time()
            if current_time - self.last_trigger < self.debounce_interval:
                return

            # 执行环境变量加载
            load_dotenv()
            logging.info("配置文件已更新")

            # 更新最后触发时间
            self.last_trigger = current_time

        except Exception as e:
            # 异常处理: 捕获并记录环境变量加载失败信息
            logging.error(f"加载环境变量失败: {str(e)}", exc_info=True)