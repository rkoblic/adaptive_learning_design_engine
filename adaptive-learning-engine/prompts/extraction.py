"""Extraction prompts for resume and project narrative parsing."""


def build_resume_extraction_prompt(learner_data: dict) -> str:
    """
    Build the prompt for extracting structured data from a resume.

    Args:
        learner_data: Dict with resume_text, major_or_program, academic_level, career_goals

    Returns:
        Complete prompt string for Claude
    """
    resume_text = learner_data.get('resume_text', '')
    major = learner_data.get('major_or_program', 'Not specified')
    level = learner_data.get('academic_level', 'Not specified')
    goals = learner_data.get('career_goals', 'Not specified')

    prompt = f"""You are an expert at analyzing resumes to extract skills, experience, and educational background relevant to workplace learning experiences.

Analyze the following resume and extract structured data. Be thorough but accurate—only extract skills and experience that are clearly evidenced in the resume.

## RESUME TEXT
{resume_text}

## ADDITIONAL CONTEXT
- Student's Major/Program: {major}
- Academic Level: {level}
- Career Goals (if provided): {goals}

## TASK
Extract the following and return as JSON:

```json
{{
  "technical_skills": [
    {{"skill": "skill name", "evidence": "brief quote or context from resume", "proficiency": "beginner|intermediate|advanced"}}
  ],
  "professional_skills": [
    {{"skill": "skill name", "evidence": "brief quote or context from resume"}}
  ],
  "tools_and_platforms": [
    {{"tool": "tool name", "context": "how they used it"}}
  ],
  "relevant_coursework": ["course 1", "course 2"],
  "work_experience_summary": "2-3 sentence summary of relevant work experience",
  "experience_level": "entry|some_experience|experienced",
  "notable_achievements": ["achievement 1", "achievement 2"],
  "inferred_strengths": ["strength 1", "strength 2"],
  "potential_growth_areas": ["area 1", "area 2"]
}}
```

Be conservative—if a skill is only implied but not demonstrated, note it in potential_growth_areas rather than technical_skills. Proficiency should be based on depth of evidence (one mention = beginner, project leadership = advanced).

Return ONLY the JSON object, no additional text."""

    return prompt


def build_project_extraction_prompt(project_data: dict) -> str:
    """
    Build the prompt for extracting structured data from a project narrative.

    Args:
        project_data: Dict with project_narrative, company_name, industry, project_title, etc.

    Returns:
        Complete prompt string for Claude
    """
    narrative = project_data.get('project_narrative', '')
    company = project_data.get('company_name', 'Not specified')
    industry = project_data.get('industry', 'Not specified')
    title = project_data.get('project_title', 'Not specified')
    mentorship = project_data.get('mentorship_level', 'Medium')
    team_size = project_data.get('team_size', 'Individual')

    prompt = f"""You are an expert at analyzing project descriptions to extract structured requirements for experiential learning curriculum design.

Analyze the following project narrative provided by an employer and extract structured data about the project scope, deliverables, and skill requirements.

## PROJECT NARRATIVE
{narrative}

## CONTEXT
- Company: {company}
- Industry: {industry}
- Project Title: {title}
- Mentorship Level: {mentorship}
- Team Size: {team_size}

## TASK
Extract the following and return as JSON:

```json
{{
  "project_summary": "2-3 sentence clear summary of what the student will do",
  "problem_or_opportunity": "What business problem or opportunity does this address?",
  "deliverables": [
    {{"deliverable": "name", "description": "brief description", "type": "document|presentation|analysis|design|code|campaign|other"}}
  ],
  "success_criteria": ["criterion 1", "criterion 2"],
  "technical_skills_required": [
    {{"skill": "skill name", "importance": "required|helpful", "context": "why needed"}}
  ],
  "professional_skills_required": [
    {{"skill": "skill name", "context": "how it will be used"}}
  ],
  "domain_knowledge": [
    {{"area": "knowledge area", "context": "why relevant"}}
  ],
  "weekly_activities_suggested": [
    {{"phase": "early|middle|late", "activity": "description"}}
  ],
  "potential_challenges": ["challenge 1", "challenge 2"],
  "learning_opportunities": ["opportunity 1", "opportunity 2"]
}}
```

Infer skills even if not explicitly stated—for example, a data analysis project implies Excel or data visualization skills. Flag required vs. helpful skills based on how central they are to the deliverables.

Return ONLY the JSON object, no additional text."""

    return prompt
