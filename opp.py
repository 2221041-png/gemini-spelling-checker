import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI 맞춤법 검사기", page_icon="✍️")
st.title("✍️ AI 맞춤법 검사기")

# 1. 사이드바 API 키 입력
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        # API 설정
        genai.configure(api_key=api_key)
        
        # 2. 모델 설정 (가장 안정적인 호출 방식)
        # 404 에러 방지를 위해 이름을 'gemini-1.5-flash'로만 설정
        model = genai.GenerativeModel('gemini-1.5-flash')

        user_input = st.text_area("문장을 입력하세요:", placeholder="안녕하새요. 오늘은 날씨가 조으네요.")

        if st.button("검사 시작"):
            if user_input.strip():
                with st.spinner("AI 분석 중..."):
                    # 3. 답변 생성
                    prompt = f"다음 문장의 맞춤법과 표준 발음을 교정해서 표 형식으로 보여줘: {user_input}"
                    response = model.generate_content(prompt)
                    
                    st.success("분석 완료!")
                    st.markdown(response.text)
            else:
                st.warning("내용을 입력해주세요.")
                
    except Exception as e:
        # 에러 발생 시 사용자에게 친절하게 표시
        st.error(f"오류가 발생했습니다: {e}")
        st.info("API 키가 정확한지, 혹은 Google AI Studio에서 프로젝트가 활성화되었는지 확인해 보세요.")
else:
    st.info("왼쪽 사이드바에 Gemini API Key를 입력하면 시작할 수 있습니다.")
