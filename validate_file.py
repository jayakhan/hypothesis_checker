import re
import pandas as pd


def validate_csv(df):
    """Validates the CSV file format and content. Returns (bool, error_message)"""

    # 1. Check if the first row has column names (Pandas assumes this, but we check explicitly)
    if df.empty:
        return False, "The uploaded CSV is empty."

    # 2. Ensure column names are valid (no special characters except underscore)
    if any(re.search(r"[^a-zA-Z0-9_ ]", col) for col in df.columns):
        return (
            False,
            "Column names should only contain letters, numbers, and underscores.",
        )

    # 3. Ensure there is a 'Group' column
    if "Group" not in df.columns:
        return (
            False,
            "The CSV must have a column named 'Group' that identifies Control and Treatment groups.",
        )

    # 4. Ensure 'Group' column contains both "Control" and "Treatment"
    unique_groups = df["Group"].dropna().unique()
    if not set(["Control", "Treatment"]).issubset(set(unique_groups)):
        return (
            False,
            "The 'Group' column must contain both 'Control' and 'Treatment' labels.",
        )

    # 5. Ensure 'Group' column is not empty
    if df["Group"].isnull().all():
        return False, "The 'Group' column should not be entirely empty."

    # 6. Ensure other columns are not entirely blank
    numerical_columns = [
        col
        for col in df.columns
        if col != "Group" and pd.api.types.is_numeric_dtype(df[col])
    ]
    if not numerical_columns:
        return False, "There must be at least one numerical column for analysis."

    # Ensure no numerical column is completely blank
    for col in numerical_columns:
        if df[col].isnull().all():
            return (
                False,
                f"The column '{col}' is entirely blank and cannot be used for A/B testing.",
            )

    return True, None  # Passed validation
