"""
Supermarket Sales Dashboard
Streamlit app for exploring supermarket sales data.
"""
import streamlit as st
from backend import load_data, get_summary, plot_sales_over_time

st.set_page_config(page_title="Supermarket Sales Dashboard", page_icon="🛒", layout="wide")

def main():
    st.title("🛒 Supermarket Sales Dashboard")
    st.caption("Interactive dashboard for exploring supermarket sales performance.")

    # ---- Load data ----
    data = load_data()

    # ---- Sidebar filters ----
    st.sidebar.header("Filters")

    # 多选筛选器：分店/城市/支付方式
    branches = sorted(data["Branch"].unique())
    cities = sorted(data["City"].unique())
    payments = sorted(data["Payment"].unique())

    selected_branches = st.sidebar.multiselect("Branch", branches, default=branches)
    selected_cities = st.sidebar.multiselect("City", cities, default=cities)
    selected_payments = st.sidebar.multiselect("Payment", payments, default=payments)

    # Rating 滑块
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 10.0, 5.0, 0.1)

    # ---- Apply filters ----
    filtered = data[
        (data["Branch"].isin(selected_branches)) &
        (data["City"].isin(selected_cities)) &
        (data["Payment"].isin(selected_payments)) &
        (data["Rating"] >= min_rating)
    ].copy()

    # ---- KPI cards ----
    summary = get_summary(filtered)

    total_sales = float(summary["Total Sales"].iloc[0])
    avg_rating = float(summary["Average Rating"].iloc[0])
    total_tx = int(summary["Total Transactions"].iloc[0])

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"{total_sales:,.2f}")
    c2.metric("Average Rating", f"{avg_rating:.2f}")
    c3.metric("Total Transactions", f"{total_tx:,}")

    st.divider()

    # ---- Tabs layout ----
    tab1, tab2, tab3 = st.tabs(["📈 Overview", "🗓️ Trends", "📄 Data"])

    with tab1:
        left, right = st.columns([1.2, 1])
        with left:
            st.subheader("Sales Over Time")
            fig = plot_sales_over_time(filtered)
            st.pyplot(fig, use_container_width=True)

        with right:
            st.subheader("Quick Notes")
            st.write(
                f"- Showing **{len(filtered):,}** records after filters.\n"
                f"- Branch: **{', '.join(selected_branches)}**\n"
                f"- City: **{', '.join(selected_cities)}**\n"
                f"- Payment: **{', '.join(selected_payments)}**\n"
            )

    with tab2:
        st.subheader("Trends")
        st.info("You can add more charts here (by Product line / Gender / Customer type).")

    with tab3:
        st.subheader("Raw Data")
        show_cols = st.multiselect("Columns to display", list(filtered.columns), default=list(filtered.columns))
        st.dataframe(filtered[show_cols], use_container_width=True)

        st.download_button(
            "Download filtered data as CSV",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="filtered_supermarket_sales.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()