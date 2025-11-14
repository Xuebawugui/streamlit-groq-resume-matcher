import streamlit as st
import pdfplumber
from groq import Groq
import os
import json
from dotenv import load_dotenv

st.set_page_config(page_title="AI简历匹配 - 日本IT专用", layout="centered")
load_dotenv()

translations = {
    "zh": {
        "title": "AI简历匹配系统（Groq超高速版）",
        "caption": "专为去日本找IT工作打造 | Llama3-70B 500token/s | 完全免费额度",
        "ui_lang_label": "界面语言",
        "model_label": "选择模型（速度排序）",
        "output_lang_label": "输出语言",
        "jd_label": "请粘贴职位描述（JD）",
        "jd_placeholder": "例：Python, React, 5年以上の経験, Tokyo勤務, ビジネスレベル日本語...",
        "upload_label": "上传简历（PDF格式）",
        "analyze_button": "开始AI分析",
        "missing_input_error": "请同时填写JD并上传简历PDF",
        "spinner_text": "Groq超高速分析中（通常3-6秒）...",
        "analysis_done": "分析完成！（Groq极速响应）",
        "result_header": "匹配结果",
        "result_raw_header": "匹配结果（原始）",
        "api_key_missing_error": "未检测到 Groq API Key。请在 Secrets 添加 GROQ_API_KEY 或设置环境变量。",
    },
    "en": {
        "title": "AI Resume Matcher (Groq Ultra Fast)",
        "caption": "Built for Japan IT job hunting | Llama3-70B | Free quota",
        "ui_lang_label": "UI Language",
        "model_label": "Choose model (sorted by speed)",
        "output_lang_label": "Output Language",
        "jd_label": "Paste Job Description (JD)",
        "jd_placeholder": "e.g., Python, React, 5+ years, Tokyo, Business-level Japanese...",
        "upload_label": "Upload Resume (PDF)",
        "analyze_button": "Analyze",
        "missing_input_error": "Please provide JD and upload a PDF resume",
        "spinner_text": "Analyzing with Groq (3–6s typical)...",
        "analysis_done": "Analysis complete (Groq fast)",
        "result_header": "Match Result",
        "result_raw_header": "Match Result (Raw)",
        "api_key_missing_error": "Groq API key not found. Set Secrets or environment variable.",
    },
    "ja": {
        "title": "AI職務適合度（Groq超高速版）",
        "caption": "日本IT就職向け | Llama3-70B | 無料枠",
        "ui_lang_label": "UI言語",
        "model_label": "モデル選択（速度順）",
        "output_lang_label": "出力言語",
        "jd_label": "求人票（JD）を貼り付けてください",
        "jd_placeholder": "例：Python, React, 経験5年以上, 東京勤務, ビジネスレベル日本語...",
        "upload_label": "履歴書をアップロード（PDF）",
        "analyze_button": "AI分析を開始",
        "missing_input_error": "JDの入力とPDF履歴書のアップロードが必要です",
        "spinner_text": "Groqで超高速分析中（通常3–6秒）...",
        "analysis_done": "分析完了（Groq高速）",
        "result_header": "適合結果",
        "result_raw_header": "適合結果（Raw）",
        "api_key_missing_error": "Groq APIキーが見つかりません。Secretsまたは環境変数を設定してください。",
    },
}

ui_lang = st.sidebar.radio("界面语言 / UI Language", ["日本語", "English", "中文"], index=2)
lang_code = "ja" if ui_lang == "日本語" else ("en" if ui_lang == "English" else "zh")
t = translations[lang_code]

st.title(t["title"])
st.caption(t["caption"])

model = st.sidebar.selectbox(
    t["model_label"],
    ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it"],
    index=0,
)

output_lang = st.sidebar.radio(t["output_lang_label"], ["日本語", "English"], index=0)

jd = st.text_area(
    t["jd_label"],
    height=160,
    placeholder=t["jd_placeholder"],
)

uploaded_file = st.file_uploader(t["upload_label"], type=["pdf"]) 

if st.button(t["analyze_button"], type="primary"):
    if not jd or not uploaded_file:
        st.error(t["missing_input_error"])
    else:
        with st.spinner(t["spinner_text"]):
            resume_text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        resume_text += text + "\n"

            api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
            if not api_key:
                st.error(t["api_key_missing_error"])
                st.stop()

            client = Groq(api_key=api_key)

            prompt = f"""
你现在是一位在日本IT公司工作10年的资深招聘官。
请根据以下职位描述和候选人简历，给出专业匹配分析。

职位描述（JD）：
{jd}

候选人简历：
{resume_text}

请严格按照以下JSON格式输出（{"日本語" if output_lang == "日本語" else "English"}）：
{{
  "match_score": 0-100,
  "summary": "一句话总体评价",
  "strengths": ["优势1", "优势2", "优势3"],
  "gaps": ["目前缺失的技能或经验1", "缺失2"],
  "japanese_suggestions": "日语简历/面试改进建议（如果适用）",
  "interview_questions": ["问题1", "问题2", "问题3"]
}}
"""

            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
                temperature=0.3,
                max_tokens=2048,
            )

            result = chat_completion.choices[0].message.content.strip()
            try:
                parsed = json.loads(result)
                st.success(t["analysis_done"])
                st.markdown(f"### {t['result_header']}")
                st.json(parsed, expanded=True)
            except Exception:
                st.success(t["analysis_done"])
                st.markdown(f"### {t['result_raw_header']}")
                st.json(result, expanded=True)