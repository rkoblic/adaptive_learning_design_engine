"""Curriculum generation prompt with embedded learning science frameworks."""

import json


def build_curriculum_prompt(confirmed_data: dict) -> str:
    """
    Build the prompt for generating the full curriculum.

    This prompt embeds:
    - Kolb's Experiential Learning Cycle
    - DEAL Reflection Model
    - Bloom's Taxonomy
    - Zone of Proximal Development (scaffolding)
    - Authentic Assessment principles

    Args:
        confirmed_data: Dict with all confirmed learner, project, gap, and institution data

    Returns:
        Complete prompt string for Claude
    """
    learner = confirmed_data.get('learner', {})
    project = confirmed_data.get('project', {})
    gaps = confirmed_data.get('gaps', {})
    institution = confirmed_data.get('institution', {})

    # Format lists for prompt
    skills_list = ", ".join(
        [s.get('skill', s) if isinstance(s, dict) else s
         for s in learner.get('confirmed_skills', [])]
    ) or "Not specified"

    coursework_list = ", ".join(learner.get('confirmed_coursework', [])) or "Not specified"
    preferences_list = ", ".join(learner.get('learning_preferences', [])) or "Not specified"

    deliverables_list = json.dumps(project.get('confirmed_deliverables', []), indent=2)
    technical_skills = json.dumps(project.get('confirmed_technical_skills', []), indent=2)
    professional_skills = json.dumps(project.get('confirmed_professional_skills', []), indent=2)
    domain_knowledge = json.dumps(project.get('confirmed_domain_knowledge', []), indent=2)
    success_criteria = json.dumps(project.get('confirmed_success_criteria', []), indent=2)

    strong_matches = json.dumps(gaps.get('strong_matches', []), indent=2)
    skill_gaps = json.dumps(gaps.get('skill_gaps', []), indent=2)

    competency_frameworks = ", ".join(institution.get('competency_framework', [])) or "None"

    # Build fixed objectives list from user selection
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

    prompt = f"""You are an expert instructional designer specializing in experiential learning and work-integrated learning curriculum. You design credit-bearing courses that transform workplace projects into structured educational experiences.

Your designs are grounded in established learning science:
- Kolb's Experiential Learning Cycle (every module includes Concrete Experience, Reflective Observation, Abstract Conceptualization, and Active Experimentation)
- The DEAL reflection model (Describe, Examine, Articulate Learning)
- Bloom's Taxonomy for learning objectives
- Authentic assessment principles
- Zone of Proximal Development for appropriate scaffolding

## LEARNER PROFILE (Confirmed)
- Name: {learner.get('learner_name', 'Student')}
- Academic Level: {learner.get('academic_level', 'Not specified')}
- Major/Program: {learner.get('major_or_program', 'Not specified')}
- Current Skills: {skills_list}
- Experience Level: {learner.get('experience_level', 'some_experience')}
- Relevant Coursework: {coursework_list}
- Career Goals: {learner.get('career_goals', 'Not specified')}
- Learning Preferences: {preferences_list}

## PROJECT DETAILS (Confirmed)
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
- Team Size: {project.get('team_size', 'Individual')}

## SKILL GAP ANALYSIS (Confirmed)
- Strong Matches: {strong_matches}
- Development Areas: {skill_gaps}
- Scaffolding Recommendation: {gaps.get('scaffolding_recommendation', 'moderate')}
- Overall Fit: {gaps.get('overall_fit', 'good')}

## INSTITUTIONAL CONSTRAINTS
- Credit Hours: {institution.get('credit_hours', '3')}
- Term Length: {institution.get('term_length_weeks', '14')} weeks
- Hours Per Week: {institution.get('hours_per_week', '9')}
- Institution: {institution.get('institution_name', 'University')}
- Grading Scale: {institution.get('grading_scale', 'Letter Grade (A-F)')}
- Competency Framework(s): {competency_frameworks}

## TASK

Generate a complete course shell including ALL of the following sections:

---

### 1. COURSE HEADER
- Course title (generated from project + institution)
- Credit hours and term length
- Course description (2-3 paragraphs synthesizing project and learning goals)

---

### 2. LEARNING OBJECTIVES

#### Fixed Objectives (Transferable Professional Skills)
Generate objectives covering ONLY the selected areas (user has chosen these):
{fixed_objectives_list}

Note: Only generate objectives for the areas listed above. If none are selected, skip this section entirely.

#### Variable Objectives (Project-Specific)
Generate 3-5 objectives derived from:
- The confirmed skill gaps (these become learning objectives)
- Technical/functional skills required by the project
- Domain knowledge for the industry

**All objectives must:**
- Begin with a Bloom's taxonomy action verb
- Be measurable and specific
- Include the cognitive level in parentheses (e.g., "Apply", "Analyze", "Evaluate", "Create")

Bloom's Levels and Example Verbs:
- Remember: Define, list, identify, recall
- Understand: Explain, describe, summarize, interpret
- Apply: Implement, execute, use, demonstrate
- Analyze: Differentiate, organize, compare, examine
- Evaluate: Critique, judge, assess, justify
- Create: Design, construct, develop, produce

---

### 3. WEEKLY SCHEDULE

Generate a week-by-week structure for ALL {institution.get('term_length_weeks', '14')} weeks.

**Each week MUST include ALL FOUR phases of Kolb's Cycle:**

```
### Week [N]: [Theme/Focus]

#### Concrete Experience
[Description of project work, employer interactions, or hands-on activities]

#### Reflective Observation
[DEAL-model reflection prompt specific to this week - see requirements below]

#### Abstract Conceptualization
[Connection to frameworks, concepts, readings, or skill articulation activities]

#### Active Experimentation
[How students will apply insights or iterate on their work]

#### Deliverables Due
- [List any deliverables due this week]

#### Milestone Check-in
[Description of any check-ins with employer or instructor]
```

IMPORTANT: Use ### (H3) for week headers and #### (H4) for subsections. Do NOT use ## (H2) for individual weeks - that header level is reserved for main sections only.

**Pacing guidance:**
- Weeks 1-2: Onboarding, context-setting, initial planning
- Weeks 3 to N-2: Core project execution cycles
- Week N-1: Synthesis, final deliverable preparation
- Week N: Presentation, final reflection, wrap-up

---

### 4. REFLECTION PROMPTS (DEAL Model)

For EACH week's Reflective Observation section, generate a specific reflection prompt following the DEAL framework:

**Describe:** What happened? What did you do? What did you observe?
- Must reference SPECIFIC activities from that week's Concrete Experience

**Examine:** Analyze the experience through one or more lenses:
- Personal growth (What did this reveal about your strengths, challenges, or interests?)
- Academic connection (How does this connect to concepts from your coursework?)
- Professional development (What did you learn about workplace norms, communication, or collaboration?)
- The lens should vary week to week

**Articulate Learning:** What specifically did you learn? How will you apply this going forward?
- Must connect to at least one learning objective

IMPORTANT: Reflection prompts must be SPECIFIC to each week's activities, not generic questions.

---

### 5. ASSESSMENT PACKAGE

#### 5a. Deliverable Rubric
Generate a detailed rubric for the primary project deliverables.

Format as a table with criteria:
| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |

Include criteria for:
- Technical quality of deliverable
- Alignment with project requirements/employer expectations
- Professional presentation
- Evidence of iteration based on feedback

#### 5b. Professional Skills Rubric
Generate a rubric for transferable skills:

| Skill Area | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |

Include: Communication, Time Management, Collaboration, Problem-Solving, Professionalism

#### 5c. Reflection Quality Rubric
Generate a rubric based on DEAL model:

| Dimension | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |

Include: Description (accuracy, detail), Examination (depth of analysis), Articulated Learning (specificity, application)

#### 5d. Employer Evaluation Form
Generate a structured form for the employer mentor:

```
EMPLOYER EVALUATION FORM

Student Name: _________________
Project: {project.get('project_title', 'Project')}
Company: {project.get('company_name', 'Organization')}
Evaluator: _________________
Date: _________________

Please rate the student on the following dimensions (1-5 scale):

WORK QUALITY
[ ] Quality of deliverables produced
[ ] Attention to detail
[ ] Technical competence
Comments: _________________

PROFESSIONALISM
[ ] Reliability and punctuality
[ ] Communication responsiveness
[ ] Receptiveness to feedback
Comments: _________________

COLLABORATION
[ ] Contribution to team (if applicable)
[ ] Interaction with stakeholders
[ ] Initiative and proactivity
Comments: _________________

OVERALL
Would you recommend this student for future opportunities? [ ] Yes [ ] No [ ] Maybe
What was the student's greatest strength?
What is one area for growth?
Additional comments:
```

#### 5e. Student Self-Assessment
Generate a self-assessment aligned to learning objectives:

```
STUDENT SELF-ASSESSMENT

For each learning objective, rate your proficiency at START and END (1-5):

| Learning Objective | Start | End | Evidence of Growth |
|--------------------|-------|-----|-------------------|
| [Each objective from section 2] | [ ] | [ ] | _________________ |

Reflection Questions:
1. Which objective did you make the most progress on? What contributed to that growth?
2. Which objective remains an area for development? What would help you improve?
3. How has this experience influenced your career goals or interests?
4. What would you do differently if you were starting this project again?
```

---

### 6. GRADING BREAKDOWN

Generate based on grading scale: {institution.get('grading_scale', 'Letter Grade (A-F)')}

**For Letter Grade:**
```
Project Deliverable(s): 40%
Weekly Reflections: 25%
Professional Skills Assessment: 20%
Final Self-Assessment & Synthesis: 10%
Employer Evaluation: 5%
```

**For Pass/Fail:**
```
To pass, students must:
- Complete all project deliverables to at least "Proficient" level
- Submit all weekly reflections meeting "Proficient" criteria
- Receive satisfactory employer evaluation
- Complete final self-assessment
```

**For Competency-Based:**
```
Students must demonstrate proficiency in all learning objectives:
- [List each objective with mastery criteria]
```

---

Format the output in clean Markdown with clear section headers. The document should look professional and be ready to share with university stakeholders."""

    return prompt
