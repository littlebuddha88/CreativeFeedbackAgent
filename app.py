import streamlit as st
import json

st.title("🎨 AI 창작자 교육 피드백 챗봇 (API 없이 테스트용)")

# 루브릭 불러오기
with open("rubric.json", "r", encoding="utf-8") as f:
    rubric = json.load(f)

# 단계 선택
level = st.selectbox("학습 난이도", ["beginner", "intermediate", "advanced"])
category_options = [item["title"] for item in rubric[level]]
category_title = st.selectbox("피드백 유형", category_options)

# 선택된 프롬프트 가져오기
selected_prompt = next(item["prompt"] for item in rubric[level] if item["title"] == category_title)

# 텍스트 제출
submission = st.text_area("✍️ 과제/아이디어 입력", placeholder="여기에 아이디어를 적어주세요")

if st.button("피드백 받기"):
    if submission.strip() == "":
        st.warning("아이디어를 입력해주세요!")
    else:
        # 더미 피드백 생성
        st.success("✅ 피드백 결과")
        st.write(f"📌 더미 피드백: '{submission[:50]}...'에 대한 개선 포인트 예시")
        st.info("💡 실제 AI 피드백 대신 테스트용 더미 텍스트입니다.")
