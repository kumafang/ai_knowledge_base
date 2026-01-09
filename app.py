#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 17:13:45 2026

@author: kumafang
"""

import sys
import os

# GitHub Token 从 Secrets 获取
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = f"https://{GITHUB_TOKEN}@github.com/kumafang/ai_knowledge_base.git"


# push knowledge base back to github 函数
import subprocess
import json

KB_PATH = "knowledge_base.json"

def save_knowledge_base(data):
    # 写入 JSON 文件
    with open(KB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 提交并 push 到 GitHub
    try:
        subprocess.run(["git", "add", KB_PATH], check=True)
        subprocess.run(["git", "commit", "-m", "Update knowledge_base.json"], check=True)
        subprocess.run(["git", "push", GITHUB_REPO, "main"], check=True)
        print("Knowledge base pushed to GitHub!")
    except subprocess.CalledProcessError as e:
        print("Git push failed:", e)


# 确保项目根目录在 sys.path
# 获取当前工作目录（Notebook / Spyder 下）
project_root = os.getcwd()  # 用 cwd 代替 __file__

# 把项目根目录加入 sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)


import streamlit as st
from loaders import load_file
from summarize import summarize_and_store
from chat import chat_with_kb

st.title("🧠 AI 个人知识库")

tab1, tab2 = st.tabs(["📥 知识输入", "💬 知识问答"])

# ---------- 知识输入 ----------
with tab1:
    uploaded = st.file_uploader(
        "上传文件（PDF / PPT / Word / Excel / CSV）",
        type=["pdf", "pptx", "docx", "xlsx", "csv"]
    )

    text_input = st.text_area("或直接输入文字")

    if st.button("让 AI 学习"):
        content = ""

        if uploaded:
            content += load_file(uploaded)

        if text_input:
            content += "\n" + text_input

        if content.strip():
            summary = summarize_and_store(content, source=uploaded.name if uploaded else "manual")
            st.success("已存入知识库")
            st.markdown("### 📌 提炼结果")
            st.write(summary)
            save_knowledge_base(knowledge_base) # 保存并 push
            st.info("✅ 知识库已同步到 GitHub")
        else:
            st.warning("请提供内容")

# ---------- 知识问答 ----------
with tab2:
    question = st.text_input("请输入你的问题")

    if st.button("提问"):
        answer = chat_with_kb(question)
        st.markdown("### 🤖 回答")
        st.write(answer)



