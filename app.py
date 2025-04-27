import streamlit as st
import pandas as pd
import os
import time
from PIL import Image
from src.LLM_interface import analyze_with_gpt
import json
from pydantic import ValidationError
import openai

# 페이지 설정
st.set_page_config(
    page_title="슬기로운 월급생활",
    page_icon="💰",
    layout="centered"
)
# CSS
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

@keyframes fadeIn {
    0% {opacity: 0; transform: translateY(-20px);}
    100% {opacity: 1; transform: translateY(0);}
}

@keyframes floatAnimation {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
    100% { transform: translateY(0px); }
}

body {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 기본 배경 */
.stApp {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9f2ff 100%);
}

/* 버튼 */
.stButton > button {
    background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%);
    color: white;
    font-weight: bold;
    border-radius: 60px;
    padding: 1rem 2.5rem;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    transition: all 0.3s ease;
    border: none;
    font-size: 1.4rem;
    text-align: center;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #3B82F6 100%);
    box-shadow: 0 6px 10px rgba(37, 99, 235, 0.3);
    transform: translateY(-2px);
}

/* 특별 버튼 - 분석 시작 버튼 */
button[data-testid="baseButton-primary"] {
    font-size: 1.7rem !important;
    padding: 1.2rem 3rem !important;
    letter-spacing: 0.5px;
    font-weight: 700 !important;
}

/* 타이틀 텍스트 */
h1 {
    animation: fadeIn 1.5s ease-out;
    color: #0F172A;
    text-align: center;
    font-weight: 700;
    background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%);
    -webkit-background-clip: text;
    font-size: 3rem;
    padding: 1.5rem 0;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    letter-spacing: 1px;
    margin-bottom: 1rem;
    position: relative;
    display: inline-block;
    width: 100%;
}

h1::after {
    content: '';
    position: absolute;
    bottom: 0.8rem;
    left: 50%;
    transform: translateX(-50%);
    width: 400px;
    height: 3px;
    background: linear-gradient(135deg, #2563EB 0%, #60A5FA 100%);
    border-radius: 2px;
}

h2 {
    animation: fadeIn 2s ease-out;
    color: #0F172A;
    text-align: center;
    font-weight: 600;
}

h3 {
    color: #0F172A;
    text-align: center;
    font-weight: 500;
}

/* 파일 업로더 */
.stFileUploader > div:first-child {
    border: 2px dashed #3B82F6;
    border-radius: 10px;
    padding: 2rem;
    background-color: rgba(59, 130, 246, 0.05);
    transition: all 0.3s ease;
}

.stFileUploader > div:first-child:hover {
    background-color: rgba(59, 130, 246, 0.1);
    border-color: #2563EB;
}

/* 인포 메시지 */
.stAlert-info {
    background-color: #EFF6FF;
    color: #1E40AF;
    border-radius: 10px;
    border-left: 5px solid #3B82F6;
    padding: 1rem;
    margin: 1rem 0;
    animation: fadeIn 1s ease-out;
}

/* 성공 메시지 */
.stAlert-success {
    background-color: #ECFDF5;
    color: #047857;
    border-radius: 10px;
    border-left: 5px solid #10B981;
    padding: 1rem;
    margin: 1rem 0;
}

/* 진행 바 */
.stProgress > div > div {
    background-color: #3B82F6;
    border-radius: 10px;
}

.stProgress {
    height: 10px;
}

/* 엑스팬더 */
.streamlit-expanderHeader {
    background-color: #EFF6FF;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    color: #1E40AF;
    border: 1px solid #DBEAFE;
    transition: all 0.2s ease;
}

.streamlit-expanderHeader:hover {
    background-color: #DBEAFE;
}

.streamlit-expanderContent {
    border: 1px solid #DBEAFE;
    border-top: none;
    border-radius: 0 0 8px 8px;
    padding: 1rem;
    background-color: white;
}

/* 해시태그 */
.spending-type-hashtag {
    color: #2563EB;
    text-align: center;
    font-size: 1.2rem;
    font-weight: 500;
    margin-top: 0.5rem;
}

/* 결과 컨테이너 */
.spending-type-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    border: 2px solid #2563EB;
    border-radius: 15px;
    box-shadow: 0 10px 15px rgba(37, 99, 235, 0.1);
    padding: 2rem;
    margin: 2rem auto;
    max-width: 90%;
    transition: all 0.3s ease;
    animation: fadeIn 0.8s ease-out;
}

