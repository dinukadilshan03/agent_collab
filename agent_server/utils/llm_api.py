import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize client
client = genai.Client(api_key=api_key)


def call_llm(prompt: str) -> dict:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_budget=0
                )  # Optional: disables "thinking"
            ),
        )

        content = response.text
        if not content:
            return {"error": "No content in response", "raw": str(response)}

        # Extract JSON from markdown code blocks
        if "```json" in content:
            start = content.find("```json") + 7
            end = content.find("```", start)
            json_content = (
                content[start:end].strip() if end != -1 else content[start:].strip()
            )
        elif "```" in content:
            start = content.find("```") + 3
            end = content.find("```", start)
            json_content = (
                content[start:end].strip() if end != -1 else content[start:].strip()
            )
        else:
            json_content = content.strip()

        return json.loads(json_content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw": content}
    except Exception as e:
        return {"error": str(e)}
