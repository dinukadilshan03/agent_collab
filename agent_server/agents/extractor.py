from utils.llm_api import call_llm

def run_agent(report_text: str) -> dict:
    prompt = (
        "You are a medical report extractor.\n"
        "Extract the following information from the report below:\n"
        "- Patient Name\n"
        "- Diagnosis\n"
        "- HbA1c\n"
        "- Blood Pressure\n"
        "- Any other relevant medical values\n"
        "Return the result as a JSON object.\n\n"
        f"Medical Report:\n{report_text}"
    )

    return call_llm(prompt)

if __name__ == "__main__":
    print("Extractor module loaded.")
