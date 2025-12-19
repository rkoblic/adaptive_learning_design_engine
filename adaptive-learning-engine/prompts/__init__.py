"""Prompt templates for AI extraction and generation."""

from .extraction import build_resume_extraction_prompt, build_project_extraction_prompt
from .gap_analysis import build_gap_analysis_prompt
from .curriculum_legacy import build_curriculum_prompt

# New modular curriculum prompts for incremental generation
from .curriculum.objectives_and_assessment import build_objectives_and_assessment_prompt
from .curriculum.course_outline import build_course_outline_prompt
from .curriculum.week_detail import build_week_detail_prompt

__all__ = [
    'build_resume_extraction_prompt',
    'build_project_extraction_prompt',
    'build_gap_analysis_prompt',
    'build_curriculum_prompt',
    # Modular curriculum prompts
    'build_objectives_and_assessment_prompt',
    'build_course_outline_prompt',
    'build_week_detail_prompt',
]
