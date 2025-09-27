# app/llm_service.py
import os
from openai import AsyncOpenAI # 修改为 AsyncOpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional

load_dotenv()

# 从 .env 文件获取 Qwen API Key 和 Base URL
QINIU_OPENAI_API_KEY = os.getenv("QINIU_OPENAI_API_KEY")
QINIU_OPENAI_BASE_URL = os.getenv("QINIU_OPENAI_BASE_URL") # 直接从 .env 获取，确保一致

if not QINIU_OPENAI_API_KEY:
    raise ValueError("QINIU_OPENAI_API_KEY environment variable not set.")
if not QINIU_OPENAI_BASE_URL:
    raise ValueError("QINIU_OPENAI_BASE_URL environment variable not set.")

# 初始化 AsyncOpenAI 客户端，指向七牛云的兼容接口
client = AsyncOpenAI(
    api_key=QINIU_OPENAI_API_KEY,
    base_url=QINIU_OPENAI_BASE_URL,
)

async def get_qwen_response(
    system_prompt: str,
    chat_history: List[Dict[str, str]], # 聊天历史，包含 sender_type 和 content
    user_message: str,
    few_shot_examples: Optional[List[Dict[str, str]]] = None,
    temperature: float = 0.7,
    max_tokens: int = 500,
    model: str = "qwen3-235b-a22b-thinking-2507" # 使用你的模型ID
) -> str:
    messages = []

    # 添加系统提示
    messages.append({"role": "system", "content": system_prompt})

    # 添加 Few-Shot 示例
    if few_shot_examples:
        for example in few_shot_examples:
            if "user" in example:
                messages.append({"role": "user", "content": example["user"]})
            if "ai" in example: # 注意 Few-shot 示例中的 AI 回复在 OpenAI API 中通常用 'assistant' 角色
                messages.append({"role": "assistant", "content": example["ai"]})

    # 添加历史消息
    for msg in chat_history:
        # 将我们数据库中的 sender_type ('user' 或 'ai') 转换为 LLM 期望的 role ('user' 或 'assistant')
        role_type = "user" if msg["sender_type"] == "user" else "assistant"
        messages.append({"role": role_type, "content": msg["content"]})

    # 添加当前用户消息
    messages.append({"role": "user", "content": user_message})

    try:
        completion = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Qwen API: {e}")
        return "Sorry, I am unable to respond at the moment."