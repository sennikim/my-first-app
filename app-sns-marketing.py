import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 페이지 설정
st.set_page_config(page_title="SNS Marketing Insights", page_icon="📊", layout="wide")

# 1. 샘플 데이터 설정
if 'sns_df' not in st.session_state:
    initial_data = [
        {"Campaign": "Summer Sale", "Platform": "Instagram", "Budget": 5000, "Revenue": 12500, "Followers": 1200, "Likes": 4500, "Shares": 300, "Comments": 150},
        {"Campaign": "Influencer Collab", "Platform": "TikTok", "Budget": 8000, "Revenue": 18000, "Followers": 5000, "Likes": 15000, "Shares": 2000, "Comments": 850},
        {"Campaign": "New Product", "Platform": "YouTube", "Budget": 3000, "Revenue": 2800, "Followers": 800, "Likes": 2100, "Shares": 120, "Comments": 60}
    ]
    st.session_state.sns_df = pd.DataFrame(initial_data)

# KPI 계산 함수
def update_metrics(df):
    df = df.copy()
    df['Engagement Rate'] = ((df['Likes'] + df['Shares'] + df['Comments']) / df['Followers'] * 100).round(2)
    df['ROI'] = ((df['Revenue'] - df['Budget']) / df['Budget'] * 100).round(2)
    return df

st.session_state.sns_df = update_metrics(st.session_state.sns_df)

# --- 사이드바 ---
st.sidebar.header("🚀 Add New Campaign")
with st.sidebar.form("input_form", clear_on_submit=True):
    c_name = st.text_input("Campaign Name")
    c_platform = st.selectbox("Platform", ["Instagram", "TikTok", "YouTube"])
    c_budget = st.number_input("Budget ($)", min_value=1)
    c_revenue = st.number_input("Revenue ($)", min_value=0)
    c_followers = st.number_input("New Followers", min_value=1)
    c_likes = st.number_input("Likes", min_value=0)
    c_shares = st.number_input("Shares", min_value=0)
    c_comments = st.number_input("Comments", min_value=0)

    if st.form_submit_button("Launch Analysis"):
        if c_name:
            new_row = pd.DataFrame([{
                "Campaign": c_name,
                "Platform": c_platform,
                "Budget": c_budget,
                "Revenue": c_revenue,
                "Followers": c_followers,
                "Likes": c_likes,
                "Shares": c_shares,
                "Comments": c_comments
            }])
            st.session_state.sns_df = pd.concat([st.session_state.sns_df, new_row], ignore_index=True)
            st.session_state.sns_df = update_metrics(st.session_state.sns_df)
        else:
            st.sidebar.warning("Please enter a campaign name.")

# --- 메인 ---
st.title("📊 SNS Marketing Analytics Dashboard")
st.markdown("Monitor campaign performance, ROI, and engagement at a glance.")

df = st.session_state.sns_df

# KPI
avg_roi = df['ROI'].mean()
avg_eng = df['Engagement Rate'].mean()

m1, m2, m3 = st.columns(3)
m1.metric("Total Budget Spent", f"${df['Budget'].sum():,}")
m2.metric("Avg. Engagement Rate", f"{avg_eng:.2f}%", delta=f"{(avg_eng-5):.1f}%")
m3.metric("Overall ROI", f"{avg_roi:.1f}%", delta=f"{(avg_roi-100):.1f}%", delta_color="normal")

# 트렌드 차트
st.subheader("📈 Weekly Performance Trend")
trend_data = pd.DataFrame(np.random.randint(10, 100, size=(10, 3)), columns=['Instagram', 'TikTok', 'YouTube'])
st.line_chart(trend_data)

# 테이블 + 차트
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Campaign Data")

    # 👉 스타일 안전 처리 (에러 방지)
    def style_roi(val):
        try:
            return 'color: green; font-weight: bold' if val >= 50 else 'color: red'
        except:
            return ''

    if 'ROI' in df.columns:
        try:
            st.dataframe(df.style.applymap(style_roi, subset=['ROI']), use_container_width=True)
        except:
            st.dataframe(df, use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("💰 ROI by Platform")
    fig = px.bar(
        df,
        x='Platform',
        y='ROI',
        color='ROI',
        color_continuous_scale=['red', 'yellow', 'green'],
        title="ROI % Comparison"
    )
    st.plotly_chart(fig, use_container_width=True)

st.balloons()
