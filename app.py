import streamlit as st
import pandas as pd
import numpy as np
import math

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="노후 연금 시뮬레이터",
    page_icon="🟣",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background: #F8F7FB;
}

.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

header {
    visibility: hidden;
}


/* =========================
   HEADER
========================= */

.main-title {
    font-size: 30px;
    font-weight: 800;
    color: #20202A;
    letter-spacing: -1.5px;
    margin-bottom: 4px;
}

.sub-title {
    font-size: 14px;
    color: #8A8994;
    margin-bottom: 28px;
}


/* =========================
   COMMON
========================= */

.card {
    background: #FFFFFF;
    border: 1px solid #EEEAF5;
    border-radius: 20px;
    padding: 24px 26px;
    box-shadow: 0 3px 16px rgba(53, 45, 83, 0.035);
}

.card-title {
    font-size: 17px;
    font-weight: 700;
    color: #272631;
    margin-bottom: 18px;
}

.section-title {
    font-size: 19px;
    font-weight: 700;
    color: #292732;
    margin-top: 34px;
    margin-bottom: 14px;
    letter-spacing: -0.5px;
}

.section-title span {
    color: #9C98A5;
    font-size: 12px;
    font-weight: 400;
    margin-left: 6px;
}


/* =========================
   INPUT
========================= */

.input-card {
    background: #FFFFFF;
    border: 1px solid #EEEAF5;
    border-radius: 20px;
    padding: 24px 26px 18px 26px;
    box-shadow: 0 3px 16px rgba(53, 45, 83, 0.035);
}

.input-section-title {
    font-size: 17px;
    font-weight: 700;
    color: #282631;
    margin-bottom: 4px;
}

.input-section-desc {
    font-size: 12px;
    color: #9895A0;
    margin-bottom: 18px;
}

div[data-baseweb="input"] {
    border-radius: 10px;
}

div[data-baseweb="select"] > div {
    border-radius: 10px;
}


/* =========================
   MONEY CARDS
========================= */

.money-card {
    background: #FFFFFF;
    border: 1px solid #EEEAF5;
    border-radius: 18px;
    padding: 21px 22px;
    height: 100%;
}

.money-label {
    color: #8D8A95;
    font-size: 12px;
    margin-bottom: 8px;
}

.money-value {
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -1px;
}

.principal {
    color: #34313C;
}

.profit {
    color: #7657D9;
}

.money-desc {
    font-size: 11px;
    color: #9D99A5;
    margin-top: 6px;
}


/* =========================
   TOTAL
========================= */

.total-box {
    background: #F7F3FF;
    border-radius: 14px;
    padding: 16px 18px;
    margin-top: 13px;
}

.total-label {
    font-size: 12px;
    color: #7F7694;
}

.total-value {
    color: #6445C3;
    font-size: 23px;
    font-weight: 800;
    margin-top: 3px;
}


/* =========================
   MAIN PENSION RESULT
========================= */

.pension-result {
    background: linear-gradient(
        135deg,
        #7655D7 0%,
        #6845C6 100%
    );
    border-radius: 22px;
    padding: 34px 30px 31px 30px;
    text-align: center;
    color: white;
    box-shadow: 0 10px 28px rgba(106, 72, 200, 0.16);
}

.pension-small {
    font-size: 12px;
    opacity: 0.78;
    margin-bottom: 8px;
}

.pension-title {
    font-size: 17px;
    font-weight: 500;
    margin-bottom: 5px;
}

.pension-value {
    font-size: 43px;
    font-weight: 800;
    letter-spacing: -2px;
    line-height: 1.15;
}

.pension-unit {
    font-size: 15px;
    font-weight: 500;
    margin-left: 4px;
}

.pension-info {
    margin-top: 15px;
    font-size: 11px;
    opacity: 0.72;
}


/* =========================
   RESULT CARDS
========================= */

.result-card {
    background: #FFFFFF;
    border: 1px solid #EEEAF5;
    border-radius: 18px;
    padding: 21px 20px;
    height: 100%;
}

