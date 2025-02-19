from .model_loader import ModelLoader
from typing import Tuple
import os
import torch
import time
import asyncio
from prometheus_client import Summary
from utils.config_manager import ConfigManager

class ResponseGenerator:
    """智能响应生成器，核心功能模块
  
    Attributes:
        model: 加载的预训练模型实例
        tokenizer: 文本分词器
    """

    RESPONSE_TIME = Summary('response_time', 'Time spent generating responses')

    def __init__(self):
        """初始化模型与分词器"""
        self.loader = ModelLoader()
        self.model, self.tokenizer = self.loader.get_model()
        self.config_manager = ConfigManager()
        self._load_gen_config()
        # 将eos_token_id和pad_token_id预计算并缓存
        self.eos_token_id = torch.tensor(self.tokenizer.eos_token_id).to(self.model.device)
        self.pad_token_id = torch.tensor(self.tokenizer.pad_token_id).to(self.model.device)
        # 添加动态状态缓存
        self.past_key_values = None

    def _load_gen_config(self):
        """加载生成配置"""
        self.gen_config = {
            "max_new_tokens": int(self.config_manager.get("MAX_TOKENS") or 512),
            "temperature": float(self.config_manager.get("TEMPERATURE") or 0.7),
            "top_p": float(self.config_manager.get("TOP_P") or 0.9),
            "repetition_penalty": float(self.config_manager.get("REP_PENALTY") or 1.1)
        }

    def generate(self, question: str) -> Tuple[str, float]:
        """生成回答
        
        Args:
            question: 用户输入的问题
        
        Returns:
            Tuple(生成的回答文本, 生成耗时秒数)
        """
        start_time = time.time()
        inputs = self.tokenizer(
            f"用户：{question}\n助手：",
            return_tensors="pt"
        ).to(self.model.device)

        # 生成回答
        with torch.no_grad():
            outputs = self.model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                eos_token_id=self.eos_token_id,
                pad_token_id=self.pad_token_id,
                max_new_tokens=self.gen_config["max_new_tokens"],
                temperature=self.gen_config["temperature"],
                top_p=self.gen_config["top_p"],
                repetition_penalty=self.gen_config["repetition_penalty"],     
            )
        
        gen_time = time.time() - start_time
        response = self.tokenizer.decode(
            outputs[0][inputs["input_ids"].size(1):], # type: ignore
            skip_special_tokens=True
        )
        
        return response.strip(), gen_time
    
    @RESPONSE_TIME.time()
    async def async_generate(self, question: str) -> Tuple[str, float]:
        """异步生成回答
      
        Args:
            question: 经过净化的用户输入问题
      
        Returns:
            Tuple(生成的回答文本, 生成耗时秒数)
        """
        loop = asyncio.get_event_loop() # 获取事件循环
        response, gen_time = await loop.run_in_executor(None, self.generate, question) # 将任务交给线程池
        return response, gen_time