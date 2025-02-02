import google.generativeai as genai
import streamlit as st

genai.configure(api_key=api_key)

PROMPT_TEMPLATE = """
You are an AI assistant helping with A/B test analysis. Given the p-values for different metrics, generate an experiment report following this format:

# A/B Experiment Analysis Report

## Summary:
[Brief explanation of whether the experiment resulted in statistically significant differences.]  

**Results Table:**  
| Metric Name            | p-value | Statistical Significance (Yes/No) |
|-----------------------|---------|----------------------------------|
{results_table}


**Next Steps:**  
- For statistically significant metrics (p-value < 0.05), recommend implementing changes if the treatment shows improvement.  
- For non-significant metrics, suggest gathering more data or reconsidering experiment conditions.  
- If all p-values are high, advise checking sample size, experiment duration, or segmenting data for deeper insights.  

**Additional Notes:**  
- If anomalies exist, suggest potential reasons (e.g., insufficient sample size, external factors).  
- Provide any necessary disclaimers regarding data limitations.

Here are the results:  
{p_values}
Please generate the report accordingly.
"""


def generate_results_table(p_values):
    """Creates a markdown table from p-values."""
    table = "| Metric Name | p-value | Statistical Significance |\n"
    table += "|------------|---------|--------------------------|\n"

    for metric, p_value in p_values.items():
        significance = "Yes" if p_value < 0.05 else "No"
        table += f"| {metric} | {p_value:.3f} | {significance} |\n"
    return table


def generate_llm_response(p_values):
    # prompt = f"""Generate a comprehensive report summarizing the results of an A/B test. The test compared a control group and a treatment group and here are the p_values for several columns:{p_values}. The control group is labeled 'control', and the treatment group is labeled 'treatment'. Interpret the p-values, and provide actionable recommendations for next steps (e.g., further testing, implementation of the winning variant). Write the report using {output} template in a clear and concise manner."""
    results_table = generate_results_table(p_values)
    prompt = PROMPT_TEMPLATE.format(results_table=results_table, p_values=p_values)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([prompt])
    return response.text
