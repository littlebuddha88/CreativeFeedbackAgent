import streamlit as st
import json
import random

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

# 더미 피드백 리스트
dummy_feedbacks = [
    "핵심 아이디어를 명확히 하면 좋겠습니다.",
    "조금 더 구체적으로 구상해보세요.",
    "창의성을 높이기 위해 새로운 요소를 추가해보세요.",
    "실현 가능성을 고려해 수정하면 더 좋겠습니다.",
    "독창적인 접근 방식을 조금 더 강조해보세요.",
    "문장을 간결하게 정리하면 이해가 더 쉬워집니다."
]

if st.button("피드백 받기"):
    if submission.strip() == "":
        st.warning("아이디어를 입력해주세요!")
    else:
        st.success("✅ 피드백 결과")
        feedback = random.choice(dummy_feedbacks)
        st.write(f"📌 더미 피드백: {feedback}")
        st.info("💡 실제 AI 피드백 대신 테스트용 더미 텍스트입니다.")
