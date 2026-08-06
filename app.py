import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

df = pd.read_csv("data/HR Data.csv")
df1 = df.copy()

df1['퇴직'] = df1['퇴직여부'].map({'No': 0, 'Yes': 1}).astype('int8')

# 연령대 생성
df1['연령대'] = pd.cut(
    df1['나이'],
    bins=[0, 29, 39, 49, 59, 100],
    labels=['20대 이하', '30대', '40대', '50대', '60대 이상']
)

df1['월급여구간'] = pd.qcut(
    df1['월급여'],
    q=4,
    labels=['하위 25%', '25~50%', '50~75%', '상위 25%']
)

def attrition_summary(data, group_column):
    result = data.groupby(group_column, observed=True).agg(
        직원수=('퇴직', 'size'),
        퇴직자수=('퇴직', 'sum'),
        퇴직률=('퇴직', 'mean')
    ).reset_index()
    result['퇴직률'] = (result['퇴직률'] * 100).round(1)
    return result.sort_values('퇴직률', ascending=False)

# ----------------- 사이드바 영역 -----------------
st.sidebar.title("필터")

over_night = st.sidebar.radio("야근 여부", ["전체", "Yes", "No"], index=0)
dept = st.sidebar.multiselect("부서 선택", options=df1['부서'].unique(), default=df1['부서'].unique())

# [수정 1] checkbox -> multiselect 로 변경하여 다중 선택 가능하도록 수정
analysis_options = ["월급여 구간별", "연령대별", "결혼 여부별", "집과의 거리별", "업무 만족도별", "근속 연수별"]
col_select = st.sidebar.multiselect("분석 기준 선택", options=analysis_options, default=["월급여 구간별"])

# 데이터 필터링
if over_night != "전체":
    df1 = df1[df1['야근정도'] == over_night]

if dept:
    df1 = df1[df1['부서'].isin(dept)]

# ----------------- 메인 화면 영역 -----------------
st.title("직원 퇴직률 분석")

total_employees = len(df1)
total_attritions = df1['퇴직'].sum() if total_employees > 0 else 0
overall_rate = round(df1['퇴직'].mean() * 100, 1) if total_employees > 0 else 0.0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("전체 직원수", f"{total_employees:,}명")
with col2:
    st.metric("전체 퇴직자수", f"{total_attritions:,}명")
with col3:
    st.metric("전체 퇴직률", f"{overall_rate:.1f}%")

st.markdown("---")

# [수정 2 & 3 & 4] 리스트 순회 및 루프 내 그래프 생성/출력 로직 수정
if total_employees > 0:
    if not col_select:
        st.info("사이드바에서 하나 이상의 분석 기준을 선택해주세요.")
    else:
        for selected in col_select:
            if selected == "월급여 구간별":
                summary = attrition_summary(df1, '월급여구간')
                x_col = '월급여구간'
            elif selected == "연령대별":
                summary = attrition_summary(df1, '연령대')
                x_col = '연령대'
            elif selected == "결혼 여부별":
                summary = attrition_summary(df1, '결혼여부')
                x_col = '결혼여부'
            elif selected == "집과의 거리별":
                summary = attrition_summary(df1, '집과의거리')
                x_col = '집과의거리'
            elif selected == "업무 만족도별":
                summary = attrition_summary(df1, '업무만족도')
                x_col = '업무만족도'
            elif selected == "근속 연수별":
                summary = attrition_summary(df1, '근속연수')
                x_col = '근속연수'

            # 각 기준별 그래프 생성 및 출력
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.barplot(data=summary, x=x_col, y='퇴직률', ax=ax, palette='viridis')
            ax.axhline(overall_rate, color='red', linestyle='--', label=f'전체 평균 ({overall_rate}%)')
            ax.set_title(f'[{selected}] 퇴직률 분석')
            ax.set_ylabel('퇴직률 (%)')
            ax.legend()
            
            plt.tight_layout()
            st.pyplot(fig)
            plt.close(fig)  # 메모리 해제
else:
    st.warning("선택된 조건에 맞는 데이터가 없습니다. 필터를 조정해주세요.")