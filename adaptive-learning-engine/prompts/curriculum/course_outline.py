"""Step 2: Generate course outline with week themes and milestones."""

import json
from .shared_context import (
    format_learner_context,
    format_project_context,
    format_institution_context,
    format_objectives_for_downstream,
)


def build_course_outline_prompt(confirmed_data: dict, objectives: dict) -> str:
    """
    Build prompt for Step 2: Generate high-level course outline.

    This creates the structure/skeleton of the course without detailed weekly content.
    User will review and edit week themes before detailed generation.

    Args:
        confirmed_data: Dict with learner, project, gaps, and institution data
        objectives: Finalized objectives from Step 1

    Returns:
        Prompt string for Claude
    """
    learner = confirmed_data.get('learner', {})
    project = confirmed_data.get('project', {})
    institution = confirmed_data.get('institution', {})

    learner_context = format_learner_context(learner)
    project_context = format_project_context(project)
    institution_context = format_institution_context(institution)
    objectives_context = format_objectives_for_downstream(objectives)

    term_length = institution.get('term_length_weeks', '14')
    scaffolding = confirmed_data.get('gaps', {}).get('scaffolding_recommendation', 'moderate')

    # Format deliverables for scheduling
    deliverables = project.get('confirmed_deliverables', [])
    deliverables_text = json.dumps(deliverables, indent=2) if deliverables else "Not specified"

    prompt = f"""You are an expert instructional designer specializing in experiential learning curriculum.

Generate a high-level course outline (syllabus-style) for a {term_length}-week experiential learning course.

{project_context}

{institution_context}

## PROJECT DELIVERABLES
{deliverables_text}

## TASK

Generate a simple course outline as JSON. Your response must be ONLY valid JSON, no other text.

### Course Header
- A course title reflecting the project
- Credit hours: {institution.get('credit_hours', '3')}
- A 1-2 sentence course description

### Weekly Structure
For each of the {term_length} weeks, provide ONLY:
- Week number
- Theme (3-6 words summarizing the focus)
- Milestone (brief checkpoint, optional for some weeks)

**Pacing:**
- Weeks 1-2: Onboarding and planning
- Middle weeks: Core project work
- Final weeks: Synthesis and presentation

## OUTPUT FORMAT

Return ONLY this JSON:

```json
{{
  "course_header": {{
    "title": "EXP 495: [Title]",
    "credits": "{institution.get('credit_hours', '3')}",
    "description": "Brief course description."
  }},
  "weeks": [
    {{"week": 1, "theme": "Onboarding & Orientation", "milestone": "Project kickoff complete"}},
    {{"week": 2, "theme": "Planning & Goal Setting", "milestone": "Project plan submitted"}}
  ]
}}
```

Generate all {term_length} weeks. Keep it concise - this is a syllabus overview, not detailed lesson plans."""

    return prompt
