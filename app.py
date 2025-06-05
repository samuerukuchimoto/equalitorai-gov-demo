
import streamlit as st
import pandas as pd
import numpy as np

st.title("EqualitorAI Gov: Bias Auditor for Public Services")
st.markdown("""
Upload a CSV file of approval decisions (e.g., social assistance, grants).
We’ll analyze potential disparities based on name, zip code, gender, and age.
""")

uploaded_file = st.file_uploader("📥 Upload CSV File", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Data Preview")
    st.dataframe(df.head())

    issues = []

    # Check for required columns
    required_cols = ["name", "zip", "gender", "age", "decision"]
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        st.error(f"Missing columns: {', '.join(missing)}")
    else:
        st.success("✅ Required columns found. Proceeding with audit...")

        st.subheader("🔍 Bias Risk Analysis")

        # Name bias (proxy for ethnicity)
        name_flags = df[df['name'].str.contains(r'[aeiou]{3,}', na=False, case=False)]
        if len(name_flags) > 0:
            issues.append("⚠️ Potential ethnic bias detected based on name patterns.")

        # Zip code clustering
        zip_counts = df['zip'].value_counts()
        top_zip = zip_counts[zip_counts > zip_counts.mean() + zip_counts.std()]
        if not top_zip.empty:
            issues.append("⚠️ Unusual concentration of decisions in specific zip codes.")

        # Gender imbalance
        gender_summary = df.groupby("gender")["decision"].value_counts(normalize=True).unstack().fillna(0)
        st.markdown("**Gender Decision Ratios:**")
        st.dataframe(gender_summary.round(2))

        # Age disparity
        df["age_group"] = pd.cut(df["age"], bins=[0, 25, 45, 65, 100], labels=["Youth", "Adult", "Mid-age", "Senior"])
        age_summary = df.groupby("age_group")["decision"].value_counts(normalize=True).unstack().fillna(0)
        st.markdown("**Age Group Decision Ratios:**")
        st.dataframe(age_summary.round(2))

        # Final summary
        st.subheader("📋 Audit Summary")
        if issues:
            for i in issues:
                st.warning(i)
            st.error("Bias risk detected. Recommend further review.")
        else:
            st.success("No significant bias risks detected in this dataset.")

    st.caption("EqualitorAI Gov MVP — For public systems that serve *everyone*.")
