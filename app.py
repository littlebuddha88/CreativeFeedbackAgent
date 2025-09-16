import streamlit as st
import pandas as pd
import openai
import json

# 🔑 환경 변수에 OPENAI_API_KEY 저장하거나, st.secrets["OPENAI_API_KEY"] 사용
openai.api_key = st.secrets["OPENAI_API_KEY"]

# JSON 불러오기
with open("rubric.json", "r", encoding="utf-8") as f:
    rubric = json.load(f)

st.title("🎨 AI 창작자 교육 피드백 챗봇")

# 단계 선택
level = st.selectbox("학습 난이도", ["beginner", "intermediate", "advanced"])
category_options = [item["title"] for item in rubric[level]]
category_title = st.selectbox("피드백 유형", category_options)

# 선택된 프롬프트 가져오기
selected_prompt = next(item["prompt"] for item in rubric[level] if item["title"] == category_title)

# 사용자 입력
submission = st.text_area("✍️ 제출물 입력", placeholder="여기에 과제나 텍스트를 붙여 넣으세요")

if st.button("피드백 받기"):
    if submission.strip() == "":
        st.warning("제출물을 입력해주세요!")
    else:
        prompt = selected_prompt.replace("{SUBMISSION}", submission)

        with st.spinner("AI가 피드백을 작성 중입니다..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "너는 창작자 교육을 돕는 피드백 코치다."},
                          {"role": "user", "content": prompt}]
            )
            feedback = response["choices"][0]["message"]["content"]
            st.success("✅ 피드백 결과")
            st.write(feedback)
