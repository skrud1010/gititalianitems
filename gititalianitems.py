import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os
import plotly.express as px

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# 1️⃣ 폰트 파일 경로 (상대경로 or 절대경로)
font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")

# 2️⃣ matplotlib에 폰트 강제 등록
fm.fontManager.addfont(font_path)
font_name = fm.FontProperties(fname=font_path).get_name()

# 3️⃣ 전역 폰트 설정
plt.rcParams["font.family"] = font_name
plt.rcParams["axes.unicode_minus"] = False

# -------------------------------
# 1. 한글 폰트 설정
# -------------------------------
@st.cache_resource
def setup_font():
    font_path = "NanumGothic.ttf"
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        plt.rc('font', family=font_prop.get_name())
        plt.rcParams['axes.unicode_minus'] = False
        return font_prop
    return None

font_prop = setup_font()

# -------------------------------
# 2. 엑셀 데이터 로드
# -------------------------------
@st.cache_data
def load_data():
    file_path = "이탈리아_한국_수출입_표.csv"
    df = pd.read_csv(file_path, encoding="cp949")
    return df

# -------------------------------
# 3. 페이지 설정
# -------------------------------
st.set_page_config(page_title="Italy–Korea Trade Pie Chart", layout="wide")

st.title("📊 이탈리아–한국 수출입 품목 구조 분석")

st.markdown("---")

# -------------------------------
# 4. 데이터 분리
# -------------------------------
df = load_data()
export_df = df[["수출_품목명", "수출_금액"]]
import_df = df[["수입_품목명", "수입_금액"]]

# -------------------------------
# 5. 레이아웃 (좌: 수출 / 우: 수입)
# -------------------------------
col1, col2 = st.columns(2)

# -------------------------------
# 6. 수출 / 수입 원형 차트 (강조 색상)
# -------------------------------
st.subheader("🔟 이탈리아의 10대 교역 품목")
st.caption("단위: 백만달러 (%)")
st.caption("자료: KITA(한국 무역협회, 2020년)")

col1, col2 = st.columns(2)

# -------------------------------
# 수출 (이탈리아로 수출)
# -------------------------------
with col1:
    st.markdown("### 📤 이탈리아 수출 상위 10개 품목")

    fig_export = px.pie(
        export_df,
        names="수출_품목명",
        values="수출_금액",
        title=""
    )

    fig_export.update_traces(
        marker=dict(
            colors=["#CD212A"] + ["#1F77B4"] * 9,
            line=dict(color="white", width=2)
        ),
        pull=[0.08] + [0] * 9,
        hovertemplate="<b>%{label}</b><br>금액: %{value} 백만달러<br>비중: %{percent}<extra></extra>"
    )

    st.plotly_chart(fig_export, use_container_width=True)

# -------------------------------
# 수입 (한국으로 수입)
# -------------------------------
with col2:
    st.markdown("### 📥 한국 수입 상위 10개 품목")

    fig_import = px.pie(
        import_df,
        names="수입_품목명",
        values="수입_금액",
        title=""
    )

    fig_import.update_traces(
        marker=dict(
            colors=["#008C45"] + ["#CD212A"] * 9,
            line=dict(color="white", width=2)
        ),
        pull=[0.1] + [0] * 9,
        hovertemplate="<b>%{label}</b><br>금액: %{value} 백만달러<br>비중: %{percent}<extra></extra>"
    )

    st.plotly_chart(fig_import, use_container_width=True)
