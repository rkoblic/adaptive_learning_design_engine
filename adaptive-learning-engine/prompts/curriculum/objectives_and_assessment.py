"""Step 1: Generate learning objectives and assessment strategy."""

from .shared_context import (
    format_learner_context,
    format_project_context,
    format_gaps_context,
    format_institution_context,
    format_fixed_objectives_selection,
)


def build_objectives_and_assessment_prompt(confirmed_data: dict) -> str:
    """
    Build prompt for Step 1: Generate learning objectives and assessment strategy.

    This is the foundation for the course - objectives drive everything else.
    User will review and edit before proceeding to course outline.

    Args:
        confirmed_data: Dict with learner, project, gaps, and institution data

    Returns:
        Prompt string for Claude
    """
    learner = confirmed_data.get('learner', {})
    project = confirmed_data.get('project', {})
    gaps = confirmed_data.get('gaps', {})
    institution = confirmed_data.get('institution', {})

    learner_context = format_learner_context(learner)
    project_context = format_project_context(project)
    gaps_context = format_gaps_context(gaps)
    institution_context = format_institution_context(institution)
    fixed_objectives_selection = format_fixed_objectives_selection(institution)

    grading_scale = institution.get('grading_scale', 'Letter Grade (A-F)')

    prompt = f"""You are an expert instructional designer specializing in experiential learning and work-integrated learning curriculum.

Your task is to generate learning objectives and an assessment strategy for a credit-bearing experiential learning course.

{learner_context}

{project_context}

{gaps_context}

{institution_context}

## USER'S SELECTED FIXED OBJECTIVES
The user has selected these professional skill areas to include:
{fixed_objectives_selection}

## TASK

Generate learning objectives and assessment strategy as JSON. Your response must be ONLY valid JSON, no other text.

### Learning Objectives Requirements

**Fixed Objectives (Professional Skills)**
For EACH selected professional skill area above, generate ONE well-crafted learning objective that:
- Begins with a Bloom's taxonomy action verb
- Is measurable and specific to this experiential context
- Do NOT include the cognitive level in the text (it will be shown separately as a tag)

**Variable Objectives (Project-Specific)**
Generate 3-5 objectives derived from:
- The confirmed skill gaps (these become learning objectives)
- Technical/functional skills required by the project
- Domain knowledge for the industry

Each variable objective must:
- Begin with a Bloom's taxonomy action verb
- Be measurable and specific
- Do NOT include the cognitive level in the text (it will be shown separately as a tag)
- Reference a specific skill gap or project requirement

Bloom's Levels and Example Verbs:
- Remember: Define, list, identify, recall
- Understand: Explain, describe, summarize, interpret
- Apply: Implement, execute, use, demonstrate
- Analyze: Differentiate, organize, compare, examine
- Evaluate: Critique, judge, assess, justify
- Create: Design, construct, develop, produce

### Assessment Strategy Requirements

Generate an assessment strategy appropriate for grading scale: {grading_scale}

**For Letter Grade (A-F):**
Include percentage breakdown:
- Project Deliverable(s): 40%
- Weekly Reflections: 25%
- Professional Skills Assessment: 20%
- Final Self-Assessment & Synthesis: 10%
- Employer Evaluation: 5%

**For Pass/Fail:**
Include proficiency requirements for passing.

**For Competency-Based:**
Include proficiency levels for each objective.

**Final Deliverable:**
Based on the project requirements, describe the final deliverable the student will produce. Include:
- A clear title for the deliverable
- A 2-3 sentence description of what it is
- 3-5 key components or sections that make up the deliverable

## OUTPUT FORMAT

Return ONLY this JSON structure:

```json
{{
  "fixed_objectives": [
    {{
      "id": "fixed_1",
      "skill_area": "project_management",
      "text": "Demonstrate effective project planning by...",
      "bloom_level": "Apply"
    }}
  ],
  "variable_objectives": [
    {{
      "id": "var_1",
      "text": "Apply data analysis techniques to...",
      "bloom_level": "Apply",
      "source": "skill_gap",
      "source_detail": "Data analysis identified as development area"
    }}
  ],
  "assessment_strategy": {{
    "grading_scale": "{grading_scale}",
    "grading_breakdown": {{
      "project_deliverables": {{"weight": 40, "description": "Quality and completion of project deliverables"}},
      "weekly_reflections": {{"weight": 25, "description": "Depth and quality of DEAL-model reflections"}},
      "professional_skills": {{"weight": 20, "description": "Demonstrated growth in professional competencies"}},
      "self_assessment": {{"weight": 10, "description": "Final synthesis and self-evaluation"}},
      "employer_evaluation": {{"weight": 5, "description": "Workplace mentor feedback"}}
    }},
    "final_deliverable": {{
      "title": "Marketing Campaign Strategy & Implementation Report",
      "description": "A comprehensive document presenting the complete marketing campaign developed for the client, including research findings, strategy rationale, and implementation results.",
      "components": [
        "Executive Summary",
        "Market Research & Customer Personas",
        "Campaign Strategy & Content Calendar",
        "Implementation Results & Analytics",
        "Recommendations for Future Campaigns"
      ]
    }}
  }}
}}
```"""

    return prompt
