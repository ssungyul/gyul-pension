import streamlit as st
import pandas as pd
import numpy as np

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="귤노션 - 썬귤이의 연금 시뮬레이터",
    page_icon="🍊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS DESIGN (귤노션 & 썬귤이 감성 톤앤매너 적용)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

/* 전체 배경: 따뜻하고 코지한 크림 베이지 톤 */
.stApp {
    background: #FDFBF7;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

header {
    visibility: hidden;
}

/* 상단 타이틀 카드 스타일 */
.top-banner {
    background: #FFFFFF;
    border: 1px solid #F0EBE1;
    border-radius: 20px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 4px 20px rgba(235, 180, 110, 0.06);
    margin-bottom: 24px;
}

.banner-title {
    font-size: 24px;
    font-weight: 800;
    color: #2D2A26;
    letter-spacing: -1px;
}

.banner-sub {
    font-size: 13px;
    color: #8C847A;
    margin-top: 4px;
}

/* 공통 카드 스타일 */
.dashboard-card {
    background: #FFFFFF;
    border: 1px solid #F0EBE1;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(235, 180, 110, 0.05);
    height: 100%;
}

.card-title {
    font-size: 15px;
    font-weight: 700;
    color: #4A443D;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* 입력 필드 레이블 디자인 */
label {
    font-weight: 600 !important;
    color: #5D554C !important;
    font-size: 13px !important;
}

/* 강조 머니 박스 */
.money-box-sub {
    background: #FFF9F0;
    border: 1px solid #FCEBD2;
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 12px;
}

.money-label {
    color: #8C847A;
    font-size: 12px;
    margin-bottom: 4px;
}

.money-value {
    font-size: 24px;
    font-weight: 800;
    color: #FF8A00;
    letter-spacing: -1px;
}

.money-value-dark {
    font-size: 24px;
    font-weight: 800;
    color: #38332E;
    letter-spacing: -1px;
}

/* 핵심 연금 결과 그라데이션 배너 (따뜻한 귤빛) */
.pension-hero {
    background: linear-gradient(135deg, #FF9500 0%, #FF6A00 100%);
    border-radius: 22px;
    padding: 34px 30px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 25px rgba(255, 149, 0, 0.22);
    margin-top: 24px;
    margin-bottom: 24px;
}

.pension-hero-small {
    font-size: 12px;
    opacity: 0.85;
    margin-bottom: 6px;
}

.pension-hero-title {
    font-size: 17px;
    font-weight: 600;
    margin-bottom: 6px;
}

.pension-hero-value {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.2;
}

.pension-hero-unit {
    font-size: 15px;
    font-weight: 600;
    margin-left: 4px;
}

.pension-hero-desc {
    margin-top: 12px;
    font-size: 11px;
    opacity: 0.8;
}

/* 섹션 타이틀 */
.section-header {
    font-size: 18px;
    font-weight: 700;
    color: #38332E;
    margin-top: 32px;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
}

/* 팁 박스 */
.tip-box {
    background: #FFFDF9;
    border: 1px solid #F5E8D3;
    border-radius: 14px;
    padding: 16px 20px;
    color: #7A6E5D;
    font-size: 12px;
    line-height: 1.6;
    margin-top: 24px;
    display: flex;
    align-items: center;
    gap: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# FUNCTIONS
# ============================================================
def future_value_monthly(current_asset, monthly_payment, annual_return, years):
    months = int(years * 12)
    monthly_rate = annual_return / 100 / 12
    if months <= 0:
        return current_asset
    if monthly_rate == 0:
        return current_asset + monthly_payment * months
    current_growth = current_asset * ((1 + monthly_rate) ** months)
    payment_growth = monthly_payment * (((1 + monthly_rate) ** months - 1) / monthly_rate)
    return current_growth + payment_growth

def calculate_principal(current_asset, monthly_payment, years):
    return current_asset + monthly_payment * years * 12

def calculate_pension_monthly(balance, annual_return, years):
    months = int(years * 12)
    if months <= 0:
        return 0
    monthly_rate = annual_return / 100 / 12
    if monthly_rate == 0:
        return balance / months
    return balance * (monthly_rate / (1 - (1 + monthly_rate) ** (-months)))

def format_money(value):
    value = float(value)
    if value >= 100_000_000:
        eok = value / 100_000_000
        if eok >= 10:
            return f"{eok:,.1f}억원"
        return f"{eok:,.2f}억원"
    elif value >= 10_000:
        man = value / 10_000
        return f"{man:,.0f}만원"
    else:
        return f"{value:,.0f}원"

# ============================================================
# TOP BANNER (BRAND IDENTITY)
# ============================================================
st.markdown("""
<div class="top-banner">
    <div>
        <div class="banner-title">🍊 귤노션 · 연금 플래너 시뮬레이터</div>
        <div class="banner-sub">코지하고 따뜻한 미래를 위해, 오늘의 자산을 똑똑하게 설계해보세요.</div>
    </div>
    <div style="font-size: 28px;">🌱🍊</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# INPUT & MAIN SUMMARY
# ============================================================
col_input, col_summary = W_cols = st.columns([1.1, 1], gap="large")

with col_input:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">⚙️ 연금 설계 조건 입력</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        current_age = st.number_input("현재 나이", min_value=18, max_value=80, value=34, step=1)
    with c2:
        retirement_age = st.number_input("은퇴 나이", min_value=30, max_value=90, value=60, step=1)

    current_asset = st.number_input("현재 연금/투자 자산 (원)", min_value=0, max_value=10_000_000_000, value=15_000_000, step=1_000_000, format="%d")
    monthly_payment = st.number_input("매월 적립 금액 (원)", min_value=0, max_value=50_000_000, value=600_000, step=50_000, format="%d")
    annual_return = st.slider("예상 연평균 수익률 (%)", min_value=0.0, max_value=15.0, value=7.0, step=0.5)
    
    st.markdown(f'<div style="background:#FFF9F0; border-radius:10px; padding:10px 14px; margin-top:8px; color:#A86C15; font-size:11px;">💡 연평균 <b style="color:#FF8A00;">{annual_return:.1f}%</b> 복리 성장을 기준으로 시뮬레이션합니다.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

years_to_retirement = max(retirement_age - current_age, 0)
final_balance = future_value_monthly(current_asset, monthly_payment, annual_return, years_to_retirement)
principal = calculate_principal(current_asset, monthly_payment, years_to_retirement)
profit = max(final_balance - principal, 0)
profit_ratio = (profit / final_balance * 100) if final_balance > 0 else 0

with col_summary:
    st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
    st.markdown('<div class="card-title">📈 은퇴 시점 자산 전망</div>', unsafe_allow_html=True)
    
    sc1, sc2 = st.columns(2, gap="medium")
    with sc1:
        st.markdown(f'''
        <div style="background:#FAF7F2; border-radius:14px; padding:16px;">
            <div class="money-label">총 투자 원금</div>
            <div class="money-value-dark">{format_money(principal)}</div>
            <div style="font-size:10px; color:#A39B90; margin-top:4px;">내가 직접 모은 금액</div>
        </div>
        ''', unsafe_allow_html=True)
    with sc2:
        st.markdown(f'''
        <div style="background:#FAF7F2; border-radius:14px; padding:16px;">
            <div class="money-label">예상 운용 수익</div>
            <div class="money-value">{format_money(profit)}</div>
            <div style="font-size:10px; color:#A39B90; margin-top:4px;">비중 {profit_ratio:.1f}%</div>
        </div>
        ''', unsafe_allow_html=True)

    st.markdown(f'''
    <div class="money-box-sub">
        <div class="money-label">🎯 {retirement_age}세 은퇴 시점 예상 총 적립액</div>
        <div class="money-value" style="margin-top:2px;">{format_money(final_balance)}</div>
    </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PENSION PAYOUT SETTINGS & HERO RESULT
# ============================================================
st.markdown('<div class="section-header">💰 매월 받을 수 있는 연금 수령액 시뮬레이션</div>', unsafe_allow_html=True)

pc1, pc2 = st.columns(2, gap="medium")
with pc1:
    receive_years = st.slider("은퇴 후 연금 수령 기간 (년)", min_value=10, max_value=40, value=30, step=1)
with pc2:
    post_retirement_return = st.slider("은퇴 후 자산 운용 수익률 (%)", min_value=0.0, max_value=8.0, value=3.0, step=0.5)

monthly_pension = calculate_pension_monthly(final_balance, post_retirement_return, receive_years)
principal_preserving = final_balance * (post_retirement_return / 100) / 12

st.markdown(f'''
<div class="pension-hero">
    <div class="pension-hero-small">🌱 썬귤이의 은퇴 플랜 · {retirement_age}세부터 {receive_years}년 동안 수령</div>
    <div class="pension-hero-title">매월 안정적으로 수령할 수 있는 예상 연금액</div>
    <div class="pension-hero-value">{monthly_pension:,.0f}<span class="pension-hero-unit">원 / 월</span></div>
    <div class="pension-hero-desc">은퇴 후 연 {post_retirement_return:.1f}% 복리 운용 및 원금 균등 소진 방식을 적용한 금액입니다.</div>
</div>
''', unsafe_allow_html=True)

# ============================================================
# DETAIL BREAKDOWN CARDS
# ============================================================
rc1, rc2, rc3 = st.columns(3, gap="medium")

with rc1:
    st.markdown(f'''
    <div class="dashboard-card">
        <div class="card-title">✨ 최종 적립액</div>
        <div style="font-size: 20px; font-weight: 800; color: #38332E; margin-top:6px;">{format_money(final_balance)}</div>
        <div style="font-size: 11px; color: #8C847A; margin-top: 6px; line-height:1.4;">은퇴 직전까지 달성하게 되는 총 연금 자산 규모입니다.</div>
    </div>
    ''', unsafe_allow_html=True)

with rc2:
    st.markdown(f'''
    <div class="dashboard-card">
        <div class="card-title">🛡️ 원금 보존형 수령액</div>
        <div style="font-size: 20px; font-weight: 800; color: #FF8A00; margin-top:6px;">{principal_preserving:,.0f}원</div>
        <div style="font-size: 11px; color: #8C847A; margin-top: 6px; line-height:1.4;">원금을 깎지 않고 이자 수익만 매월 타 쓰는 방식입니다.</div>
    </div>
    ''', unsafe_allow_html=True)

with rc3:
    st.markdown(f'''
    <div class="dashboard-card">
        <div class="card-title">⏳ 기간 소진형 수령액</div>
        <div style="font-size: 20px; font-weight: 800; color: #38332E; margin-top:6px;">{monthly_pension:,.0f}원</div>
        <div style="font-size: 11px; color: #8C847A; margin-top: 6px; line-height:1.4;">{receive_years}년 동안 원금과 수익을 모두 나누어 받는 방식입니다.</div>
    </div>
    ''', unsafe_allow_html=True)

# ============================================================
# GROWTH CHART
# ============================================================
st.markdown('<div class="section-header">📊 연금 자산 성장 추이 그래프</div>', unsafe_allow_html=True)

years = np.arange(0, years_to_retirement + 1)
balances = [future_value_monthly(current_asset, monthly_payment, annual_return, int(y)) for y in years]
chart_df = pd.DataFrame({"나이": current_age + years, "예상 자산": balances})

st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
st.line_chart(chart_df.set_index("나이"), height=320, color="#FF8A00")
st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER TIP
# ============================================================
st.markdown(f'''
<div class="tip-box">
    <span style="font-size: 16px;">🍊</span>
    <div>
        <b>귤노션 시뮬레이터 안내</b><br>
        현재 자산 <b>{format_money(current_asset)}</b>, 월 납입액 <b>{format_money(monthly_payment)}</b>을 바탕으로 계산되었습니다. 
        세금, 물가상승률 및 수수료는 반영되지 않은 참고용 시뮬레이션입니다. 오늘도 작은 실천으로 따뜻한 미래를 만들어가세요!
    </div>
</div>
''', unsafe_allow_html=True)
