import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="완전해결 맞춤법검사기", page_icon="✅")
st.title("✅ AI 맞춤법 & 발음 교정기")

api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # [핵심] 여러 버전의 모델명을 리스트로 준비합니다.
        model_names = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-pro"]
        
        # 사용 가능한 모델 하나를 선택
        model = None
        for name in model_names:
            try:
                temp_model = genai.GenerativeModel(name)
                # 실제로 작동하는지 가볍게 테스트
                temp_model.generate_content("test", generation_config={"max_output_tokens": 1})
                model = temp_model
                break # 성공하면 루프 탈출
            except:
                continue

        if model is None:
            st.error("사용 가능한 Gemini 모델을 찾을 수 없습니다. API 키 권한을 확인해주세요.")
        else:
            user_input = st.text_area("교정할 문장을 입력하세요:")

            if st.button("교정 실행"):
                if user_input.strip():
                    with st.spinner(f"AI 분석 중... (사용한 모델: {model.model_name})"):
                        prompt = f"다음 문장의 맞춤법과 발음을 교정해서 표로 보여줘: {user_input}"
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                else:
                    st.warning("내용을 입력해주세요.")

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
else:
    st.info("왼쪽 사이드바에 API Key를 입력해주세요.")
