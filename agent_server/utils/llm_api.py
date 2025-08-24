import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def call_llm(prompt: str) -> dict:
    try:
        response = model.generate_content(prompt)
        content = response.text

        # Extract JSON from markdown code blocks if present
        if "```json" in content:
            # Find the JSON content between ```json and ```
            start = content.find("```json") + 7  # Skip "```json"
            end = content.find("```", start)
            if end != -1:
                json_content = content[start:end].strip()
            else:
                json_content = content[start:].strip()
        elif "```" in content:
            # Handle generic code blocks
            start = content.find("```") + 3
            end = content.find("```", start)
            if end != -1:
                json_content = content[start:end].strip()
            else:
                json_content = content[start:].strip()
        else:
            json_content = content.strip()

        # Try to parse JSON from the extracted content
        return json.loads(json_content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": content}
    except Exception as e:
        return {"error": str(e)}