.spending-type-container:hover {
    box-shadow: 0 15px 20px rgba(37, 99, 235, 0.15);
    transform: translateY(-5px);
}

.spending-type-container h3 {
    margin-bottom: 0.5rem;
    font-size: 1.3rem;
    opacity: 0.9;
}

.spending-type-header {
    font-size: 2.5rem !important;
    font-weight: bold;
    color: #2563EB;
    font-family: 'Noto Sans KR', sans-serif;
    text-align: center;
    margin: 0.5rem 0 1rem 0;
    padding: 0.5rem 0;
    text-shadow: 1px 1px 3px rgba(37, 99, 235, 0.2);
}

/* 테이블 */
table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

thead tr {
    background-color: #EFF6FF;
    color: #1E40AF;
}

th, td {
    padding: 12px 15px;
    text-align: left;
    border-bottom: 1px solid #DBEAFE;
}

tbody tr:hover {
    background-color: #F8FAFC;
}

/* 응원 메시지 */
.encouragement-message {
    background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
    padding: 1.5rem;
    border-radius: 12px;
    border-left: 5px solid #3B82F6;
    margin: 1.5rem 0;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.1);
    position: relative;
    overflow: hidden;
}

.encouragement-message::before {
    content: '💙';
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 1.5rem;
    opacity: 0.2;
}

.encouragement-message h4 {
    color: #2563EB;
    margin-bottom: 1rem;
    font-size: 1.2rem;
    font-weight: 600;
}

/* 푸터 */
footer {
    text-align: center;
    padding: 1.5rem 0;
    font-size: 0.9rem;
    color: #6B7280;
    margin-top: 2rem;
}

/* 캐릭터 이미지 */
.character-image {
    animation: floatAnimation 3s ease-in-out infinite;
    filter: drop-shadow(0 10px 8px rgba(0, 0, 0, 0.04));
    margin: 1rem 0;
}

/* 체크리스트 아이템 */
.checklist-item {
    background-color: #FAFAFA;
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    border-left: 4px solid #3B82F6;
}

.difficulty {
    color: #F59E0B;
    font-size: 0.9rem;
}

.saving {
    color: #10B981;
    font-weight: 500;
}

