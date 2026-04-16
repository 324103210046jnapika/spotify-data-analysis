# ==========================================
# TASK 7: STREAMLIT \
# ==========================================

# -------------------------------
# 1. Import Required Libraries
# -------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# 2. Page Configuration
# -------------------------------
st.set_page_config(page_title="Spotify Data Analysis App", layout="wide")

st.title("🎵 Spotify Dataset Analysis using Streamlit")
st.write("Upload, Clean, Filter, Analyze and Visualize Spotify Data Interactively")

# -------------------------------
# 3. File Upload Section
# -------------------------------
uploaded_file = st.file_uploader("Upload Spotify CSV File", type=["csv"])

if uploaded_file is not None:

    # -------------------------------
    # 4. Load Dataset
    # -------------------------------
    df = pd.read_csv(uploaded_file)
    st.success("Dataset Uploaded Successfully!")

    # Show first 5 records
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # -------------------------------
    # 5. Dataset Information
    # -------------------------------
    st.subheader("Dataset Information")
    st.write("Shape of Dataset:", df.shape)
    st.write("Column Names:", df.columns.tolist())

    # -------------------------------
    # 6. Missing Value Analysis
    # -------------------------------
    st.subheader("Missing Values")
    st.write(df.isnull().sum())

    # -------------------------------
    # 7. DATA CLEANING SECTION
    # -------------------------------
    st.subheader("Data Cleaning")

    # Handle Missing Values
    numeric_cols = df.select_dtypes(include=np.number).columns
    categorical_cols = df.select_dtypes(include="object").columns

    # Fill numeric columns with mean
    for col in numeric_cols:
        df[col].fillna(df[col].mean(), inplace=True)

    # Fill categorical columns with mode
    for col in categorical_cols:
        df[col].fillna(df[col].mode()[0], inplace=True)

    st.success("Missing values handled using Mean & Mode")

    # Remove Duplicate Records
    df.drop_duplicates(inplace=True)
    st.success("Duplicate Records Removed")

    # -------------------------------
    # 8. DATA WRANGLING
    # -------------------------------
    st.subheader("Data Wrangling")

    # Convert Explicit column safely
    if "explicit" in df.columns:
        df["explicit"] = pd.to_numeric(df["explicit"], errors="coerce").fillna(0).astype(int)

    # Create Derived Column: Popularity Category
    if "popularity" in df.columns:
        df["popularity_category"] = pd.cut(
            df["popularity"],
            bins=[0, 40, 70, 100],
            labels=["Low", "Medium", "High"]
        )

    st.success("Data Type Conversion and Feature Engineering Applied")

    st.dataframe(df.head())

    # -------------------------------
    # 9. FILTERING & INDEXING
    # -------------------------------
    st.subheader("Filtering & Indexing")

    selected_artist = st.selectbox(
        "Select Artist for Filtering",
        options=["All"] + sorted(df["artist"].unique().tolist())
    )

    if selected_artist != "All":
        filtered_df = df[df["artist"] == selected_artist]
    else:
        filtered_df = df.copy()

    st.dataframe(filtered_df.head())

    # Set Track Name as Index (if exists)
    if "track_name" in df.columns:
        df.set_index("track_name", inplace=True, drop=False)

    # -------------------------------
    # 10. VISUALIZATION USING MATPLOTLIB
    # -------------------------------
    st.subheader("Visualization Section")

    chart_type = st.selectbox(
        "Select Chart Type",
        ["Line Plot", "Scatter Plot", "Bar Chart", "Histogram"]
    )

    # ---------- LINE PLOT ----------
    if chart_type == "Line Plot":
        st.subheader("Line Plot: Popularity Trend")

        if "popularity" in df.columns:
            plt.figure()
            plt.plot(df["popularity"].values)
            plt.xlabel("Records")
            plt.ylabel("Popularity")
            plt.title("Popularity Line Graph")
            st.pyplot(plt)

    # ---------- SCATTER PLOT ----------
    elif chart_type == "Scatter Plot":
        st.subheader("Scatter Plot: Danceability vs Energy")

        if "danceability" in df.columns and "energy" in df.columns:
            plt.figure()
            plt.scatter(df["danceability"], df["energy"])
            plt.xlabel("Danceability")
            plt.ylabel("Energy")
            plt.title("Danceability vs Energy")
            st.pyplot(plt)

    # ---------- BAR CHART ----------
    elif chart_type == "Bar Chart":
        st.subheader("Bar Chart: Popularity by Artist")

        if "artist" in df.columns and "popularity" in df.columns:
            top_artists = df.groupby("artist")["popularity"].mean().nlargest(10)

            plt.figure()
            top_artists.plot(kind="bar")
            plt.xlabel("Artist")
            plt.ylabel("Average Popularity")
            plt.title("Top 10 Artists by Popularity")
            st.pyplot(plt)

    # ---------- HISTOGRAM ----------
    elif chart_type == "Histogram":
        st.subheader("Histogram: Distribution of Track Popularity")

        if "popularity" in df.columns:
            plt.figure()
            plt.hist(df["popularity"], bins=20)
            plt.xlabel("Popularity")
            plt.ylabel("Frequency")
            plt.title("Popularity Distribution")
            st.pyplot(plt)

    # -------------------------------
    # 11. DOWNLOAD CLEANED DATASET
    # -------------------------------
    st.subheader("Download Cleaned Dataset")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Cleaned Spotify Dataset",
        data=csv,
        file_name="cleaned_spotify_data.csv",
        mime="text/csv"
    )

else:
    st.warning("⚠️ Please upload a Spotify CSV file to continue.")
