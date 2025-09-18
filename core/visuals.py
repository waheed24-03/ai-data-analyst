# core/visuals.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def quick_visuals(df):
    """Generate quick exploratory visuals for the dataset."""
    st.subheader("📊 Quick Visual Insights")

    # Numeric column distribution
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if numeric_cols:
        col1, col2 = st.columns(2)

        with col1:
            st.write("Histogram of first numeric column")
            col = numeric_cols[0]
            fig, ax = plt.subplots()
            sns.histplot(df[col].dropna(), kde=True, ax=ax)
            st.pyplot(fig)

        if len(numeric_cols) > 1:
            with col2:
                st.write("Boxplot of second numeric column")
                col = numeric_cols[1]
                fig, ax = plt.subplots()
                sns.boxplot(y=df[col].dropna(), ax=ax)
                st.pyplot(fig)

    # Correlation heatmap
    if len(numeric_cols) >= 2:
        st.write("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
