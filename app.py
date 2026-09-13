import streamlit as st
import pandas as pd
import numpy as np

# 페이지 기본 설정
st.set_page_config(
    page_title="귤노션 | 따뜻한 노후연금 시뮬레이터",
    page_icon="🍊",
    layout="wide"
)

# 따뜻하고 코지한 감성의 CSS 스타일 적용
st.markdown("""
<style>
    .main {
        background-color: #FAF8F5;
    }
    .stSidebar {
        background-color: #F4EFEB;
    }
    h1, h2, h3 {
        color: #4A3B32;
        font-family: 'Malgun Gothic', sans-serif;
    }
    .metric-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E6DFD5;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀 섹션
st.title("🍊 귤노션 | 한눈에 보는 노후연금 시뮬레이터")
st.markdown("은퇴 후의 든든한 현금흐름을 코지하고 직관적으로 설계해보세요.")
st.markdown("---")

# 사이드바 (시뮬레이션 설정)
st.sidebar.header("🛠️ 시뮬레이션 설정")

current_age = st.sidebar.slider("현재 나이", min_value=20, max_value=60, value=30, step=1)
target_retire_age = st.sidebar.slider("목표 은퇴 연령", min_value=50, max_value=70, value=60, step=1)
monthly_saving = st.sidebar.slider("사적연금 월 저축액 (연저펀·IRP)", min_value=10, max_value=300, value=100, step=10, format="%d만원")
current_asset = st.sidebar.slider("현재 사적연금 적립액", min_value=0, max_value=20000, value=1000, step=100, format="%d만원")
annual_return = st.sidebar.slider("예상 투자 수익률 (연)", min_value=1.0, max_value=12.0, value=7.0, step=0.5, format="%.1f%%")

st.sidebar.markdown("---")
inflation_mode = st.sidebar.checkbox("📉 물가상승률 반영 (실질 가치)", value=True)
inflation_rate = 2.0
if inflation_mode:
    inflation_rate = st.sidebar.slider("연간 물가상승률", min_value=1.0, max_value=5.0, value=2.0, step=0.5, format="%.1f%%")

# 계산 로직
saving_months = (target_retire_age - current_age) * 12
r = (annual_return / 100) / 12
pv = current_asset * 10000
pmt = monthly_saving * 10000

# 복리 계산 (은퇴 시점 총 자산)
if r > 0:
    future_value = pv * ((1 + r) ** saving_months) + pmt * (((1 + r) ** saving_months - 1) / r)
else:
    future_value = pv + pmt * saving_months

# 물가상승률 반영 (현재 가치로 환산)
if inflation_mode:
    deflator = (1 + inflation_rate / 100) ** (target_retire_age - current_age)
    effective_future_value = future_value / deflator
else:
    effective_future_value = future_value

# 사적연금 월 수령액 추정 (20년 수령 기준 단순 환산)
monthly_private_pension = (effective_future_value / (20 * 12)) / 10000

# 국민연금 (가입기간에 따른 고정 추정치 부여)
national_pension = 95 + max(0, (target_retire_age - 60) * 5)
if inflation_mode:
    national_pension = national_pension / ((1 + inflation_rate / 100) ** max(0, 65 - current_age))

total_monthly_pension = national_pension + monthly_private_pension

# 결과 대시보드 출력
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #8C7B70; font-size: 14px; margin-bottom: 5px;">국민연금 (월)</p>
        <h3 style="color: #D97706; margin: 0;">{int(national_pension):,}만원</h3>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #8C7B70; font-size: 14px; margin-bottom: 5px;">사적연금 (월)</p>
        <h3 style="color: #D97706; margin: 0;">{int(monthly_private_pension):,}만원</h3>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <p style="color: #8C7B70; font-size: 14px; margin-bottom: 5px;">은퇴 후 총 현금흐름 (월)</p>
        <h3 style="color: #C2410C; margin: 0;">{int(total_monthly_pension):,}만원</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 자산 추이 시각화 그래프 데이터 생성
ages = list(range(current_age, target_retire_age + 26))
asset_trajectory = []

for age in ages:
    if age <= target_retire_age:
        m = (age - current_age) * 12
        if r > 0:
            val = pv * ((1 + r) ** m) + pmt * (((1 + r) ** m - 1) / r)
        else:
            val = pv + pmt * m
        if inflation_mode:
            val = val / ((1 + inflation_rate / 100) ** (age - current_age))
        asset_trajectory.append(val / 10000)
    else:
        remaining_months = (age - target_retire_age) * 12
        withdrawn = (effective_future_value - (effective_future_value / (20 * 12)) * remaining_months)
        val = max(0, withdrawn)
        asset_trajectory.append(val / 10000)

chart_df = pd.DataFrame({"나이": [f"{a}세" for a in ages], "자산": asset_trajectory})
chart_df.set_index("나이", inplace=True)

st.subheader("📈 은퇴 전후 자산 추이 시뮬레이션")
st.line_chart(chart_df, color="#F97316")

# 하단 홍보 및 배너 영역
st.markdown("---")
st.markdown("""
<div style="background-color: #FFFBEB; padding: 20px; border-radius: 12px; border: 1px solid #FDE68A; text-align: center;">
    <h4 style="color: #92400E; margin-bottom: 5px;">🍊 더 완벽한 자산 관리를 원하신다면?</h4>
    <p style="color: #78350F; font-size: 14px; margin-bottom: 15px;">인스타그램 추천 TOP 2! 귤노션 한눈에 보는 가계부 템플릿과 함께 체계적인 저축 습관을 만들어보세요.</p>
    <a href="https://notion.so" target="_blank" style="background-color: #F59E0B; color: white; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; font-size: 14px;">귤노션 템플릿 보러가기 🚀</a>
</div>
""", unsafe_allow_html=True)
