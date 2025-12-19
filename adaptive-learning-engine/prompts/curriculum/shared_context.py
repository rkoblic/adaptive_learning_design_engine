"""Shared context formatting helpers for curriculum generation prompts."""

import json


def format_learner_context(learner: dict) -> str:
    """Format learner profile for prompt context."""
    skills_list = ", ".join(
        [s.get('skill', s) if isinstance(s, dict) else s
         for s in learner.get('confirmed_skills', [])]
    ) or "Not specified"

    coursework_list = ", ".join(learner.get('confirmed_coursework', [])) or "Not specified"
    preferences_list = ", ".join(learner.get('learning_preferences', [])) or "Not specified"

    return f"""## LEARNER PROFILE
- Name: {learner.get('learner_name', 'Student')}
- Academic Level: {learner.get('academic_level', 'Not specified')}
- Major/Program: {learner.get('major_or_program', 'Not specified')}
- Current Skills: {skills_list}
- Experience Level: {learner.get('experience_level', 'some_experience')}
- Relevant Coursework: {coursework_list}
- Career Goals: {learner.get('career_goals', 'Not specified')}
- Learning Preferences: {preferences_list}"""


def format_project_context(project: dict) -> str:
    """Format project details for prompt context."""
    deliverables_list = json.dumps(project.get('confirmed_deliverables', []), indent=2)
    technical_skills = json.dumps(project.get('confirmed_technical_skills', []), indent=2)
    professional_skills = json.dumps(project.get('confirmed_professional_skills', []), indent=2)
    domain_knowledge = json.dumps(project.get('confirmed_domain_knowledge', []), indent=2)
    success_criteria = json.dumps(project.get('confirmed_success_criteria', []), indent=2)

    return f"""## PROJECT DETAILS
- Company: {project.get('company_name', 'Partner Organization')}
- Industry: {project.get('industry', 'Not specified')}
- Project Title: {project.get('project_title', 'Experiential Learning Project')}
- Project Summary: {project.get('confirmed_summary', 'Not specified')}
- Deliverables: {deliverables_list}
- Technical Skills Required: {technical_skills}
- Professional Skills Required: {professional_skills}
- Domain Knowledge: {domain_knowledge}
- Success Criteria: {success_criteria}
- Mentorship Level: {project.get('mentorship_level', 'Medium')}
- Team Size: {project.get('team_size', 'Individual')}"""


def format_gaps_context(gaps: dict) -> str:
    """Format skill gap analysis for prompt context."""
    strong_matches = json.dumps(gaps.get('strong_matches', []), indent=2)
    skill_gaps = json.dumps(gaps.get('skill_gaps', []), indent=2)

    return f"""## SKILL GAP ANALYSIS
- Strong Matches: {strong_matches}
- Development Areas: {skill_gaps}
- Scaffolding Recommendation: {gaps.get('scaffolding_recommendation', 'moderate')}
- Overall Fit: {gaps.get('overall_fit', 'good')}"""


def format_institution_context(institution: dict) -> str:
    """Format institutional constraints for prompt context."""
    competency_frameworks = ", ".join(institution.get('competency_framework', [])) or "None"

    return f"""## INSTITUTIONAL CONSTRAINTS
- Credit Hours: {institution.get('credit_hours', '3')}
- Term Length: {institution.get('term_length_weeks', '14')} weeks
- Hours Per Week: {institution.get('hours_per_week', '9')}
- Institution: {institution.get('institution_name', 'University')}
- Grading Scale: {institution.get('grading_scale', 'Letter Grade (A-F)')}
- Competency Framework(s): {competency_frameworks}"""


def format_fixed_objectives_selection(institution: dict) -> str:
    """Format user's selected fixed objectives."""
    fixed_objectives_map = {
        'project_management': 'Project management and organization',
        'professional_communication': 'Professional communication',
        'time_management': 'Time management and accountability',
        'critical_thinking': 'Critical thinking and problem-solving',
        'collaboration': 'Collaboration/teamwork',
        'self_reflection': 'Self-reflection and metacognition'
    }
    selected_fixed = institution.get('fixed_objectives', list(fixed_objectives_map.keys()))
    fixed_objectives_list = "\n".join(
        [f"- {fixed_objectives_map.get(obj, obj)}" for obj in selected_fixed]
    ) or "- None selected"

    return fixed_objectives_list


def format_objectives_for_downstream(objectives: dict) -> str:
    """Format finalized objectives for use in subsequent prompts."""
    fixed = objectives.get('fixed_objectives', [])
    variable = objectives.get('variable_objectives', [])

    fixed_text = "\n".join([f"- {obj.get('text', obj)}" for obj in fixed]) if fixed else "None"
    variable_text = "\n".join([
        f"- {obj.get('text', obj)} (Bloom's: {obj.get('bloom_level', 'Apply')})"
        for obj in variable
    ]) if variable else "None"

    return f"""## FINALIZED LEARNING OBJECTIVES

### Fixed Objectives (Professional Skills)
{fixed_text}

### Variable Objectives (Project-Specific)
{variable_text}"""


def format_outline_for_downstream(outline: dict) -> str:
    """Format course outline for use in week detail generation."""
    header = outline.get('course_header', {})
    weeks = outline.get('weeks', [])

    weeks_text = "\n".join([
        f"- Week {w.get('week', '?')}: {w.get('theme', 'TBD')} | Milestone: {w.get('milestone', 'None')} | Deliverables: {', '.join(w.get('deliverables', [])) or 'None'}"
        for w in weeks
    ]) if weeks else "No weeks defined"

    return f"""## COURSE OUTLINE

### Course Header
- Title: {header.get('title', 'TBD')}
- Description: {header.get('description', 'TBD')}

### Weekly Structure
{weeks_text}"""
