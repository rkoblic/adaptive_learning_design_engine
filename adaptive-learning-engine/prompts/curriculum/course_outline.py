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

Your task is to generate a high-level course outline with week themes, milestones, and deliverable scheduling.

{learner_context}

{project_context}

{institution_context}

{objectives_context}

## PROJECT DELIVERABLES TO SCHEDULE
{deliverables_text}

## SCAFFOLDING RECOMMENDATION
Based on the learner-project fit analysis: {scaffolding}
- "minimal": Learner is well-prepared, can work more independently
- "moderate": Some guidance needed, balanced support
- "significant": More structure and check-ins needed

## TASK

Generate a course outline as JSON. Your response must be ONLY valid JSON, no other text.

### Course Header
Create a compelling course title and 2-3 paragraph description that:
- Reflects the specific project and learning context
- Highlights experiential learning approach
- Appeals to both academic and professional audiences

### Weekly Structure
Generate an outline for ALL {term_length} weeks with:

**Pacing Guidelines:**
- Weeks 1-2: Onboarding, context-setting, initial planning, relationship building
- Weeks 3 to {int(term_length)-2}: Core project execution cycles
- Week {int(term_length)-1}: Synthesis, final deliverable preparation
- Week {term_length}: Presentation, final reflection, wrap-up

**For Each Week Include:**
- A clear theme (3-6 words)
- A milestone or checkpoint
- Any deliverables due that week (distribute project deliverables appropriately)

**Deliverable Distribution:**
- Schedule smaller/draft deliverables in middle weeks
- Reserve final deliverables for weeks {int(term_length)-1}-{term_length}
- Include reflection submissions each week

## OUTPUT FORMAT

Return ONLY this JSON structure:

```json
{{
  "course_header": {{
    "title": "EXP 495: [Project-Specific Title]",
    "credits": "{institution.get('credit_hours', '3')}",
    "description": "This experiential learning course..."
  }},
  "weeks": [
    {{
      "week": 1,
      "theme": "Onboarding & Context Setting",
      "milestone": "Project kickoff meeting completed",
      "deliverables": ["Learning contract draft"],
      "key_activities": ["Meet with mentor", "Review project scope", "Set communication expectations"]
    }},
    {{
      "week": 2,
      "theme": "Initial Planning & Goal Setting",
      "milestone": "Project plan approved",
      "deliverables": ["Project plan", "Weekly reflection #1"],
      "key_activities": ["Develop timeline", "Identify resources needed", "Establish success metrics"]
    }}
  ]
}}
```

Generate entries for ALL {term_length} weeks following the pacing guidelines above."""

    return prompt
