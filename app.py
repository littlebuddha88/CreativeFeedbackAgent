import streamlit as st
import openai
import json

# OpenAI API 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 루브릭 불러오기
with open("rubric.json", "r", encoding="utf-8") as f:
    rubric = json.load(f)

st.title("🎨 AI 창작자 교육 피드백 챗봇 (텍스트 전용)")

# 단계 선택
level = st.selectbox("학습 난이도", ["beginner", "intermediate", "advanced"])
category_options = [item["title"] for item in rubric[level]]
category_title = st.selectbox("피드백 유형", category_options)

# 선택된 프롬프트 가져오기
selected_prompt = next(item["prompt"] for item in rubric[level] if item["title"] == category_title)

# 텍스트 제출
submission = st.text_area("✍️ 과제/아이디어 입력", placeholder="여기에 아이디어를 적어주세요")

# 피드백 버튼
if st.button("피드백 받기"):
    if submission.strip() == "":
        st.warning("아이디어를 입력해주세요!")
    else:
        # 프롬프트 생성
        prompt_text = selected_prompt.replace("{SUBMISSION}", submission)

        with st.spinner("AI가 피드백 작성 중..."):
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "너는 창작자 교육을 돕는 피드백 코치다."},
                    {"role": "user", "content": prompt_text}
                ]
            )
            feedback = response["choices"][0]["message"]["content"]
            st.success("✅ 피드백 결과")
            st.write(feedback)
