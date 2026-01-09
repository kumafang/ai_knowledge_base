#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 19:28:07 2026

@author: kumafang
"""

import json
import os
from openai import OpenAI

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
KB_PATH = "knowledge_base.json"

def chat_with_kb(question):
    if not os.path.exists(KB_PATH):
        return "知识库为空，请先上传内容。"

    with open(KB_PATH, "r", encoding="utf-8") as f:
        kb = json.load(f)

    knowledge = "\n\n".join(
        f"- {item['summary']}" for item in kb
    )

    system_prompt = f"""
你是一个基于知识库回答问题的 AI。
你只能使用以下知识库内容作答。
如果知识库中没有答案，请回答“知识库中未包含相关信息”。

知识库：
{knowledge}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0
    )

    return resp.choices[0].message.content
