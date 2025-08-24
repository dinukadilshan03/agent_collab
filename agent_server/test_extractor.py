from agents.extractor import run_agent

# Sample medical report text
sample_report = """
Patient Name: John Doe
Diagnosis: Type 2 Diabetes
HbA1c: 8.5%
Blood Pressure: 140/90
Cholesterol: 220 mg/dL
"""

# Run the extractor agent
result = run_agent(sample_report)

# Print the result
print("Extracted Data:")
print(result)
