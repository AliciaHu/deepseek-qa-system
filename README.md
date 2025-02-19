# Deepseek QA System- 智能问答系统

基于 Deepseek 大模型开发的智能问答系统，通过 Chainlit 提供交互式聊天界面，支持异步回答生成、环境配置热加载以及性能监控。

## 特性

- **智能问答**：利用 Deepseek 大模型实时生成回答。
- **异步生成**：支持异步调用，提升响应效率。
- **配置热加载**：基于 `.env` 文件，通过 `ConfigManager` 自动更新环境变量配置。
- **性能监控**：使用 Prometheus 监控回答生成耗时。
- **模型缓存**：单例模式加载并缓存模型与分词器。

## 技术栈

- Python 3.11
- HuggingFace Transformers
- Asyncio 异步框架
- Prometheus监控
- 自定义输入处理模块

## 系统架构
```mermaid
flowchart TB
  A([用户输入]) --> B{输入净化}
  B --> C{模型选择}
  C -->|主模型| D[DeepSeek-7B]
  C -->|降级策略| E[备用模型]
  D --> F[异步生成响应]
  E --> F
  F --> G[[结果输出]]
  
  style A fill:#4CAF50,stroke:#388E3C
  style B fill:#2196F3,stroke:#1976D2
  style C fill:#FF9800,stroke:#F57C00
  style D fill:#9C27B0,stroke:#7B1FA2
  style E fill:#E91E63,stroke:#C2185B
  style F fill:#009688,stroke:#00796B
  style G fill:#795548,stroke:#5D4037