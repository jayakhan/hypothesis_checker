import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

from validate_file import validate_csv
from gemini_integration import *


st.title("Check Your A/B Experiment Results")
st.write("***Ensure your dataset follows this format before uploading.***")

# Create two columns
col1, col2 = st.columns([3, 1])  # Adjust width as needed

with col1:
    st.write("Your dataset should follow this format:")
    st.markdown(
        """
    - **Column names**: Must be parsable (letters, numbers, spaces, underscores only).
    - **First row**: Should contain column names.
    - **Group column**: Must exist and contain only "Control" and "Treatment".
    - **Other columns**: Must contain numeric data, with no fully empty columns.
    """
    )

with col2:
    with open(
        "experiment_data.csv", "rb"
    ) as f:  # Open as binary file for proper download
        st.download_button(
            "📥 Download Sample CSV",
            f,
            file_name="experiment_data.csv",
            mime="text/csv",
        )

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        df.dropna(inplace=True)

        # Validate the CSV
        is_valid, error_message = validate_csv(df)
        if not is_valid:
            st.error(error_message)
        else:
            control_group = df[df["Group"] == "Control"]
            treatment_group = df[df["Group"] == "Treatment"]
            p_values = {}
            for col in df.select_dtypes(include=[np.number]).columns:
                if col != "Group":  # Avoid the 'Group' column
                    t_statistic, p_value = stats.ttest_ind(
                        control_group[col], treatment_group[col], nan_policy="omit"
                    )
                p_values[col] = p_value
            report = generate_llm_response(p_values)
            st.markdown(report)
    except Exception as e:
        st.error(f"An error occurred: {e}")
