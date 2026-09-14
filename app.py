import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="귤노션 | 노후 연금 시뮬레이터",
    page_icon="🍊",
    layout="wide"
)

# 따뜻하고 코지한 귤노션 감성 CSS 적용
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-10-21@1.0/MaruBuri-Regular.woff');
    
    .main, h1, h2, h3, p, span, div, label {
        font-family: 'MaruBuri-Regular', 'Malgun Gothic', sans-serif !important;
    }
    .main {
        background-color: #FFFDF9;
    }
    h1, h2, h3 {
        color: #4A3B32;
    }
    .metric-card {
        background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%);
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #FDE68A;
        box-shadow: 0 4px 10px rgba(245, 158, 11, 0.05);
        text-align: center;
    }
    .stButton>button {
        background-color: #F59E0B;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        padding: 10px 0px;
    }
    .stButton>button:hover {
        background-color: #D97706;
        color: white;
    }
    /* 상세설정 토글 버튼 스타일링 */
    .toggle-btn > button {
        background-color: #FFFBEB !important;
        color: #92400E !important;
        border: 1px solid #FDE68A !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        text-align: left !important;
        width: 100% !important;
    }
    .toggle-btn > button:hover {
        background-color: #FEF3C7 !important;
        color: #78350F !important;
    }
</style>
""", unsafe_allow_html=True)

# 세션 상태를 이용해 상세 설정 열닫힘 관리
if 'show_detail' not in st.session_state:
    st.session_state.show_detail = False

# 타이틀 섹션
st.markdown("""
    <h1 style='margin-bottom: 0px;'>🍊 귤노션 | 노후 연금 시뮬레이터 <span style='font-size: 16px; color: #D97706; font-weight: normal;'>by ssungyul</span></h1>
    <p style='color: #78350F; font-size: 16px; margin-top: 5px;'>은퇴 후의 든든한 현금흐름을 코지하고 직관적으로 설계해보세요.</p>
