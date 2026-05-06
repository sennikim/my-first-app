import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🎨 Art Gallery Dashboard", layout="wide")

# 1. 샘플 데이터 설정
if 'gallery_data' not in st.session_state:
    initial_data = [
        {"Title": "Starry Night", "Artist": "Vincent van Gogh", "Year": 1889, "Medium": "Oil on Canvas", "Price": 100000000, "Period": "Post-Impressionism"},
        {"Title": "Mona Lisa", "Artist": "Leonardo da Vinci", "Year": 1503, "Medium": "Oil on Poplar", "Price": 850000000, "Period": "Renaissance"},
        {"Title": "The Scream", "Artist": "Edvard Munch", "Year": 1893, "Medium": "Oil, Tempera & Pastel", "Price": 120000000, "Period": "Expressionism"},
        {"Title": "Guernica", "Artist": "Pablo Picasso", "Year": 1937, "Medium": "Oil on Canvas", "Price": 200000000, "Period": "Cubism"},
        {"Title": "Girl with a Pearl Earring", "Artist": "Johannes Vermeer", "Year": 1665, "Medium": "Oil on Canvas", "Price": 50000000, "Period": "Baroque"}
    ]
    st.session_state.gallery_data = pd.DataFrame(initial_data)

# --- 사이드바: 새로운 작품 추가 ---
st.sidebar.header("➕ Add New Artwork")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_title = st.text_input("Title")
    new_artist = st.text_input("Artist")
    new_year = st.number_input("Year", min_value=0, value=2024)
    new_medium = st.selectbox("Medium", ["Oil on Canvas", "Watercolor", "Sculpture", "Digital Art", "Other"])
    new_price = st.number_input("Price ($)", min_value=0)
    new_period = st.text_input("Art Period (e.g., Renaissance, Modern)")

    submit_button = st.form_submit_button("Add to Collection")

    if submit_button:
        if new_title and new_artist:
            new_row = {
                "Title": new_title,
                "Artist": new_artist,
                "Year": new_year,
                "Medium": new_medium,
                "Price": new_price,
                "Period": new_period
            }
            st.session_state.gallery_data = pd.concat(
                [st.session_state.gallery_data, pd.DataFrame([new_row])],
                ignore_index=True
            )
            st.sidebar.success("Added to gallery! ✨")
        else:
            st.sidebar.warning("Please enter at least Title and Artist.")

# --- 메인 영역 ---
st.title("🎨 Interactive Art Gallery Dashboard")
st.markdown("Curation tool for your digital art collection.")

# 검색 기능
search_query = st.text_input("🔍 Search by Artist Name", "")

filtered_df = st.session_state.gallery_data[
    st.session_state.gallery_data['Artist'].str.contains(search_query, case=False, na=False)
]

# 데이터 테이블
st.subheader("🖼️ Collection Overview")
st.dataframe(filtered_df, use_container_width=True)

# 시각화
col1, col2 = st.columns(2)

with col1:
    st.subheader("💰 Price Analysis ($)")
    if not filtered_df.empty:
        fig_bar = px.bar(
            filtered_df,
            x='Title',
            y='Price',
            color='Artist',
            title="Artwork Prices Comparison",
            template="plotly_white"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No data available for chart.")

with col2:
    st.subheader("⏳ Distribution by Period")
    if not filtered_df.empty:
        fig_pie = px.pie(
            filtered_df,
            names='Period',
            title="Works by Period",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.warning("No data available for chart.")

st.balloons()
