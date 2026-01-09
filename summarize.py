#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 19:22:20 2026

@author: kumafang
"""

import json
import os
from openai import OpenAI


openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
KB_PATH = "knowledge_base.json"

def summarize_and_store(content, source="manual"):
    prompt = f"""
你是一个知识整理助手。
请从以下内容中提炼最重要、最核心的信息。
要求：
- 用简洁的中文
- 不添加原文没有的信息
- 类似“知识卡片”的总结

内容：
{content}
"""

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    summary = resp.choices[0].message.content

    data = []
    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

    data.append({
        "source": source,
        "summary": summary
    })

    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return summary
