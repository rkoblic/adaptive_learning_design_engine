"""Step 3: Generate detailed week content with Kolb cycles and DEAL reflections."""

from .shared_context import (
    format_learner_context,
    format_project_context,
    format_objectives_for_downstream,
    format_outline_for_downstream,
)


def build_week_detail_prompt(
    confirmed_data: dict,
    objectives: dict,
    outline: dict,
    week_num: int,
    feedback: str = None
) -> str:
    """
    Build prompt for Step 3: Generate detailed content for a single week.

    This creates the full Kolb cycle and DEAL reflection for one week.
    Can be called multiple times (once per week) or regenerated with feedback.

    Args:
        confirmed_data: Dict with learner, project, gaps, and institution data
        objectives: Finalized objectives from Step 1
        outline: Course outline from Step 2
        week_num: Which week to generate (1-indexed)
        feedback: Optional user feedback for regeneration

    Returns:
        Prompt string for Claude
    """
    learner = confirmed_data.get('learner', {})
    project = confirmed_data.get('project', {})
    institution = confirmed_data.get('institution', {})

    learner_context = format_learner_context(learner)
    project_context = format_project_context(project)
    objectives_context = format_objectives_for_downstream(objectives)
    outline_context = format_outline_for_downstream(outline)

    term_length = int(institution.get('term_length_weeks', '14'))
    scaffolding = confirmed_data.get('gaps', {}).get('scaffolding_recommendation', 'moderate')

    # Get this week's outline info
    weeks = outline.get('weeks', [])
    this_week = next((w for w in weeks if w.get('week') == week_num), {})
    week_theme = this_week.get('theme', f'Week {week_num}')
    week_milestone = this_week.get('milestone', 'Progress check')
    week_deliverables = this_week.get('deliverables', [])
    week_activities = this_week.get('key_activities', [])

    # Get adjacent weeks for context
    prev_week = next((w for w in weeks if w.get('week') == week_num - 1), None)
    next_week = next((w for w in weeks if w.get('week') == week_num + 1), None)

    prev_context = f"Previous week ({week_num-1}): {prev_week.get('theme', 'N/A')}" if prev_week else "This is the first week"
    next_context = f"Next week ({week_num+1}): {next_week.get('theme', 'N/A')}" if next_week else "This is the final week"

    # Determine week phase for appropriate framing
    if week_num <= 2:
        phase = "onboarding"
        phase_guidance = "Focus on orientation, relationship building, and establishing foundations."
    elif week_num >= term_length - 1:
        phase = "wrap-up"
        phase_guidance = "Focus on synthesis, final deliverables, and reflection on overall learning."
    elif week_num == term_length - 2:
        phase = "synthesis"
        phase_guidance = "Focus on bringing work together, preparing final deliverables, and deeper reflection."
    else:
        phase = "core"
        phase_guidance = "Focus on active project work, skill development, and iterative progress."

    # Format deliverables for this week
    deliverables_text = "\n".join([f"- {d}" for d in week_deliverables]) if week_deliverables else "- Weekly reflection"
    activities_text = "\n".join([f"- {a}" for a in week_activities]) if week_activities else "- Continue project work"

    # Add regeneration feedback if provided
    feedback_section = ""
    if feedback:
        feedback_section = f"""
## USER FEEDBACK FOR REGENERATION
The user has requested changes to this week's content:
{feedback}

Please incorporate this feedback while maintaining the Kolb cycle structure and DEAL reflection format.
"""

    prompt = f"""You are an expert instructional designer specializing in experiential learning using Kolb's Experiential Learning Cycle and the DEAL reflection model.

Your task is to generate detailed content for Week {week_num} of an experiential learning course.

{learner_context}

{project_context}

{objectives_context}

{outline_context}

## WEEK {week_num} CONTEXT
- Theme: {week_theme}
- Milestone: {week_milestone}
- Phase: {phase} ({phase_guidance})
- {prev_context}
- {next_context}
- Scaffolding level: {scaffolding}

## PLANNED DELIVERABLES THIS WEEK
{deliverables_text}

## PLANNED KEY ACTIVITIES
{activities_text}
{feedback_section}
## TASK

Generate detailed content for Week {week_num} in Markdown format.

### Kolb's Experiential Learning Cycle
Each week must include ALL FOUR phases:

1. **Concrete Experience**: Hands-on project work, employer interactions, or activities
   - Be specific about what the student will DO
   - Reference actual project deliverables and activities

2. **Reflective Observation**: DEAL-model reflection prompt
   - **Describe**: What specific activities/experiences to describe
   - **Examine**: Lens for analysis (varies by week - personal growth, academic connection, professional development)
   - **Articulate Learning**: Connection to specific learning objectives

3. **Abstract Conceptualization**: Frameworks, concepts, or skill articulation
   - Connect to relevant professional concepts or academic frameworks
   - Help student understand the "why" behind experiences

4. **Active Experimentation**: Application or iteration
   - How student will apply insights to next steps
   - Preparation for upcoming work

### DEAL Reflection Requirements
The reflection prompt must:
- Reference SPECIFIC activities from this week's Concrete Experience
- Use a varied examination lens (rotate through: personal growth, academic connection, professional development, civic/ethical)
- Connect to at least one specific learning objective
- Be contextual, not generic

## OUTPUT FORMAT

Generate ONLY Markdown in this exact format:

```markdown
### Week {week_num}: {week_theme}

#### Concrete Experience
[2-3 sentences describing specific hands-on activities, project work, or interactions]

#### Reflective Observation

**This Week's DEAL Reflection:**

*Describe:* [Specific prompt asking student to describe this week's activities]

*Examine:* [Specific prompt with chosen lens - e.g., "Through the lens of professional development, analyze..."]

*Articulate Learning:* [Prompt connecting to specific learning objective, e.g., "How did this week's activities advance your ability to [specific objective]?"]

#### Abstract Conceptualization
[2-3 sentences connecting experiences to frameworks, concepts, or professional knowledge]

#### Active Experimentation
[2-3 sentences about applying insights and preparing for next steps]

#### Deliverables Due
{deliverables_text}

#### Milestone Check-in
[1-2 sentences about checkpoint with employer/instructor, aligned to milestone: {week_milestone}]
```

Generate the content now. Be specific and contextual - avoid generic language."""

    return prompt
