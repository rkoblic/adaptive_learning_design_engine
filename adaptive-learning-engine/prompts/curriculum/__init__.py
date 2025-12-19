"""Modular curriculum generation prompts for incremental course building."""

from .objectives_and_assessment import build_objectives_and_assessment_prompt
from .course_outline import build_course_outline_prompt
from .week_detail import build_week_detail_prompt

__all__ = [
    'build_objectives_and_assessment_prompt',
    'build_course_outline_prompt',
    'build_week_detail_prompt',
]
