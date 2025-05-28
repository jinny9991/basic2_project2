import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="내 대시보드",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 제목
st.title("📊 데이터 대시보드")
st.markdown("---")

# 사이드바
st.sidebar.header("설정")
chart_type = st.sidebar.selectbox(
    "차트 유형 선택",
    ["선 그래프", "막대 그래프", "산점도", "히트맵"]
)

# 샘플 데이터 생성
@st.cache_data
def load_data():
    dates = pd.date_range('2024-01-01', periods=100)
    data = pd.DataFrame({
        'date': dates,
        'sales': np.random.normal(1000, 200, 100).cumsum(),
        'visitors': np.random.normal(500, 100, 100),
        'conversion_rate': np.random.normal(0.05, 0.01, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    return data

df = load_data()

# 메트릭 표시
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="총 매출",
        value=f"₩{df['sales'].sum():,.0f}",
        delta=f"{df['sales'].iloc[-1] - df['sales'].iloc[-2]:,.0f}"
    )

with col2:
    st.metric(
        label="평균 방문자",
        value=f"{df['visitors'].mean():.0f}",
        delta=f"{df['visitors'].iloc[-1] - df['visitors'].mean():.0f}"
    )

with col3:
    st.metric(
        label="전환율",
        value=f"{df['conversion_rate'].mean():.2%}",
        delta=f"{df['conversion_rate'].iloc[-1] - df['conversion_rate'].mean():.2%}"
    )

with col4:
    st.metric(
        label="데이터 포인트",
        value=len(df),
        delta="100"
    )

# 차트 표시
st.markdown("## 📈 데이터 시각화")

if chart_type == "선 그래프":
    fig = px.line(df, x='date', y='sales', title='일별 매출 추이')
    st.plotly_chart(fig, use_container_width=True)
    
elif chart_type == "막대 그래프":
    category_sales = df.groupby('category')['sales'].sum().reset_index()
    fig = px.bar(category_sales, x='category', y='sales', title='카테고리별 매출')
    st.plotly_chart(fig, use_container_width=True)
    
elif chart_type == "산점도":
    fig = px.scatter(df, x='visitors', y='sales', color='category', title='방문자 vs 매출')
    st.plotly_chart(fig, use_container_width=True)
    
elif chart_type == "히트맵":
    correlation = df[['sales', 'visitors', 'conversion_rate']].corr()
    fig = px.imshow(correlation, text_auto=True, title='상관관계 히트맵')
    st.plotly_chart(fig, use_container_width=True)

# 데이터 테이블
st.markdown("## 📋 원본 데이터")
st.dataframe(df, use_container_width=True)

# 다운로드 버튼
csv = df.to_csv(index=False)
st.download_button(
    label="CSV로 다운로드",
    data=csv,
    file_name="dashboard_data.csv",
    mime="text/csv"
)