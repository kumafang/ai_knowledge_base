#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 19:22:20 2026

@author: kumafang
"""

import json
import os
from openai import OpenAI
import subprocess

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
KB_PATH = "knowledge_base.json"
# GitHub Token 从 Secrets 获取
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")

def load_latest_kb():
    # 从 GitHub 拉取最新版本
    try:
        subprocess.run(["git", "pull", GITHUB_REPO, "main"], check=True)
    except subprocess.CalledProcessError as e:
        print("Git pull failed, maybe first run:", e)

    if os.path.exists(KB_PATH):
        with open(KB_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []

    return data


def summarize_and_store(content, source="manual"):
    data = load_latest_kb()  # 拉取最新 KB
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

        # push 回 GitHub
    try:
        subprocess.run(["git", "add", KB_PATH], check=True)
        # 如果没有 commit 则 commit，否则 git 会提示 nothing to commit
        subprocess.run(["git", "commit", "-m", f"Update knowledge_base: {source}"], check=False)
        subprocess.run(["git", "push", GITHUB_REPO, "main"], check=True)
        print("Knowledge base pushed to GitHub!")
    except Exception as e:
        print("Git push failed:", e)
        
    return summary, data
