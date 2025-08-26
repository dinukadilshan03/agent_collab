from typing import Dict, Tuple, Optional
import sys
import os

# Add utils directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from utils.llm_api import call_llm

# Reference ranges for common medical tests (values are examples and can be adjusted)
REFERENCE_RANGES = {
    "Hemoglobin": {
        "male": (13.5, 17.5),
        "female": (12.0, 15.5),
        "all": (12.0, 17.5),
    },
    "Fasting Glucose": {
        "all": (70, 99),
    },
    "ALT": {
        "male": (10, 40),
        "female": (7, 35),
        "all": (7, 40),
    },
    "Creatinine": {
        "male": (0.74, 1.35),
        "female": (0.59, 1.04),
        "all": (0.59, 1.35),
    },
    "Platelet Count": {
        "all": (150, 450),
    },
    "WBC": {
        "all": (4.0, 11.0),
    },
}


def classify_report(
    report: Dict[str, Tuple[float, Optional[str]]],
    reference_ranges: Optional[Dict] = None,
) -> Dict[str, str]:
    """
    Main agent function: Classify a medical report using Gemini LLM.
    Input: {test_name: (value, gender)}, optional reference_ranges from report
    Output: {test_name: classification}
    """
    # Use provided reference ranges first, fallback to default ranges
    ranges_to_use = reference_ranges if reference_ranges else REFERENCE_RANGES

    # Prepare context for LLM
    test_info = []
    for test, (value, gender) in report.items():
        test_ranges = ranges_to_use.get(test)
        ref_info = ""
        if test_ranges:
            if isinstance(test_ranges, dict):  # Gender-specific ranges
                ref_range = test_ranges.get(gender or "all", test_ranges.get("all"))
            else:  # Simple tuple (low, high)
                ref_range = test_ranges

            if ref_range:
                if isinstance(ref_range, tuple):
                    low, high = ref_range
                    ref_info = f" (ref: {low}-{high})"
        test_info.append(f"- {test}: {value}{ref_info}")

    # Determine if using report-provided ranges or fallback
    range_source = "report-provided" if reference_ranges else "standard fallback"

    prompt = f"""
    You are a medical lab report classifier. Analyze the following complete lab report and classify each test result.
    
    Lab Results:
    {chr(10).join(test_info)}
    
    Reference Range Source: {range_source} ranges
    
    For each test, classify as:
    - Normal
    - Borderline low
    - Borderline high  
    - Mildly Abnormal low
    - Mildly Abnormal high
    - Severely Abnormal low
    - Severely Abnormal high
    
    Classification Algorithm:
    1. PRIORITY: Use the reference ranges provided with each test result if available
    2. If no reference ranges are provided in the report, use standard medical reference ranges
    
    3. Classification logic:
       - If low ≤ value ≤ high: classify as "Normal"
       - For values outside range, calculate deviation:
         * Below range: deviation = (low - value) / (high - low)
         * Above range: deviation = (value - high) / (high - low)
       - Apply thresholds:
         * deviation ≤ 0.10: "Borderline [low/high]"
         * deviation ≤ 0.25: "Mildly Abnormal [low/high]"
         * deviation > 0.25: "Severely Abnormal [low/high]"
    
    Consider clinical context and test relationships while following this systematic approach.
    
    Respond in JSON format with each test name as key and classification as value:
    {{
        "test_name_1": "classification_1",
        "test_name_2": "classification_2"
    }}
    """

    result = call_llm(prompt)
    if "error" in result:
        # Fallback to rule-based classification
        results = {}
        for test, (value, gender) in report.items():
            results[test] = _fallback_classify(
                test, value, gender or "all", ranges_to_use
            )
        return results

    # Filter result to only include tests from the report
    filtered_result = {}
    for test in report.keys():
        if test in result:
            filtered_result[test] = result[test]
        else:
            # Fallback for missing classifications
            value, gender = report[test]
            filtered_result[test] = _fallback_classify(
                test, value, gender or "all", ranges_to_use
            )

    return filtered_result


def _fallback_classify(
    test_name: str, value: float, gender: str = "all", ranges: Optional[Dict] = None
) -> str:
    """
    Fallback rule-based classification if LLM fails.
    """
    ranges_to_use = ranges if ranges else REFERENCE_RANGES
    test_ranges = ranges_to_use.get(test_name)
    if not test_ranges:
        return "Unknown Test"

    if isinstance(test_ranges, dict):  # Gender-specific ranges
        ref_range = test_ranges.get(gender, test_ranges.get("all"))
    else:  # Simple tuple (low, high)
        ref_range = test_ranges

    if not ref_range:
        return "No Reference Range"

    if isinstance(ref_range, tuple):
        low, high = ref_range
    else:
        return "Invalid Reference Range"

    if low <= value <= high:
        return "Normal"

    if value < low:
        deviation = (low - value) / (high - low)
        direction = "low"
    else:
        deviation = (value - high) / (high - low)
        direction = "high"

    if deviation <= 0.10:
        return f"Borderline {direction}"
    elif deviation <= 0.25:
        return f"Mildly Abnormal {direction}"
    else:
        return f"Severely Abnormal {direction}"


if __name__ == "__main__":
    # Example usage
    sample_report = {
        "Hemoglobin": (11.5, "female"),
        "Fasting Glucose": (110, None),
        "ALT": (45, "male"),
        "Creatinine": (1.5, "male"),
        "Platelet Count": (140, None),
        "WBC": (12.0, None),
    }
    classifications = classify_report(sample_report)
    for test, result in classifications.items():
        print(f"{test}: {result}")