""", unsafe_allow_html=True)
st.markdown("---")

# 화면을 좌우로 나누기 (왼쪽: 결과 및 그래프 / 오른쪽: 설정 패널)
left_col, right_col = st.columns([1.4, 1])

with right_col:
    st.subheader("🛠️ 시뮬레이션 설정")
    
    # 필수 입력 항목
    current_age = st.number_input("현재 나이 (만 나이)", min_value=20, max_value=60, value=30, step=1)
    target_retire_age = st.number_input("은퇴 나이 (은퇴 예정 나이)", min_value=50, max_value=70, value=60, step=1)
    
    # 1000단위 콤마 입력을 위한 텍스트 처리 방식
    current_asset_str = st.text_input("초기 자금 (원) [이미 보유한 자산]", value="10,000,000")
    monthly_saving_str = st.text_input("월 납입액 (원) [매월 정기 납입할 금액]", value="1,000,000")
    
    # 문자열 콤마 제거 후 숫자로 변환
    try:
        current_asset = int(current_asset_str.replace(",", "").strip())
    except:
        current_asset = 0
        
    try:
        monthly_saving = int(monthly_saving_str.replace(",", "").strip())
    except:
        monthly_saving = 0

    st.markdown("---")

    # [수정됨] 엉킴 현상 없는 커스텀 삼각형 토글 버튼 구현
    toggle_icon = "▼" if st.session_state.show_detail else "▶"
    if st.button(f"{toggle_icon} 상세 설정 (수익률 및 수령기간 조절)", use_container_width=True):
        st.session_state.show_detail = not st.session_state.show_detail
        st.rerun()

    # 기본값 설정
    annual_return = 7.0
    pension_term = 20

    # [수정됨] 토글이 열렸을 때만 노란색 배경 박스 안에 슬라이더 배치
    if st.session_state.show_detail:
        st.markdown("""
        <div style='background-color: #FFFBEB; padding: 18px; border-radius: 12px; border: 1px solid #FDE68A; margin-top: 10px; margin-bottom: 10px;'>
        """, unsafe_allow_html=True)
        
        annual_return = st.slider("연복리 수익률 (%)", min_value=1.0, max_value=12.0, value=7.0, step=0.5, format="%.1f%%")
        pension_term = st.slider("연금 수령 기간 (년)", min_value=10, max_value=30, value=20, step=1, format="%d년")
        
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # 물가상승률 설정
    inflation_mode = st.checkbox("📉 물가상승률 반영 (실질 가치)", value=True)
    inflation_rate = 2.0
    if inflation_mode:
        inflation_rate = st.slider("연간 물가상승률 (%)", min_value=1.0, max_value=5.0, value=2.0, step=0.5, format="%.1f%%")

    st.markdown("<br>", unsafe_allow_html=True)
    calculate_btn = st.button("연금 계산하기 🍊", use_container_width=True)

with left_col:
    # 계산 로직
    saving_months = max(0, (target_retire_age - current_age) * 12)
    r = (annual_return / 100) / 12
    pv = float(current_asset)
    pmt = float(monthly_saving)

    # 복리 계산 (은퇴 시점 총 자산)
    if r > 0:
        future_value = pv * ((1 + r) ** saving_months) + pmt * (((1 + r) ** saving_months - 1) / r)
    else:
        future_value = pv + pmt * saving_months

    # 물가상승률 반영 (현재 가치로 환산)
    if inflation_mode:
        deflator = (1 + inflation_rate / 100) ** max(0, (target_retire_age - current_age))
        effective_future_value = future_value / deflator
    else:
        effective_future_value = future_value

    # 사적연금 월 수령액 추정
    total_months = pension_term * 12
    monthly_private_pension = (effective_future_value / total_months) / 10000 if total_months > 0 else 0

    # 국민연금 추정치
    national_pension = 95 + max(0, (target_retire_age - 60) * 5)
    if inflation_mode:
        national_pension = national_pension / ((1 + inflation_rate / 100) ** max(0, 65 - current_age))

    total_monthly_pension = national_pension + monthly_private_pension

    # 결과 대시보드 카드 출력
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #92400E; font-size: 13px; margin-bottom: 5px; font-weight: bold;">국민연금 (월)</p>
            <h3 style="color: #D97706; margin: 0; font-size: 20px;">{int(national_pension):,}만원</h3>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p style="color: #92400E; font-size: 13px; margin-bottom: 5px; font-weight: bold;">사적연금 (월)</p>
            <h3 style="color: #D97706; margin: 0; font-size: 20px;">{int(monthly_private_pension):,}만원</h3>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%); border: 1px solid #F59E0B;">
            <p style="color: #78350F; font-size: 13px; margin-bottom: 5px; font-weight: bold;">총 현금흐름 (월)</p>
            <h3 style="color: #B45309; margin: 0; font-size: 20px;">{int(total_monthly_pension):,}만원</h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 자산 추이 시각화 그래프 데이터 생성 (X축 '세' 단위 포함)
    ages = list(range(int(current_age), int(target_retire_age) + pension_term + 1))
    asset_trajectory = []

    for age in ages:
        if age <= target_retire_age:
            m = (age - current_age) * 12
            if r > 0:
                val = pv * ((1 + r) ** m) + pmt * (((1 + r) ** m - 1) / r)
            else:
                val = pv + pmt * m
            if inflation_mode:
                val = val / ((1 + inflation_rate / 100) ** max(0, age - current_age))
            asset_trajectory.append(val / 10000)
        else:
            elapsed_retire_months = (age - target_retire_age) * 12
            withdrawn = (effective_future_value - ((effective_future_value / total_months) * elapsed_retire_months))
            val = max(0, withdrawn)
            asset_trajectory.append(val / 10000)

    chart_df = pd.DataFrame({"자산 (만원)": asset_trajectory}, index=[f"{a}세" for a in ages])

    st.subheader("📈 은퇴 전후 자산 추이 시뮬레이션")
    st.line_chart(chart_df, color="#F59E0B")

# 하단 홍보 및 배너 영역 (노션 템플릿 링크 연결)
st.markdown("---")
st.markdown("""
<div style="background-color: #FFFBEB; padding: 20px; border-radius: 14px; border: 1px solid #FDE68A; text-align: center;">
    <h4 style="color: #92400E; margin-bottom: 5px;">🍊 더 완벽한 자산 관리를 원하신다면?</h4>
    <p style="color: #78350F; font-size: 14px; margin-bottom: 15px;">인스타그램 추천 TOP 2! 귤노션 한눈에 보는 가계부 템플릿과 함께 체계적인 저축 습관을 만들어보세요.</p>
    <a href="https://notion.so" target="_blank" style="background-color: #F59E0B; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px;">귤노션 템플릿 보러가기 🚀</a>
</div>
""", unsafe_allow_html=True)
