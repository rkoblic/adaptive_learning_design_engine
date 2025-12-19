"""Gap analysis prompt for comparing learner skills to project requirements."""

import json


def build_gap_analysis_prompt(learner_extraction: dict, project_extraction: dict) -> str:
    """
    Build the prompt for analyzing skill gaps between learner and project.

    Args:
        learner_extraction: Extracted learner data from resume
        project_extraction: Extracted project data from narrative

    Returns:
        Complete prompt string for Claude
    """
    learner_json = json.dumps(learner_extraction, indent=2)
    project_json = json.dumps(project_extraction, indent=2)

    prompt = f"""You are an expert at matching learner capabilities to project requirements and identifying development opportunities.

Compare the learner's current skills to the project requirements and produce a gap analysis.

## LEARNER SKILLS (extracted from resume)
{learner_json}

## PROJECT REQUIREMENTS (extracted from narrative)
{project_json}

## TASK
Analyze the match between learner and project and return as JSON:

```json
{{
  "strong_matches": [
    {{"learner_skill": "skill", "project_need": "requirement", "match_quality": "direct|transferable"}}
  ],
  "partial_matches": [
    {{"learner_skill": "skill", "project_need": "requirement", "gap_description": "what's missing"}}
  ],
  "skill_gaps": [
    {{
      "project_need": "requirement name",
      "importance": "critical|important|nice_to_have",
      "learning_objective": "Properly formatted learning objective using Bloom's verb",
      "bloom_level": "Remember|Understand|Apply|Analyze|Evaluate|Create"
    }}
  ],
  "fit_assessment": {{
    "overall_fit": "excellent|good|stretch|challenging",
    "rationale": "2-3 sentence explanation",
    "scaffolding_recommendation": "minimal|moderate|significant",
    "key_development_areas": ["area 1", "area 2", "area 3"]
  }}
}}
```

## BLOOM'S TAXONOMY FOR LEARNING OBJECTIVES
For each skill gap, write a measurable learning objective using Bloom's Taxonomy action verbs:

- **Remember**: define, list, identify, recall, name, recognize
- **Understand**: explain, summarize, interpret, describe, classify, compare
- **Apply**: implement, execute, use, demonstrate, solve, apply
- **Analyze**: compare, examine, differentiate, organize, deconstruct, investigate
- **Evaluate**: assess, critique, justify, recommend, judge, defend
- **Create**: design, develop, construct, produce, formulate, compose

**Learning Objective Format**: "[Action verb] + [specific skill/content] + [context/condition for the project]"

**Examples**:
- "Analyze website traffic data using Google Analytics to identify customer acquisition patterns"
- "Design customer persona documents based on market research and user interviews"
- "Implement RESTful API endpoints using Python Flask for data retrieval"
- "Evaluate campaign performance metrics to recommend optimization strategies"

Choose the Bloom's level that matches the depth required by the project (Apply/Analyze for hands-on work, Create for design tasks, Evaluate for assessment tasks).

Guidelines:
- A "strong_match" means the learner has demonstrated this skill and it directly applies
- A "partial_match" means the learner has related experience but would need to extend or adapt
- A "skill_gap" means the project requires something the learner hasn't demonstrated
- "critical" gaps are essential for project success; "nice_to_have" gaps are bonus areas

For fit_assessment:
- "excellent" = learner exceeds requirements, minimal learning stretch
- "good" = solid foundation with room to grow
- "stretch" = significant learning opportunity, achievable with support
- "challenging" = major gaps that may need scope adjustment

Scaffolding recommendation:
- "minimal" = learner can work independently with occasional check-ins
- "moderate" = regular guidance and structured milestones helpful
- "significant" = needs detailed structure, frequent support, and possibly reduced scope

Be encouraging but honest. A "stretch" project is good for learning; a "challenging" fit may need additional support structures or scope adjustment.

Return ONLY the JSON object, no additional text."""

    return prompt
