"""Prompt templates for AI extraction and generation."""

from .extraction import build_resume_extraction_prompt, build_project_extraction_prompt
from .gap_analysis import build_gap_analysis_prompt
from .curriculum import build_curriculum_prompt

__all__ = [
    'build_resume_extraction_prompt',
    'build_project_extraction_prompt',
    'build_gap_analysis_prompt',
    'build_curriculum_prompt'
]
