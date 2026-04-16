import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Interactive Data Explorer", layout="wide")

# ---------------- UI ----------------
st.title("📊 Interactive Data Exploration App")
st.caption("Upload • Filter • Group • Visualize • Download")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:

    # ---------------- LOAD DATA ----------------
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Dataset loaded successfully!")

    # ---------------- DATA PREVIEW ----------------
    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    # ---------------- DATA SUMMARY ----------------
    st.subheader("ℹ Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())

    # ---------------- FILTERING ----------------
    st.subheader("🎛 Simple Filtering")
    filter_col = st.selectbox("Select column to filter", df.columns)

    df_filtered = df.copy()

    if df[filter_col].dtype == "object":
        selected_vals = st.multiselect("Select values", df[filter_col].dropna().unique())
        if selected_vals:
            df_filtered = df[df[filter_col].isin(selected_vals)]
    else:
        min_val, max_val = float(df[filter_col].min()), float(df[filter_col].max())
        range_vals = st.slider("Select range", min_val, max_val, (min_val, max_val))
        df_filtered = df[
            (df[filter_col] >= range_vals[0]) &
            (df[filter_col] <= range_vals[1])
        ]

    st.info(f"✅ {df_filtered.shape[0]} records after filtering")
    st.dataframe(df_filtered, use_container_width=True)

    # ---------------- GROUPING ----------------
    st.subheader("📊 Grouping & Aggregation")

    group_col = st.selectbox("Group by", df.columns)

    numeric_cols = df_filtered.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        st.warning("⚠ No numeric columns available for aggregation.")
    else:
        agg_col = st.selectbox("Select numeric column for aggregation", numeric_cols)
        agg_func = st.radio(
            "Aggregation Function",
            ["mean", "sum", "count", "max", "min"],
            horizontal=True
        )

        grouped_df = (
            df_filtered
            .groupby(group_col, as_index=False)
            .agg({agg_col: agg_func})
        )

        st.dataframe(grouped_df, use_container_width=True)

    # ---------------- VISUALIZATION ----------------
    st.subheader("📈 Data Visualization")

    numeric_cols = df_filtered.select_dtypes(include="number").columns

    if len(numeric_cols) == 0:
        st.warning("⚠ No numeric columns available for visualization.")
    else:
        viz_col = st.selectbox("Select Numerical Column for Visualization", numeric_cols)

        chart_type = st.selectbox(
            "Choose Chart Type",
            ["Histogram", "Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart"]
        )

        # ✅ HISTOGRAM
        if chart_type == "Histogram":
            fig = px.histogram(
                df_filtered,
                x=viz_col,
                nbins=30,
                title=f"Distribution of {viz_col}"
            )

        # ✅ LINE CHART
        elif chart_type == "Line Chart":
            fig = px.line(
                df_filtered,
                y=viz_col,
                title=f"Trend of {viz_col}"
            )

        # ✅ BAR CHART
        elif chart_type == "Bar Chart":
            bar_group = st.selectbox("Select Group Column for Bar Chart", df.columns)
            bar_data = df_filtered.groupby(bar_group, as_index=False)[viz_col].mean()

            fig = px.bar(
                bar_data,
                x=bar_group,
                y=viz_col,
                title=f"Average {viz_col} by {bar_group}"
            )

        # ✅ SCATTER PLOT
        elif chart_type == "Scatter Plot":
            scatter_col = st.selectbox(
                "Select Second Numerical Column",
                [col for col in numeric_cols if col != viz_col]
            )

            fig = px.scatter(
                df_filtered,
                x=viz_col,
                y=scatter_col,
                title=f"{viz_col} vs {scatter_col}"
            )

        # ✅ PIE CHART
        elif chart_type == "Pie Chart":
            pie_group = st.selectbox("Select Category for Pie Chart", df.columns)
            pie_data = df_filtered.groupby(pie_group, as_index=False)[viz_col].sum()

            fig = px.pie(
                pie_data,
                names=pie_group,
                values=viz_col,
                title=f"{viz_col} Distribution by {pie_group}"
            )

        st.plotly_chart(fig, use_container_width=True)

    # ---------------- DOWNLOAD ----------------
    st.subheader("⬇ Download Filtered Data")

    csv = df_filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download CSV",
        csv,
        "filtered_data.csv",
        "text/csv"
    )

else:
    st.info("👆 Please upload a dataset to start.")
