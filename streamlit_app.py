import random
from datetime import date

import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="이게뭐에요..?",
    page_icon="🧪",
    layout="wide",
)


def make_sales_data(refresh_count: int) -> pd.DataFrame:
    """차트와 표에서 함께 사용할 간단한 예제 데이터를 만듭니다."""
    generator = random.Random(42 + refresh_count)
    categories = {"음료": 120, "간식": 85, "식사": 160}
    rows = []

    for day_index, day in enumerate(pd.date_range("2026-01-01", periods=14)):
        for category, base in categories.items():
            rows.append(
                {
                    "날짜": day,
                    "분류": category,
                    "매출(천원)": base + day_index * 3 + generator.randint(-18, 18),
                    "판매 수량": 8 + day_index + generator.randint(0, 12),
                }
            )

    return pd.DataFrame(rows)


if "click_count" not in st.session_state:
    st.session_state.click_count = 0
if "data_refresh_count" not in st.session_state:
    st.session_state.data_refresh_count = 0


with st.sidebar:
    st.title("실습 안내")
    st.write("각 탭의 위젯을 직접 바꾸고 결과가 어떻게 달라지는지 확인해 보세요.")
    st.divider()
    st.caption("예제 데이터는 앱 안에서 생성되며 원본 파일을 변경하지 않습니다.")


st.title("Streamlit 요소 실습실")
st.write("웹 앱의 기본 요소를 한 페이지에서 직접 눌러보고 바꿔보세요.")
st.caption("위젯을 조작하면 페이지가 다시 실행되고, 입력값에 맞춰 결과가 업데이트됩니다.")

intro_columns = st.columns(3)
intro_columns[0].metric("텍스트·입력", "직접 입력")
intro_columns[1].metric("상호작용", "버튼·슬라이더")
intro_columns[2].metric("데이터 표현", "표·차트")

text_tab, controls_tab, data_tab, layout_tab = st.tabs(
    ["텍스트와 입력", "버튼과 상태", "표와 차트", "레이아웃과 기타"]
)


with text_tab:
    st.header("텍스트와 입력 위젯")
    st.write("`st.write`는 텍스트, 숫자, 데이터 등 다양한 값을 화면에 보여줍니다.")
    st.markdown("마크다운으로 **굵은 글씨**나 목록도 표현할 수 있어요.")
    st.caption("`st.caption`은 보충 설명처럼 작은 글씨를 표시합니다.")

    left_column, right_column = st.columns(2)
    with left_column:
        visitor_name = st.text_input("이름을 입력해 보세요", placeholder="예: 민지")
        visitor_age = st.number_input("나이", min_value=0, max_value=120, value=20)
        favorite_color = st.selectbox("좋아하는 색", ["파랑", "초록", "빨강", "노랑"])
        interests = st.multiselect(
            "관심 있는 주제 (여러 개 선택 가능)",
            ["데이터", "차트", "웹 앱", "파이썬"],
            default=["데이터"],
        )
    with right_column:
        message = st.text_area("짧은 메모", placeholder="여기에 내용을 입력하세요.")
        visit_date = st.date_input("날짜 선택", value=date.today())
        display_mode = st.radio("표시 방식", ["간단히", "자세히"], horizontal=True)
        wants_updates = st.checkbox("새 소식 받기")

    greeting_name = visitor_name or "방문자"
    st.info(f"안녕하세요, {greeting_name}님! {visitor_age}세, {favorite_color}을(를) 좋아하시네요.")
    st.write(f"관심 주제: {', '.join(interests) if interests else '선택하지 않음'}")
    if display_mode == "자세히":
        st.write(f"선택한 날짜: {visit_date} · 메모: {message or '작성하지 않음'}")
    if wants_updates:
        st.success("체크박스를 선택해 추가 안내가 나타났습니다.")

    st.subheader("폼으로 한 번에 제출하기")
    st.write("폼 안의 입력값은 제출 버튼을 누를 때 한꺼번에 전달됩니다.")
    with st.form("topic_form"):
        topic = st.text_input("배우고 싶은 Streamlit 주제", key="form_topic")
        submitted = st.form_submit_button("주제 제출")
    if submitted:
        st.success(f"'{topic or '새 주제'}' 주제를 확인했어요.")


