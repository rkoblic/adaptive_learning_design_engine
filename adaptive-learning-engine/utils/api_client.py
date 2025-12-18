"""Claude API client with retry logic for the Adaptive Learning Design Engine."""

import json
import time
import re
import anthropic
from anthropic import APIError, RateLimitError

from config import Config
from prompts import (
    build_resume_extraction_prompt,
    build_project_extraction_prompt,
    build_gap_analysis_prompt,
    build_curriculum_prompt
)


class ClaudeClient:
    """Wrapper for Claude API with retry logic and structured responses."""

    def __init__(self):
        """Initialize the Claude client."""
        self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        self.model = Config.CLAUDE_MODEL
        self.max_retries = Config.MAX_RETRIES
        self.retry_delay = Config.RETRY_DELAY

    def _call_with_retry(self, messages: list, max_tokens: int) -> str:
        """
        Call Claude API with exponential backoff retry.

        Args:
            messages: List of message dicts for the API
            max_tokens: Maximum tokens in response

        Returns:
            Response text from Claude
        """
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    messages=messages
                )
                return response.content[0].text

            except RateLimitError:
                if attempt < self.max_retries - 1:
                    wait_time = (2 ** attempt) * self.retry_delay
                    time.sleep(wait_time)
                else:
                    raise

            except APIError as e:
                if attempt < self.max_retries - 1 and e.status_code >= 500:
                    wait_time = (2 ** attempt) * self.retry_delay
                    time.sleep(wait_time)
                else:
                    raise

    def _extract_json_from_response(self, text: str) -> str:
        """
        Extract JSON from a response that may have markdown formatting.

        Args:
            text: Raw response text from Claude

        Returns:
            Clean JSON string
        """
        # Try to find JSON in markdown code blocks
        json_pattern = r'```(?:json)?\s*([\s\S]*?)```'
        matches = re.findall(json_pattern, text)

        if matches:
            # Return the first JSON block found
            return matches[0].strip()

        # If no code blocks, try to find raw JSON
        # Look for content starting with { and ending with }
        text = text.strip()
        if text.startswith('{') and text.endswith('}'):
            return text

        # Try to find JSON object in the text
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and end > start:
            return text[start:end + 1]

        return text

    def extract_from_resume(self, learner_data: dict) -> dict:
        """
        Extract structured data from resume using Claude.

        Args:
            learner_data: Dict containing resume_text and learner context

        Returns:
            Dict with extracted skills, experience, coursework, etc.
        """
        prompt = build_resume_extraction_prompt(learner_data)

        response_text = self._call_with_retry(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=Config.EXTRACTION_MAX_TOKENS
        )

        json_str = self._extract_json_from_response(response_text)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Return a default structure if parsing fails
            return {
                "technical_skills": [],
                "professional_skills": [],
                "tools_and_platforms": [],
                "relevant_coursework": [],
                "work_experience_summary": "Unable to parse resume data",
                "experience_level": "entry",
                "notable_achievements": [],
                "inferred_strengths": [],
                "potential_growth_areas": [],
                "parse_error": str(e)
            }

    def extract_from_narrative(self, project_data: dict) -> dict:
        """
        Extract structured data from project narrative using Claude.

        Args:
            project_data: Dict containing project_narrative and context

        Returns:
            Dict with extracted deliverables, requirements, etc.
        """
        prompt = build_project_extraction_prompt(project_data)

        response_text = self._call_with_retry(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=Config.EXTRACTION_MAX_TOKENS
        )

        json_str = self._extract_json_from_response(response_text)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Return a default structure if parsing fails
            return {
                "project_summary": project_data.get('project_narrative', '')[:200],
                "problem_or_opportunity": "",
                "deliverables": [],
                "success_criteria": [],
                "technical_skills_required": [],
                "professional_skills_required": [],
                "domain_knowledge": [],
                "weekly_activities_suggested": [],
                "potential_challenges": [],
                "learning_opportunities": [],
                "parse_error": str(e)
            }

    def analyze_gaps(self, learner_extraction: dict, project_extraction: dict) -> dict:
        """
        Analyze skill gaps between learner and project requirements.

        Args:
            learner_extraction: Extracted learner data from resume
            project_extraction: Extracted project data from narrative

        Returns:
            Dict with matches, gaps, fit assessment, scaffolding recommendation
        """
        prompt = build_gap_analysis_prompt(learner_extraction, project_extraction)

        response_text = self._call_with_retry(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=Config.GAP_ANALYSIS_MAX_TOKENS
        )

        json_str = self._extract_json_from_response(response_text)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            # Return a default structure if parsing fails
            return {
                "strong_matches": [],
                "partial_matches": [],
                "skill_gaps": [],
                "fit_assessment": {
                    "overall_fit": "good",
                    "rationale": "Unable to complete gap analysis",
                    "scaffolding_recommendation": "moderate",
                    "key_development_areas": []
                },
                "parse_error": str(e)
            }

    def generate_curriculum(self, confirmed_data: dict) -> str:
        """
        Generate full curriculum from confirmed data.

        Args:
            confirmed_data: Dict with all confirmed learner, project, gap, and institution data

        Returns:
            Markdown string of complete course shell
        """
        prompt = build_curriculum_prompt(confirmed_data)

        response_text = self._call_with_retry(
            messages=[{"role": "user", "content": prompt}],
            max_tokens=Config.CURRICULUM_MAX_TOKENS
        )

        return response_text
