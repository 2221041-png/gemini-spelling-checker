import streamlit as st
import google.generativeai as genai

# 페이지 설정
st.set_page_config(page_title="AI 맞춤법 검사기", page_icon="✨")
st.title("✨ AI 맞춤법 & 발음 교정기")

# 사이드바에서 API 키 입력
api_key = st.sidebar.text_input("Gemini API Key", type="password")

if api_key:
    try:
        # API 구성
        genai.configure(api_key=api_key)
        
        # [수정 포인트] 모델 호출 방식을 가장 명확하게 변경
        # 경로 없이 이름만 입력하거나, 지원되는 정확한 모델명을 사용합니다.
        model = genai.GenerativeModel('gemini-1.5-flash')

        user_input = st.text_area("교정할 문장을 입력하세요:", placeholder="예: 아버지가방에들어가신다. 날씨가 참 조으네요.")

        if st.button("교정 실행"):
            if user_input.strip():
                with st.spinner("AI가 문장을 분석하고 있습니다..."):
                    # 프롬프트 설정
                    prompt = f"""
                    입력된 문장의 맞춤법, 띄어쓰기, 표준 발음을 교정해줘.
                    반드시 아래 형식의 표(Table)로 출력해줘.
                    
                    | 구분 | 내용 |
                    | :--- | :--- |
                    | **교정 문장** | (교정된 결과) |
                    | **틀린 이유** | (어떤 부분이 왜 틀렸는지 설명) |
                    | **표준 발음** | (올바른 한국어 발음) |

                    문장: "{user_input}"
                    """
                    
                    # 콘텐츠 생성
                    response = model.generate_content(prompt)
                    
                    # 결과 출력
                    st.success("분석 완료!")
                    st.markdown(response.text)
            else:
                st.warning("내용을 입력해 주세요.")
                
    except Exception as e:
        # 에러 메시지를 구체적으로 확인하기 위한 출력
        st.error(f"오류가 발생했습니다: {e}")
        st.info("API 키가 올바른지, 혹은 Google AI Studio에서 'Gemini 1.5 Flash' 모델이 활성화되었는지 확인하세요.")
else:
    st.info("왼쪽 사이드바에 Gemini API Key를 입력하면 시작할 수 있습니다.")
