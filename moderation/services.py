import json
import os
from anthropic import Anthropic

def get_client():
    return Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def moderate_content(text: str) -> dict:
    client = get_client()

    system_prompt = (
        "You are a content moderation system. Classify the following text into one of "
        "three categories: safe, warning, or violation.\n\n"
        "Respond ONLY with valid JSON in this exact format:\n"
        '{"category": "safe|warning|violation", "severity_score": 0.0-1.0, "reasoning": "brief explanation"}\n\n'
        "Guidelines:\n"
        "- safe: Normal content with no issues (severity_score 0.0-0.3)\n"
        "- warning: Content that is borderline or mildly inappropriate (severity_score 0.3-0.7)\n"
        "- violation: Content that is clearly harmful, hateful, or dangerous (severity_score 0.7-1.0)\n"
    )

    try:
        message = client.messages.create(
            model = "claude-haiku-4-5-20251001",
            max_tokens=256,
            system=system_prompt,
            messages=[
                {"role": "user", "content": text},
            ],
        )
        response_text = message.content[0].text.strip()

        if response_text.startswith("```json"):
            response_text = response_text[7:]
        elif response_text.startswith("```"):
            response_text = response_text[3:]

        if response_text.endswith("```"):
            response_text = response_text[:-3]

        response_text = response_text.strip()

        result = json.loads(response_text)

        if result.get("category") not in ("safe", "warning", "violation"):
            result["category"] = "error"

        result["severity_score"] = max(0.0, min(1.0, float(result.get("severity_score", 0.0))))
        return result
    
    except Exception:
        return {
            "category": "error",
            "severity_score": 0.0,
            "reasoning": "Moderation service encountered an error"
        }