# src/core/model_loader.py
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from dotenv import load_dotenv
import os
from huggingface_hub import login
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging

load_dotenv()

class ModelLoader:
    _instance = None    
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.model_name = os.getenv("MODEL_NAME", "deepseek-ai/deepseek-llm-7b-chat")
        
        # 设置 Hugging Face 镜像代理
        os.environ["HF_HUB_ENABLE_HF_TRANSFER"] = "true"

        # 设置 MPS 高水位线和低水位线比例
        os.environ["PYTORCH_MPS_HIGH_WATERMARK_RATIO"] = "0.9"  # 设置为 90%
        os.environ["PYTORCH_MPS_LOW_WATERMARK_RATIO"] = "0.5"   # 设置为 50%

        # 设置请求重试机制
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http = requests.Session()
        http.mount("https://", adapter)
        http.mount("http://", adapter)

        # 登录 Hugging Face
        hf_token = os.getenv("HF_API_TOKEN")
        if hf_token:
            login(token=hf_token)

        # 量化配置及加载模型
        try:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                offload_folder="./offload"  # 指定权重卸载的文件夹
            )
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        except Exception as e:
            logging.info(f"加载主模型 '{self.model_name}' 失败: {e}. 尝试备用模型 'deepseek-ai/deepseek-llm-1b-chat'.")
            backup_model = os.getenv("MODEL_NAME", "deepseek-ai/deepseek-llm-7b-chat")
            self.model = AutoModelForCausalLM.from_pretrained(
                backup_model,
                torch_dtype=torch.float16,
                device_map="auto",
                trust_remote_code=True,
                offload_folder="./offload"
            )
            self.tokenizer = AutoTokenizer.from_pretrained(backup_model)
            # 更新模型名称为备用模型
            self.model_name = backup_model

        self.tokenizer.pad_token = self.tokenizer.eos_token

    def get_model(self):
        return self.model, self.tokenizer