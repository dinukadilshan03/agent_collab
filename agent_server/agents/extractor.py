from utils.llm_api import call_llm

def run_agent(report_text: str) -> dict:
    prompt = f"""
You are a highly accurate and thorough medical report data extraction specialist. Your task is to analyze the provided medical report and extract structured information into a specific JSON format.

<extraction_instructions>
1.  **Be Comprehensive:** Extract all available information that fits into the specified JSON schema.
2.  **Be Precise:** Copy values exactly as they appear in the report (e.g., "168/95", "102 bpm").
3.  **Categorize Correctly:** Pay close attention to the context to distinguish between past history, admission details, and discharge details.
4.  **Use Arrays:** For fields that can have multiple values (e.g., diagnoses, medications, allergies), always use a list, even if there is only one item.
5.  **Handle Missing Data:** If a value is not mentioned in the report, set it to `null`.
6.  **Handle Unspecified Data:** For any medically relevant information that does not fit neatly into the predefined schema below, summarize it concisely and add it to the `"other_notes"` array. This includes:
    - Details of the "History of Present Illness" (HPI)
    - Detailed physical exam findings beyond vitals
    - Narrative portions of the hospital course
    - Specific discharge instructions
    - Any other notable findings, symptoms, or context not captured elsewhere.
</extraction_instructions>

<output_format>
You MUST return ONLY a valid JSON object that strictly follows this schema. Do not add any other text before or after the JSON object.

{{
  "patient_information": {{
    "name": "string | null",
    "mrn": "string | null",
    "date_of_birth": "string | null",
    "gender": "string | null",
    "admission_date": "string | null",
    "discharge_date": "string | null"
  }},
  "clinical_team": {{
    "attending_physician": "string | null"
  }},
  "medical_history": {{
    "past_medical_history": ["list", "of", "conditions", "or", "null"],
    "past_surgical_history": ["list", "of", "procedures", "or", "null"],
    "allergies": ["list", "of", "allergies", "and", "reactions", "or", "null"],
    "social_history": {{
      "smoking_status": "string | null",
      "alcohol_use": "string | null"
    }}
  }},
  "clinical_findings": {{
    "vitals_on_admission": {{
      "blood_pressure": "string | null",
      "heart_rate": "string | null",
      "temperature": "string | null",
      "respiratory_rate": "string | null",
      "o2_saturation": "string | null"
    }},
    "labs": {{
      "troponin": "string | null",
      "hba1c": "string | null"
    }},
    "key_procedures": ["list", "of", "procedures", "with", "dates", "or", "null"]
  }},
  "assessment_and_diagnosis": {{
    "primary_diagnosis": "string | null",
    "discharge_diagnoses": ["list", "of", "all", "discharge", "diagnoses", "or", "null"],
    "icd10_codes": ["list", "of", "codes", "if", "available", "or", "null"]
  }},
  "medications": {{
    "home_medications": ["list", "of", "meds", "on", "admission", "or", "null"],
    "discharge_medications": ["list", "of", "meds", "at", "discharge", "or", "null"]
  }},
  "plan_and_follow_up": {{
    "follow_up_instructions": ["list", "of", "instructions", "or", "null"]
  }},
  "other_notes": [
    "list",
    "of",
    "strings",
    "summarizing",
    "any",
    "other",
    "relevant",
    "information",
    "not",
    "captured",
    "above",
    "or",
    "null"
  ]
}}
</output_format>

Now, analyze the following medical report and extract the data accordingly.

MEDICAL REPORT:
{report_text}

EXTRACTED JSON:
"""

    return call_llm(prompt)

if __name__ == "__main__":
    print("Extractor module loaded.")