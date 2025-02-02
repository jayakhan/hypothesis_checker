import streamlit as st
import pandas as pd
import numpy as np
from scipy import stats

from validate_file import validate_csv
from gemini_integration import *


st.title("Check Your A/B Experiment Results")

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
