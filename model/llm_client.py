"""
LLM client for generating yoga routine scripts with weighted segments.
Supports OpenAI-compatible APIs via environment variables.
"""
import os
import json
import logging
from typing import List, Dict, Any, Optional
import requests

logger = logging.getLogger(__name__)

# Default to OpenAI API if no base URL is set
DEFAULT_BASE_URL = "https://api.openai.com/v1"
DEFAULT_MODEL = "gpt-3.5-turbo"


class LLMClientError(Exception):
    """Custom exception for LLM client errors."""
    pass


class LLMClient:
    """Client for communicating with OpenAI-compatible LLM APIs."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.base_url = base_url or os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.getenv("LLM_API_KEY")
        self.model = model or os.getenv("LLM_MODEL", DEFAULT_MODEL)

        if not self.api_key:
            logger.warning("LLM_API_KEY not set - LLM calls will fail")

    def _build_routine_prompt(
        self,
        body_parts: List[str],
        duration_minutes: int,
        difficulty: str
    ) -> str:
        """Build the prompt for generating a yoga routine script."""
        body_parts_str = ", ".join(body_parts) if body_parts else "full body"
        
        return f"""You are a yoga instructor creating a guided yoga routine.

Create a {duration_minutes}-minute yoga routine focusing on: {body_parts_str}
Difficulty level: {difficulty}

Generate a freeform coaching script broken into segments. Each segment should be a phrase or instruction that will be spoken aloud via text-to-speech.

IMPORTANT: You must respond with ONLY valid JSON, no other text. The format must be:
{{
  "segments": [
    {{"text": "Welcome to your yoga practice. Take a deep breath and find a comfortable standing position.", "weight": 2}},
    {{"text": "Begin by rolling your shoulders back and down, releasing any tension.", "weight": 1}},
    ...
  ]
}}

Rules for the response:
1. Each segment's "text" should be a natural spoken phrase (1-3 sentences)
2. The "weight" indicates relative duration (1-5 scale):
   - weight 1: quick transition or brief cue
   - weight 2: short instruction
   - weight 3: standard pose hold
   - weight 4: longer hold or detailed instruction
   - weight 5: extended hold or relaxation
3. Total weights should roughly correspond to {duration_minutes} minutes when distributed
4. Include warm-up, main practice, and cool-down phases
5. Use clear, calming language appropriate for yoga instruction
6. For {difficulty} difficulty, adjust complexity and hold times accordingly

Generate approximately {max(5, duration_minutes * 2)} to {duration_minutes * 4} segments for a {duration_minutes}-minute routine."""

    def generate_routine(
        self,
        body_parts: List[str],
        duration_minutes: int,
        difficulty: str
    ) -> Dict[str, Any]:
        """
        Generate a yoga routine script with weighted segments.

        Args:
            body_parts: List of body parts to focus on
            duration_minutes: Total duration of the routine in minutes
            difficulty: Difficulty level (beginner, intermediate, advanced)

        Returns:
            Dict with 'segments' list and 'total_seconds'

        Raises:
            LLMClientError: If the API call fails or returns invalid data
        """
        if not self.api_key:
            raise LLMClientError("LLM_API_KEY environment variable not set")

        prompt = self._build_routine_prompt(body_parts, duration_minutes, difficulty)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a yoga instructor. Respond only with valid JSON."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            raise LLMClientError("LLM API request timed out")
        except requests.exceptions.RequestException as e:
            raise LLMClientError(f"LLM API request failed: {str(e)}")

        try:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise LLMClientError(f"Invalid response from LLM API: {str(e)}")

        # Parse and validate the JSON response
        return self._parse_routine_response(content, duration_minutes)

    def _parse_routine_response(
        self,
        content: str,
        duration_minutes: int
    ) -> Dict[str, Any]:
        """Parse and validate the LLM response."""
        # Try to extract JSON from the response
        content = content.strip()
        
        # Handle cases where the model wraps JSON in markdown code blocks
        if content.startswith("```"):
            lines = content.split("\n")
            json_lines = []
            in_json = False
            for line in lines:
                if line.startswith("```") and not in_json:
                    in_json = True
                    continue
                elif line.startswith("```") and in_json:
                    break
                elif in_json:
                    json_lines.append(line)
            content = "\n".join(json_lines)

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            raise LLMClientError(f"LLM returned invalid JSON: {str(e)}")

        # Validate structure
        if "segments" not in data:
            raise LLMClientError("LLM response missing 'segments' field")

        segments = data["segments"]
        if not isinstance(segments, list) or len(segments) == 0:
            raise LLMClientError("LLM response 'segments' must be a non-empty list")

        # Validate and normalize each segment
        validated_segments = []
        for i, segment in enumerate(segments):
            if not isinstance(segment, dict):
                raise LLMClientError(f"Segment {i} is not a dictionary")
            
            if "text" not in segment:
                raise LLMClientError(f"Segment {i} missing 'text' field")
            
            text = str(segment["text"]).strip()
            if not text:
                continue  # Skip empty segments

            # Default weight to 2 if not provided or invalid
            weight = segment.get("weight", 2)
            try:
                weight = int(weight)
                weight = max(1, min(5, weight))  # Clamp to 1-5
            except (TypeError, ValueError):
                weight = 2

            validated_segments.append({
                "text": text,
                "weight": weight
            })

        if len(validated_segments) == 0:
            raise LLMClientError("No valid segments in LLM response")

        return {
            "segments": validated_segments,
            "total_seconds": duration_minutes * 60
        }


# Singleton instance for convenience
_client: Optional[LLMClient] = None


def get_llm_client() -> LLMClient:
    """Get or create the singleton LLM client instance."""
    global _client
    if _client is None:
        _client = LLMClient()
    return _client