.result-label {
    color: #85818D;
    font-size: 12px;
    margin-bottom: 9px;
}

.result-value {
    color: #27252E;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.7px;
}

.result-unit {
    font-size: 12px;
    color: #8F8B96;
    margin-left: 2px;
}

.result-desc {
    color: #AAA6B0;
    font-size: 11px;
    margin-top: 8px;
    line-height: 1.5;
}


/* =========================
   GOAL REVERSE CALCULATOR
========================= */

.goal-box {
    background: #FFFFFF;
    border: 1px solid #E9E2F8;
    border-radius: 22px;
    padding: 27px 28px 25px 28px;
    box-shadow: 0 5px 20px rgba(53, 45, 83, 0.04);
}

.goal-header {
    display: flex;
    align-items: center;
    gap: 9px;
    margin-bottom: 5px;
}

.goal-icon {
    font-size: 22px;
}

.goal-title {
    font-size: 19px;
    font-weight: 700;
    color: #292732;
}

.goal-desc {
    font-size: 12px;
    color: #96929F;
    margin-bottom: 20px;
}

.goal-highlight {
    background: #F7F3FF;
    border-radius: 15px;
    padding: 18px 20px;
    margin-top: 17px;
}

.goal-highlight-label {
    color: #807594;
    font-size: 12px;
}

.goal-highlight-value {
    color: #6847C8;
    font-size: 27px;
    font-weight: 800;
    margin-top: 4px;
    letter-spacing: -1px;
}

.goal-result {
    background: #FCFBFE;
    border: 1px solid #EEEAF5;
    border-radius: 17px;
    padding: 20px;
    height: 100%;
}

.goal-result-label {
    font-size: 12px;
    color: #85818D;
    margin-bottom: 8px;
}

.goal-result-value {
    font-size: 23px;
    font-weight: 800;
    color: #282630;
    letter-spacing: -0.8px;
}

.goal-result-desc {
    font-size: 11px;
    color: #9995A1;
    line-height: 1.55;
    margin-top: 8px;
}


/* =========================
   CHART
========================= */

.chart-card {
    background: #FFFFFF;
    border: 1px solid #EEEAF5;
    border-radius: 20px;
    padding: 22px 25px 10px 25px;
}


/* =========================
   NOTICE
========================= */

.notice {
    background: #FFF9EF;
    border: 1px solid #F5E8CB;
    border-radius: 14px;
    padding: 15px 18px;
    color: #817761;
    font-size: 11px;
    line-height: 1.7;
    margin-top: 24px;
}


/* =========================
   DIVIDER
========================= */

.soft-divider {
    height: 1px;
    background: #F0EDF5;
    margin: 23px 0;
}


/* =========================
   MOBILE
========================= */

