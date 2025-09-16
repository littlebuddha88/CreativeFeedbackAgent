import streamlit as st
import openai
import json
from PIL import Image

# OpenAI API Key 설정
openai.api_key = st.secrets.get("OPENAI_API_KEY")

# 루브릭 불러오기
with open("rubric.json", "r", encoding="utf-8") as f:
    rubric = json.load(f)

st.title("🎨 AI 창작자 교육 피드백 챗봇 (텍스트+이미지)")

# 단계 선택
level = st.selectbox("학습 난이도", ["beginner", "intermediate", "advanced"])
category_options = [item["title"] for item in rubric[level]]
category_title = st.selectbox("피드백 유형", category_options)
selected_prompt = next(item["prompt"] for item in rubric[level] if item["title"] == category_title)

# 텍스트 제출
submission = st.text_area("✍️ 과제 텍스트 입력", placeholder="여기에 과제나 텍스트를 붙여 넣으세요")

# 이미지 제출
uploaded_file = st.file_uploader("📷 이미지 업로드 (선택)", type=["png", "jpg", "jpeg"])
image_description = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드한 이미지 미리보기", use_column_width=True)
    image_description = st.text_input("이미지에 대한 설명 입력 (예: '촬영 장면, 구성 의도')")

# 피드백 버튼
if st.button("피드백 받기"):
    if not submission.strip() and uploaded_file is None:
        st.warning("텍스트 또는 이미지를 제출해주세요!")
    else:
        # 프롬프트 생성
        prompt_text = selected_prompt.replace("{SUBMISSION}", submission)
        if uploaded_file is not None:
            prompt_text += f"\n이미지 설명: {image_description}"

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
