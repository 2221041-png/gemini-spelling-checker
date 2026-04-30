import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="AI 맞춤법 & 발음 교정기", page_icon="✍️")
st.title("✍️ AI 맞춤법 & 발음 교정기")
st.markdown("문장을 입력하면 Gemini AI가 맞춤법과 올바른 발음을 교정해 드립니다.")

# 2. Gemini API 키 설정 (Streamlit Secrets 사용 권장)
# 로컬 테스트 시에는 'YOUR_API_KEY'에 직접 입력하세요.
api_key = st.sidebar.text_input("Gemini API Key를 입력하세요", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 3. 사용자 입력
    user_input = st.text_area("교정할 문장을 입력하세요:", placeholder="예: 아버지가방에들어가신다. 오늘은 날씨가 참 조으네요.")

    if st.button("교정 시작"):
        if user_input.strip():
            with st.spinner("AI가 문장을 분석 중입니다..."):
                # Gemini에게 보낼 프롬프트
                prompt = f"""
                다음 문장의 맞춤법, 띄어쓰기, 그리고 한국어 표준 발음을 교정해줘.
                결과는 반드시 아래의 표 형식(Markdown Table)으로 출력해줘.
                
                1. 교정된 문장
                2. 틀린 부분 및 이유 (간략하게)
                3. 표준 발음 (한글로 표기)

                문장: "{user_input}"
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.success("분석 완료!")
                    st.markdown("### 📋 분석 결과")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
        else:
            st.warning("문장을 입력해 주세요.")
else:
    st.info("왼쪽 사이드바에 Gemini API 키를 입력해 주세요. (Google AI Studio에서 발급 가능)")

# 하단 정보
st.divider()
st.caption("Powered by Google Gemini 1.5 Flash & Streamlit")