with controls_tab:
    st.header("버튼과 값 조절")
    st.write("버튼을 누르면 값이 바뀌고, 세션 상태에 저장되어 다시 실행된 뒤에도 유지됩니다.")

    button_column, result_column = st.columns([1, 2])
    with button_column:
        if st.button("클릭 횟수 +1", type="primary"):
            st.session_state.click_count += 1
        if st.button("횟수 초기화"):
            st.session_state.click_count = 0
    with result_column:
        st.metric("버튼 클릭 횟수", st.session_state.click_count)

    st.divider()
    satisfaction = st.slider("오늘의 만족도", min_value=0, max_value=100, value=65, step=5)
    st.write(f"선택한 만족도: **{satisfaction}점**")
    volume = st.select_slider("음량 단계", options=["조용히", "보통", "크게"], value="보통")
    st.write(f"현재 음량: {volume}")

    show_progress = st.toggle("진행률 표시")
    if show_progress:
        st.progress(satisfaction, text=f"만족도 {satisfaction}%")
    else:
        st.caption("토글을 켜면 진행률 표시줄이 나타납니다.")


with data_tab:
    st.header("데이터 표와 차트")
    st.write("표는 행 단위의 데이터를, 차트는 데이터의 변화와 비교를 보여줍니다.")

    if st.button("예제 데이터 새로 만들기"):
        st.session_state.data_refresh_count += 1
    sales_data = make_sales_data(st.session_state.data_refresh_count)

    category_options = sales_data["분류"].unique().tolist()
    selected_categories = st.multiselect(
        "표시할 분류", category_options, default=category_options, key="chart_categories"
    )
    chart_kind = st.radio(
        "차트 종류", ["선 차트", "막대 차트", "영역 차트"], horizontal=True
    )

    filtered_data = sales_data[sales_data["분류"].isin(selected_categories)]
    total_sales = int(filtered_data["매출(천원)"].sum()) if not filtered_data.empty else 0
    st.metric("선택한 분류의 총매출", f"{total_sales:,} 천원")

    daily_sales = filtered_data.groupby(["날짜", "분류"], as_index=False)["매출(천원)"].sum()
    if chart_kind == "선 차트":
        st.line_chart(daily_sales, x="날짜", y="매출(천원)", color="분류")
    elif chart_kind == "막대 차트":
        st.bar_chart(daily_sales, x="날짜", y="매출(천원)", color="분류")
    else:
        st.area_chart(daily_sales, x="날짜", y="매출(천원)", color="분류")

    st.subheader("상세 데이터")
    st.dataframe(filtered_data, width="stretch", hide_index=True)
    st.caption("`st.dataframe`은 정렬·크기 조절이 가능한 표입니다.")
    st.write("처음 5개 행을 고정된 표로 보기")
    st.table(filtered_data.head(5))

    st.download_button(
        "CSV 다운로드",
        data=filtered_data.to_csv(index=False).encode("utf-8-sig"),
        file_name="streamlit_sample_data.csv",
        mime="text/csv",
    )


with layout_tab:
    st.header("화면 구성 요소")
    st.write("열, 구분선, 접기 영역을 조합해 정보를 읽기 쉽게 배치할 수 있습니다.")

    first_column, second_column = st.columns(2)
    with first_column:
        st.subheader("첫 번째 열")
        st.info("`st.columns`는 화면을 나란한 영역으로 나눕니다.")
    with second_column:
        st.subheader("두 번째 열")
        st.success("각 열 안에도 다른 위젯을 넣을 수 있습니다.")

    with st.expander("눌러서 자세한 설명 보기"):
        st.write("`st.expander`는 필요한 경우에만 내용을 펼쳐 보여줘 화면을 간결하게 유지합니다.")

    with st.container(border=True):
        st.subheader("그룹으로 묶인 영역")
        st.write("`st.container`는 관련된 요소를 한 영역으로 묶을 때 사용합니다.")
        st.button("비활성화된 버튼 예시", disabled=True)

    st.divider()
    st.warning("이 안내는 `st.warning` 예시입니다. 실제 오류가 발생한 것은 아닙니다.")