@media (max-width: 768px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .main-title {
        font-size: 25px;
    }

    .pension-value {
        font-size: 34px;
    }

    .goal-title {
        font-size: 17px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CALCULATION FUNCTIONS
# ============================================================

def future_value_monthly(
    current_asset,
    monthly_payment,
    annual_return,
    years
):
    """
    현재 자산 + 매월 납입금의 미래가치
    월복리 기준
    """

    months = int(years * 12)
    monthly_rate = annual_return / 100 / 12

    if months <= 0:
        return current_asset

    if monthly_rate == 0:
        return current_asset + monthly_payment * months

    current_growth = current_asset * (
        (1 + monthly_rate) ** months
    )

    payment_growth = monthly_payment * (
        ((1 + monthly_rate) ** months - 1)
        / monthly_rate
    )

    return current_growth + payment_growth


def calculate_principal(
    current_asset,
    monthly_payment,
    years
):
    return (
        current_asset
        + monthly_payment * years * 12
    )


def calculate_pension_monthly(
    balance,
    annual_return,
    years
):
    """
    은퇴 후 일정 기간 동안
    매월 동일 금액 수령
    """

    months = int(years * 12)

    if months <= 0:
        return 0

    monthly_rate = annual_return / 100 / 12

    if monthly_rate == 0:
        return balance / months

    payment = balance * (
        monthly_rate
        /
        (
            1 -
            (1 + monthly_rate) ** (-months)
        )
    )

    return payment


def calculate_required_balance(
    target_monthly_pension,
    annual_return,
    years
):
    """
    목표 월 연금액을 만들기 위해 필요한
    은퇴 시점의 자산
    """

    months = int(years * 12)
    monthly_rate = annual_return / 100 / 12

    if months <= 0:
        return 0

    if monthly_rate == 0:
        return target_monthly_pension * months

    balance = target_monthly_pension * (
        1 -
        (1 + monthly_rate) ** (-months)
    ) / monthly_rate

    return balance


def calculate_required_monthly_payment(
    current_asset,
    target_balance,
    annual_return,
    years
):
    """
    목표 은퇴자산을 만들기 위해 필요한
    월 납입액
    """

    months = int(years * 12)
    monthly_rate = annual_return / 100 / 12

    if months <= 0:
        return 0

    if target_balance <= current_asset:
        return 0

    if monthly_rate == 0:
        return (
            target_balance - current_asset
        ) / months

    current_growth = current_asset * (
        (1 + monthly_rate) ** months
    )

    required_payment = (
        target_balance - current_growth
    ) * monthly_rate / (
        (1 + monthly_rate) ** months - 1
    )

    return max(required_payment, 0)


def find_required_retirement_years(
    current_age,
    current_asset,
    monthly_payment,
    annual_return,
    target_balance,
    max_retirement_age=90
):
    """
    현재 월 납입액을 유지했을 때
    목표 자산을 만들기 위해 필요한 은퇴 나이
    """

    max_years = max(
        max_retirement_age - current_age,
        0
    )

    # 이미 달성
    if current_asset >= target_balance:
        return 0

    # 최대 기간에도 못 만드는 경우
    max_balance = future_value_monthly(
        current_asset,
        monthly_payment,
        annual_return,
        max_years
    )

    if max_balance < target_balance:
        return None

    low = 0.0
    high = float(max_years)

    # 이진 탐색
    for _ in range(100):

        mid = (low + high) / 2

        balance = future_value_monthly(
            current_asset,
            monthly_payment,
            annual_return,
            mid
        )

        if balance >= target_balance:
            high = mid
        else:
            low = mid

    return high


def format_money(value):
    """
    화면용 금액 표시
    """

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


def format_won(value):
    return f"{value:,.0f}원"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🟣 노후 연금 시뮬레이터</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '지금부터 준비하면 은퇴 후 매달 얼마를 받을 수 있을까요?'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT / CURRENT ASSET
# ============================================================

left, right = st.columns(
    [1.05, 1],
    gap="large"
)


# ============================================================
# LEFT : INPUT
# ============================================================

with left:

    st.markdown(
        """
        <div class="input-card">

            <div class="input-section-title">
                연금 준비 조건
            </div>

            <div class="input-section-desc">
                현재 상황과 은퇴 계획을 입력해보세요.
            </div>

        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        current_age = st.number_input(
            "현재 나이",
            min_value=18,
            max_value=80,
            value=35,
            step=1
        )

    with c2:

        retirement_age = st.number_input(
            "은퇴 나이",
            min_value=30,
            max_value=90,
            value=60,
            step=1
        )

    current_asset = st.number_input(
        "현재 연금 자산",
        min_value=0,
        max_value=10_000_000_000,
        value=10_000_000,
        step=1_000_000,
        format="%d"
    )

    monthly_payment = st.number_input(
        "매월 투자 금액",
        min_value=0,
        max_value=50_000_000,
        value=500_000,
        step=50_000,
        format="%d"
    )

    annual_return = st.slider(
        "예상 연평균 수익률",
        min_value=0.0,
        max_value=15.0,
        value=7.0,
        step=0.5
    )

    st.markdown(
        f"""
        <div style="
            background:#F8F6FC;
            border-radius:10px;
            padding:10px 13px;
            margin-top:4px;
            margin-bottom:15px;
            color:#77727F;
            font-size:11px;
        ">
            💡 연평균
            <b style="color:#7655D7;">
            {annual_return:.1f}%
            </b>
            의 수익률을 가정합니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# MAIN CALCULATION
# ============================================================

years_to_retirement = max(
    retirement_age - current_age,
    0
)


final_balance = future_value_monthly(
    current_asset,
    monthly_payment,
    annual_return,
    years_to_retirement
)


principal = calculate_principal(
    current_asset,
    monthly_payment,
    years_to_retirement
)


profit = max(
    final_balance - principal,
    0
)


profit_ratio = (
    profit / final_balance * 100
    if final_balance > 0
    else 0
)


# ============================================================
# RIGHT : PRINCIPAL / PROFIT
# ============================================================

with right:

    st.markdown(
        '<div class="card-title">'
        '은퇴 시점 예상 자산'
        '</div>',
        unsafe_allow_html=True
    )

    m1, m2 = st.columns(
        2,
        gap="medium"
    )

    with m1:

        st.markdown(
            f"""
            <div class="money-card">

                <div class="money-label">
                    투자 원금
                </div>

                <div class="money-value principal">
                    {format_money(principal)}
                </div>

                <div class="money-desc">
                    내가 실제로 납입한 금액
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with m2:

        st.markdown(
            f"""
            <div class="money-card">

                <div class="money-label">
                    예상 수익금
                </div>

                <div class="money-value profit">
                    {format_money(profit)}
                </div>

                <div class="money-desc">
                    전체 적립액의 {profit_ratio:.1f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="total-box">

            <div class="total-label">
                {retirement_age}세 은퇴 시 예상 최종 적립액
            </div>

            <div class="total-value">
                {format_money(final_balance)}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PENSION SETTINGS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '예상 연금 수령액'
    '</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:

    receive_years = st.slider(
        "은퇴 후 연금 수령 기간",
        min_value=10,
        max_value=40,
        value=25,
        step=1
    )

with c2:

    post_retirement_return = st.slider(
        "은퇴 후 예상 운용 수익률",
        min_value=0.0,
        max_value=8.0,
        value=3.0,
        step=0.5
    )


# ============================================================
# PENSION CALCULATION
# ============================================================

monthly_pension = calculate_pension_monthly(
    final_balance,
    post_retirement_return,
    receive_years
)


principal_preserving = (
    calculate_principal_preserving_income
    if False else
    final_balance
    * (post_retirement_return / 100)
    / 12
)


# ============================================================
# MAIN PENSION RESULT
# ============================================================

st.markdown(
    f"""
    <div class="pension-result">

        <div class="pension-small">
            {retirement_age}세 은퇴 ·
            {receive_years}년간 수령
        </div>

        <div class="pension-title">
            당신의 예상 연금 수령액은
        </div>

        <div class="pension-value">
            {monthly_pension:,.0f}
            <span class="pension-unit">
                원 / 월
            </span>
        </div>

        <div class="pension-info">
            은퇴 후 연 {post_retirement_return:.1f}%의
            운용수익률을 가정한 시뮬레이션입니다.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DETAILED RESULT
# ============================================================

st.markdown(
    '<div class="section-title">'
    '은퇴 후 자산은 어떻게 사용할까요?'
    '</div>',
    unsafe_allow_html=True
)

r1, r2, r3 = st.columns(
    3,
    gap="medium"
)


# FINAL BALANCE
with r1:

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                은퇴시점 최종적립액
            </div>

            <div class="result-value">
                {format_money(final_balance)}
            </div>

            <div class="result-desc">
                은퇴하는 순간 예상되는
                전체 연금 자산입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# PRINCIPAL PRESERVING
with r2:

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                원금 보존 월 수령액
            </div>

            <div class="result-value">
                {principal_preserving:,.0f}
                <span class="result-unit">
                    원
                </span>
            </div>

            <div class="result-desc">
                원금을 유지하면서
                운용수익만 사용하는 경우입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# PRINCIPAL EXHAUSTION
with r3:

    st.markdown(
        f"""
        <div class="result-card">

            <div class="result-label">
                원금 소진 월 수령액
            </div>

            <div class="result-value">
                {monthly_pension:,.0f}
                <span class="result-unit">
                    원
                </span>
            </div>

            <div class="result-desc">
                {receive_years}년 동안 모두 사용하는 경우
                매월 받을 수 있는 금액입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# ⭐ GOAL REVERSE CALCULATOR
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🎯 목표 연금 역산'
    '<span>원하는 연금액을 먼저 정해보세요</span>'
    '</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="goal-box">

        <div class="goal-header">
            <div class="goal-icon">🎯</div>
            <div class="goal-title">
                나는 은퇴 후 매월 얼마가 필요할까?
            </div>
        </div>

        <div class="goal-desc">
            원하는 월 연금액을 입력하면,
            현재 조건에서 목표를 달성하기 위해
            얼마나 더 준비해야 하는지 계산해드려요.
        </div>

    """,
    unsafe_allow_html=True
)


goal_col1, goal_col2 = st.columns(
    [1, 1],
    gap="large"
)


with goal_col1:

    target_monthly_pension = st.number_input(
        "목표 월 연금액",
        min_value=500_000,
        max_value=20_000_000,
        value=2_000_000,
        step=100_000,
        format="%d"
    )


with goal_col2:

    st.markdown(
        f"""
        <div class="goal-highlight">

            <div class="goal-highlight-label">
                현재 예상 연금
            </div>

            <div class="goal-highlight-value">
                {monthly_pension:,.0f}원 / 월
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# GOAL CALCULATIONS
# ============================================================

required_balance = calculate_required_balance(
    target_monthly_pension,
    post_retirement_return,
    receive_years
)


required_monthly_payment = calculate_required_monthly_payment(
    current_asset,
    required_balance,
    annual_return,
    years_to_retirement
)


extra_monthly_payment = max(
    required_monthly_payment - monthly_payment,
    0
)


required_years = find_required_retirement_years(
    current_age,
    current_asset,
    monthly_payment,
    annual_return,
    required_balance,
    max_retirement_age=90
)


# ============================================================
# GOAL STATUS
# ============================================================

if monthly_pension >= target_monthly_pension:

    st.success(
        f"🎉 현재 조건만으로도 목표 연금액 "
        f"{target_monthly_pension:,.0f}원을 달성할 수 있습니다!"
    )

else:

    shortfall = (
        target_monthly_pension
        - monthly_pension
    )

    st.markdown(
        f"""
        <div style="
            background:#FFF7F5;
            border:1px solid #F5DDD7;
            border-radius:13px;
            padding:13px 16px;
            margin-top:17px;
            color:#826F69;
            font-size:12px;
        ">
            현재 예상 연금은
            <b>{monthly_pension:,.0f}원</b>으로,
            목표보다
            <b>{shortfall:,.0f}원</b>
            부족합니다.
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    '<div class="soft-divider"></div>',
    unsafe_allow_html=True
)


# ============================================================
# GOAL RESULT CARDS
# ============================================================

g1, g2, g3 = st.columns(
    3,
    gap="medium"
)


# REQUIRED BALANCE
with g1:

    st.markdown(
        f"""
        <div class="goal-result">

            <div class="goal-result-label">
                필요한 은퇴자산
            </div>

            <div class="goal-result-value">
                {format_money(required_balance)}
            </div>

            <div class="goal-result-desc">
                은퇴 후 {receive_years}년 동안
                매월 {target_monthly_pension:,.0f}원을 받기 위해
                필요한 예상 자산입니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# EXTRA MONTHLY PAYMENT
with g2:

    if monthly_pension >= target_monthly_pension:

        extra_text = "추가 투자 필요 없음"

    else:

        extra_text = (
            f"+{extra_monthly_payment:,.0f}원"
        )

    st.markdown(
        f"""
        <div class="goal-result">

            <div class="goal-result-label">
                매월 추가 투자
            </div>

            <div class="goal-result-value">
                {extra_text}
            </div>

            <div class="goal-result-desc">
                현재 월 {monthly_payment:,.0f}원에서
                이 금액만큼 더 투자하면
                현재 은퇴 시점에 목표 달성이 가능합니다.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# RETIREMENT DELAY
with g3:

    if monthly_pension >= target_monthly_pension:

        retirement_text = (
            f"{retirement_age}세면 충분"
        )

        retirement_desc = (
            "현재 계획대로 은퇴해도 "
            "목표 연금액을 달성할 수 있습니다."
        )

    elif required_years is None:

        retirement_text = "90세 이후 필요"

        retirement_desc = (
            "현재 월 납입액으로는 "
            "90세까지 투자해도 목표자산 달성이 어렵습니다."
        )

    else:

        required_retirement_age = (
            current_age + required_years
        )

        delay_years = (
            required_retirement_age
            - retirement_age
        )

        retirement_text = (
            f"{required_retirement_age:.1f}세"
        )

        retirement_desc = (
            f"현재 납입액을 유지한다면 "
            f"약 {delay_years:.1f}년 "
            f"더 준비해야 합니다."
        )

    st.markdown(
        f"""
        <div class="goal-result">

            <div class="goal-result-label">
                필요한 은퇴 시점
            </div>

            <div class="goal-result-value">
                {retirement_text}
            </div>

            <div class="goal-result-desc">
                {retirement_desc}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# SIMPLE ACTION MESSAGE
# ============================================================

if monthly_pension < target_monthly_pension:

    st.markdown(
        f"""
        <div class="goal-highlight">

            <div class="goal-highlight-label">
                💡 목표 달성 방법
            </div>

            <div style="
                color:#4C4164;
                font-size:14px;
                font-weight:600;
                margin-top:5px;
                line-height:1.7;
            ">

                지금 은퇴 계획을 유지한다면
                매월
                <span style="color:#6847C8;">
                    {extra_monthly_payment:,.0f}원
                </span>
                을 추가 투자하는 방법이 있습니다.

                또는 현재 납입액을 유지하면서
                은퇴 시점을 늦추는 방법도 있습니다.

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# ASSET GROWTH CHART
# ============================================================

st.markdown(
    '<div class="section-title">'
    '노후 자산 성장 과정'
    '</div>',
    unsafe_allow_html=True
)


years = np.arange(
    0,
    years_to_retirement + 1
)


balances = [
    future_value_monthly(
        current_asset,
        monthly_payment,
        annual_return,
        int(y)
    )
    for y in years
]


chart_df = pd.DataFrame(
    {
        "나이": current_age + years,
        "예상 자산": balances
    }
)


st.markdown(
    '<div class="chart-card">',
    unsafe_allow_html=True
)


st.line_chart(
    chart_df.set_index("나이"),
    height=300
)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# CALCULATION NOTICE
# ============================================================

st.markdown(
    f"""
    <div class="notice">

        <b>💡 계산 기준</b><br>

        현재 연금자산
        <b>{format_money(current_asset)}</b>에
        매월
        <b>{format_money(monthly_payment)}</b>을 투자하고,
        연평균
        <b>{annual_return:.1f}%</b>
        의 수익률을 얻는다고 가정했습니다.

        <br>

        은퇴 후 연금 계산은 연
        <b>{post_retirement_return:.1f}%</b>
        의 운용수익률을 가정하며,
        <b>{receive_years}년</b>
        동안 매월 동일한 금액을 수령하는 방식으로 계산합니다.

        <br>

        세금, 수수료, 물가상승률, 국민연금 및 기타 연금소득은
        반영하지 않은 단순 시뮬레이션입니다.

        <br>

        실제 투자 결과와 연금 수령액은
        투자수익률 및 상품 조건에 따라 달라질 수 있습니다.

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#AAA7B1;
        font-size:10px;
        margin-top:35px;
    ">
        노후 연금 시뮬레이터 · 참고용 계산 결과
    </div>
    """,
    unsafe_allow_html=True
)
