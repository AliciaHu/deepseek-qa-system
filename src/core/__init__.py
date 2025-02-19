# 在类初始化中添加
from accelerate import init_empty_weights, load_checkpoint_and_dispatch

class ModelLoader:
    """
    ModelLoader 类用于加载模型。

    参数:
    model (Any): 要加载的模型。
    model_path (str): 模型的路径。
    """
    from typing import Any

    def __init__(self, model: Any, model_path: str):
        self.model = model
        self.model_path = model_path

    def load_model(self) -> None:
        """
        加载模型并分配到设备。

        返回:
        None
        """
        try:
            self.model = load_checkpoint_and_dispatch(
                self.model,
                self.model_path,
                device_map="auto",
                no_split_module_classes=["DeepseekLayer"]
            )
        except Exception as e:
            print(f"加载模型时出错: {e}")