/* 카드 스타일 */
.card {
    background-color: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    padding: 1.5rem;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.card:hover {
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    transform: translateY(-3px);
}

/* 로딩 스피너 */
.stSpinner > div {
    border-color: #3B82F6 !important;
}
</style>
"""

# 스트림릿에 적용
st.markdown(custom_css, unsafe_allow_html=True)

# Streamlit 세션 상태 초기화
if 'model' not in st.session_state:
    st.session_state.model = "gpt-4.1-mini"
if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'spending_type' not in st.session_state:
    st.session_state.spending_type = None
if 'gpt_response' not in st.session_state:
    st.session_state.gpt_response = None
if 'df' not in st.session_state:
    st.session_state.df = None



# 소비 유형 정의
SPENDING_TYPES = {
    "절약형": "saver.png",
    "균형형": "balancer.png",
    "플렉스형": "flexer.png",
    # 나머지 13가지 유형은 추가 이미지가 준비되면 추가
}

def analyze_spending_pattern(df):
    """
    소비 패턴을 분석하여 유형을 반환하는 함수
    실제 구현에서는 더 복잡한 규칙 또는 AI 모델 활용
    """
    # 간단한 예시 규칙 (실제로는 더 복잡한 분석 필요)
    try:
        # 카테고리별 지출 비율 계산 (카테고리 컬럼이 있다고 가정)
        if '카테고리' in df.columns or '분류' in df.columns:
            category_col = '카테고리' if '카테고리' in df.columns else '분류'
            category_spending = df.groupby(category_col).sum().reset_index()
            
            # 여기서는 간단한 예시 규칙으로 구현
            # 실제로는 더 복잡한 분류 로직 구현 필요
            food_spending = category_spending[category_spending[category_col].str.contains('식비|음식|카페', na=False)]
            shopping_spending = category_spending[category_spending[category_col].str.contains('쇼핑|의류|가전', na=False)]
            
            if food_spending.empty and shopping_spending.empty:
                return "균형형"
            
            total_spending = df['금액'].sum() if '금액' in df.columns else 0
            
            # 식비 비중이 30% 이상이면 "플렉스형"
            if not food_spending.empty:
                food_ratio = food_spending['금액'].sum() / total_spending if total_spending > 0 else 0
                if food_ratio > 0.3:
                    return "플렉스형"
            
            # 쇼핑 비중이 낮으면 "절약형"
            if not shopping_spending.empty:
                shopping_ratio = shopping_spending['금액'].sum() / total_spending if total_spending > 0 else 0
                if shopping_ratio < 0.1:
                    return "절약형"
        
        # 기본값
        return "균형형"
    except Exception as e:
        st.error(f"분석 중 오류가 발생했습니다: {e}")
        return "균형형"  # 기본값


# 제목
image = Image.open("images/제목.png")
st.image(image, use_column_width=True)



# 메인 화면
st.write("## 나의 지출 내역을 업로드하면 소비 패턴을 한 눈에!")
# 파일 업로드 위젯
uploaded_file = st.file_uploader("", type=["xlsx", "csv"])


# 시스템 프롬프트 가져오기 (설정 탭에서 저장된 값)

# 파일이 업로드되면 자동으로 데이터프레임 생성
if uploaded_file is not None and not st.session_state.analyzing and not st.session_state.analysis_complete:
    # 데이터 미리보기
    try:
        # 데이터 로드
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:  # .xlsx 파일
            df = pd.read_excel(uploaded_file)
        
        # 세션에 데이터프레임 저장
        st.session_state.df = df
        with st.expander("데이터 미리보기"):
            if st.session_state.df is not None:
                st.dataframe(st.session_state.df.head())

        # 분석 시작 버튼
        col1, col2, col3 = st.columns([7, 5, 7])
        with col2:
            if st.button("분석 시작", use_container_width=True, key="start_analysis_button"):
                st.session_state.analyzing = True
                st.rerun()
    
    except Exception as e:
        st.error(f"파일 처리 중 오류가 발생했습니다: {e}")
    

# 분석 중일 때
if st.session_state.analyzing and not st.session_state.analysis_complete:
    # 분석 진행 표시
    with st.expander("데이터 미리보기"):
        if st.session_state.df is not None:
            st.dataframe(st.session_state.df.head())
    with st.spinner("소비 패턴을 분석 중입니다..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.03)  # 약 2초 동안 진행
            progress_bar.progress(i + 1)
        
        # GPT를 이용한 분석
        spending_type, gpt_response = analyze_with_gpt(st.session_state.df)
        print(gpt_response)
        
        # 세션 상태에 결과 저장
        st.session_state.spending_type = spending_type
        st.session_state.gpt_response = gpt_response
        st.session_state.analyzing = False
        st.session_state.analysis_complete = True
        
        # 페이지 새로고침 (결과 화면 표시용)
        st.rerun()

# 분석 결과 표시
if st.session_state.analysis_complete:
    st.divider()  # 구분선 추가
    
    # 결과 콘테이너
    result_container = st.container()
    
    with result_container:
        # 결과 표시
        hashtag = st.session_state.gpt_response['해시태그']
        st.success("분석이 완료되었습니다!")
        st.markdown(f"""<div class="spending-type-container"> 
                    <h3 style='text-align: center;'>당신의 소비 유형은</h3>
                    <h3 class="spending-type-header" style="text-align: center;">"{st.session_state.spending_type}"</h3>
                    <h4 class="spending-type-hashtag" style='text-align: center;'>{hashtag}</h4>
                    </div>""", unsafe_allow_html=True)
        
        # 이미지 파일 경로
        image_path = os.path.join("images/", st.session_state.spending_type + ".png")
        
        # 이미지 파일 존재 여부 확인
        if os.path.exists(image_path):
            image = Image.open(image_path)
            col1, col2, col3 = st.columns([1, 6, 1])
            with col2:  # 가운데 열에 이미지 배치
                st.markdown("<div class='character-image'>", unsafe_allow_html=True)
                st.image(image, width=400, use_column_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning(f"이미지 파일({image_path})을 찾을 수 없습니다.")
        
        # GPT 응답 표시
        if st.session_state.gpt_response:
            try:
                # 각 버튼에 대한 세션 상태 초기화
                if 'show_소비_유형_분석_결과' not in st.session_state:
                    st.session_state.show_소비_유형_분석_결과 = False
                if 'show_지출_패턴_분석' not in st.session_state:
                    st.session_state.show_지출_패턴_분석 = False
                if 'show_재정_건전성_평가' not in st.session_state:
                    st.session_state.show_재정_건전성_평가 = False
                if 'show_맞춤형_조언' not in st.session_state:
                    st.session_state.show_맞춤형_조언 = False
                if 'show_소비_습관_개선_체크리스트' not in st.session_state:
                    st.session_state.show_소비_습관_개선_체크리스트 = False
                if 'show_목표_문구' not in st.session_state:
                    st.session_state.show_목표_문구 = False
                if 'show_응원_메시지' not in st.session_state:
                    st.session_state.show_응원_메시지 = False
                if 'show_과소비_영역_탐지' not in st.session_state:
                    st.session_state.show_과소비_영역_탐지 = False
                if 'show_맞춤_재정_플랜' not in st.session_state:
                    st.session_state.show_맞춤_재정_플랜 = False
                
                # 각 항목을 expander로 표시
                with st.expander("✨ 소비 유형 분석 결과"):
                    if '소비_유형_분석_결과' in st.session_state.gpt_response:
                        st.markdown(st.session_state.gpt_response['소비_유형_분석_결과'], unsafe_allow_html=True)

                with st.expander("📊 지출 패턴 분석"):
                    if '지출_패턴_분석' in st.session_state.gpt_response:
                        st.write(st.session_state.gpt_response['지출_패턴_분석'])
                        
                with st.expander("💵 재정 건전성 평가"):
                    if '재정_건전성_평가' in st.session_state.gpt_response:
                        st.write(st.session_state.gpt_response['재정_건전성_평가'])
                
                with st.expander("💡 맞춤형 조언"):
                    if '맞춤형_조언' in st.session_state.gpt_response:
                        st.write(st.session_state.gpt_response['맞춤형_조언'])
                
                with st.expander("✅ 소비 습관 개선 체크리스트"):
                    if '소비_습관_개선_체크리스트' in st.session_state.gpt_response:
                        checklist_content = st.session_state.gpt_response['소비_습관_개선_체크리스트']
                        # 체크리스트 항목에 스타일 적용
                        checklist_content = checklist_content.replace("[ ]", "☐")
                        st.write(checklist_content)
                
                with st.expander("🎯 목표 문구"):
                    if '목표_문구' in st.session_state.gpt_response:
                        st.write(st.session_state.gpt_response['목표_문구'])
                
                with st.expander("⚠️ 과소비 영역 탐지"):
                    if '과소비_영역_탐지' in st.session_state.gpt_response:
                        st.write(st.session_state.gpt_response['과소비_영역_탐지'])
                
                with st.expander("📆 맞춤 재정 플랜"):
                    if '맞춤_재정_플랜' in st.session_state.gpt_response:
                        st.write(st.session_state.gpt_response['맞춤_재정_플랜'])

                with st.expander("💌 응원 메시지"):
                    if '응원_메시지' in st.session_state.gpt_response:
                        st.markdown(f"""
                        <div class="encouragement-message">
                            <h4>💌 응원의 한마디</h4>
                            {st.session_state.gpt_response['응원_메시지']}
                        </div>
                        """, unsafe_allow_html=True)
            except Exception as e:
                st.write(st.session_state.gpt_response)
        
        # 다시 분석하기 버튼
        st.markdown("<div style='text-align: center; margin-top: 2rem;'>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([7, 5, 7])
        with col2:
            if st.button("다시 분석하기", use_container_width=True, key="analyze_again_button"):
                st.session_state.analysis_complete = False
                st.session_state.analyzing = False
                st.session_state.spending_type = None
                st.session_state.gpt_response = None
                st.session_state.df = None
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    # st.write(st.session_state.gpt_response)
# 파일이 업로드되지 않았을 때는 안내 메시지만 표시
if uploaded_file is None and not st.session_state.analyzing and not st.session_state.analysis_complete:
    st.markdown("<div style='text-align: center; margin-top: 2rem;'>", unsafe_allow_html=True)
    st.info("👆 엑셀 또는 CSV 파일을 업로드해주세요.")
    st.markdown("""
    <div style='margin-top: 2rem; text-align: center;'>
        <p style='color: #6B7280; margin-top: 1rem;'>지출 내역을 분석하여 소비 패턴을 파악해보세요!</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 푸터
st.markdown("---")
st.markdown("<footer>© 2023 슬기로운 월급생활 | Made with ❤️ using Streamlit</footer>", unsafe_allow_html=True) 
