# Product Requirements Document: Adaptive Learning Design Engine Prototype

## Overview

### Purpose
Build a functional prototype that demonstrates AI-powered curriculum generation for experiential learning. The prototype takes structured inputs about a learner, project, and institutional constraints, then generates a complete course shell grounded in established learning science frameworks.

### Target Users
This prototype is a demonstration tool for Riipen's business development conversations with university partners. It should produce outputs that look like professional course materials a university could actually use.

### Scope
The prototype covers three pipeline stages:
1. **Intake & Mapping** — Accept and structure inputs
2. **Curriculum Generation** — Generate weekly structure, learning objectives, reflection prompts
3. **Assessment Design** — Generate rubrics and evaluation instruments

Out of scope: Delivery/LMS integration, actual student tracking, employer matching.

---

## Technical Architecture

### Recommended Stack
- **Backend**: Python with Flask or FastAPI
- **Frontend**: Simple HTML/CSS form (can use Tailwind for styling) or React if preferred
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514 or claude-sonnet-4-20250514)
- **Output**: Generate both on-screen display and downloadable Markdown file

### Application Flow
```
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: RAW INTAKE                                                         │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │  Resume Upload  │   │ Project Narrative│   │  Institutional  │           │
│  │  (PDF/DOCX)     │   │  (Free text)    │   │  Constraints    │           │
│  └────────┬────────┘   └────────┬────────┘   └────────┬────────┘           │
│           │                     │                     │                     │
│           └─────────────────────┴─────────────────────┘                     │
│                                 │                                           │
│                                 ▼                                           │
│                    ┌────────────────────────┐                              │
│                    │  Submit Raw Inputs     │                              │
│                    └────────────┬───────────┘                              │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  AI EXTRACTION (3 API calls)                                                │
│  ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐           │
│  │ Resume Parser   │   │ Narrative Parser│   │  Gap Analyzer   │           │
│  │ → Skills, etc.  │   │ → Deliverables  │   │ → Matches, Gaps │           │
│  └─────────────────┘   └─────────────────┘   └─────────────────┘           │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: CONFIRM & EDIT                                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Extracted Skills (editable tags)                                   │   │
│  │  Extracted Deliverables (editable list)                             │   │
│  │  Skill Gap Analysis (visual matching)                               │   │
│  │  Scaffolding Recommendation                                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                    ┌────────────────────────┐                              │
│                    │  Confirm & Generate    │                              │
│                    └────────────┬───────────┘                              │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  CURRICULUM GENERATION (1 API call)                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Confirmed inputs → Detailed prompt → Claude API → Course shell     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────┼───────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: OUTPUT                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Complete Course Shell                                              │   │
│  │  • Learning Objectives (Fixed + Variable)                           │   │
│  │  • Weekly Schedule (Kolb-aligned)                                   │   │
│  │  • DEAL Reflection Prompts                                          │   │
│  │  • Assessment Package (Rubrics, Forms)                              │   │
│  │  • Download Options (Markdown, PDF)                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

### File Structure
```
/adaptive-learning-engine/
├── app.py                 # Main Flask/FastAPI application
├── templates/
│   ├── index.html         # Input form
│   └── result.html        # Output display
├── static/
│   └── styles.css         # Styling (if not using Tailwind CDN)
├── prompts/
│   ├── curriculum.py      # Curriculum generation prompt templates
│   └── assessment.py      # Assessment generation prompt templates
├── utils/
│   ├── input_processor.py # Input validation and structuring
│   └── output_formatter.py # Format API response for display
├── requirements.txt
└── README.md
```

---

## Input Specifications

The prototype uses a **two-step intake flow** to minimize manual data entry:

1. **Step 1 - Raw Intake:** User provides unstructured inputs (resume upload, narrative descriptions)
2. **Step 2 - AI Extraction & Confirmation:** System extracts structured data and presents for user review/editing
3. **Step 3 - Generation:** User confirms extracted data and triggers curriculum generation

This approach reflects the real-world use case where learners and employers shouldn't need to manually tag every skill—the AI handles extraction and users just confirm.

---

### Application Flow (Updated)

```
[Step 1: Raw Intake Form] 
    → [AI Extraction API Call] 
    → [Step 2: Confirmation/Edit Form with Pre-filled Data] 
    → [User Confirms] 
    → [Curriculum Generation API Call] 
    → [Step 3: Output Display]
```

---

### Step 1: Raw Intake Form

#### 1a. Learner Profile (Raw Intake)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `learner_name` | text | No | Student name (for personalization in output) |
| `academic_level` | select | Yes | Freshman, Sophomore, Junior, Senior, Graduate |
| `major_or_program` | text | Yes | Student's field of study |
| `resume_file` | file upload | Yes* | PDF or DOCX resume (*or manual entry) |
| `resume_text` | textarea | Yes* | Paste resume text if not uploading file (*or file upload) |
| `career_goals` | textarea | No | Student's career interests or aspirations |
| `skills_to_develop` | textarea | No | Optional: specific skills student wants to work on |
| `learning_preferences` | select (multi) | No | Visual, Reading/Writing, Hands-on, Collaborative, Independent |

**Resume Processing:**
- Accept PDF or DOCX file uploads
- Extract text from uploaded file using appropriate library
- Also allow direct text paste for users without a file handy
- Pass extracted/pasted text to AI for skill extraction

#### 1b. Project & Employer Profile (Raw Intake)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `company_name` | text | Yes | Name of the employer organization |
| `industry` | select | Yes | Industry sector from predefined list with "Other" option |
| `project_title` | text | Yes | Brief title for the project |
| `project_narrative` | textarea (large) | Yes | Free-form description of the project (see prompt below) |
| `mentorship_level` | select | Yes | High (weekly meetings), Medium (bi-weekly), Low (as-needed) |
| `team_size` | select | Yes | Individual, Pair (2), Small Team (3-4), Large Team (5+) |

**Project Narrative Prompt:**
Display this helper text above the `project_narrative` field:

> *Describe the project in your own words. Include:*
> - *What problem or opportunity will the student address?*
> - *What will the student actually do day-to-day?*
> - *What will they produce or deliver by the end?*
> - *What does success look like?*
> - *What skills or background would be helpful (but don't worry about being exhaustive—we'll help identify these)?*
>
> *Write 2-4 paragraphs. The more context you provide, the better we can design the learning experience.*

#### 1c. Institutional Constraints

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `credit_hours` | number | Yes | Number of credit hours (typically 1-4) |
| `term_length_weeks` | number | Yes | Duration in weeks (typically 8-16) |
| `hours_per_week` | number | Yes | Expected student effort per week |
| `institution_name` | text | No | Name of the university (for output branding) |
| `grading_scale` | select | Yes | Letter Grade (A-F), Pass/Fail, Competency-Based |
| `competency_framework` | select (multi) | No | NACE Career Readiness, AAC&U VALUE, Institution-Specific, None |

---

### Step 2: AI Extraction & Confirmation Form

After Step 1 submission, the system calls an extraction API to parse the resume and project narrative. The user then sees a confirmation screen with pre-filled fields they can edit before generation.

#### 2a. Extracted Learner Data (Confirmation)

| Field | Type | Source | User Action |
|-------|------|--------|-------------|
| `extracted_skills` | tag/chip list | AI extraction from resume | Review, add, remove skills |
| `experience_level` | text summary | AI inference from resume | Review, edit if inaccurate |
| `relevant_coursework` | tag/chip list | AI extraction from resume | Review, add, remove |
| `skill_gaps_inferred` | tag/chip list | AI comparison of resume vs project needs | Review, confirm development goals |

**UI Pattern for Skill Confirmation:**
- Display extracted skills as editable tags/chips
- Allow user to click to remove incorrect extractions
- Provide "Add skill" button for missing items
- Show confidence indicator if feasible (e.g., skills mentioned explicitly vs. inferred)
- Group skills by category: Technical, Communication, Analytical, etc.

#### 2b. Extracted Project Data (Confirmation)

| Field | Type | Source | User Action |
|-------|------|--------|-------------|
| `project_summary` | textarea | AI-generated concise summary | Review, edit |
| `deliverables` | editable list | AI extraction from narrative | Review, add, remove, reorder |
| `technical_skills_required` | tag/chip list | AI inference from narrative | Review, add, remove |
| `professional_skills_required` | tag/chip list | AI inference from narrative | Review, add, remove |
| `domain_knowledge` | tag/chip list | AI inference from industry + narrative | Review, add, remove |
| `success_criteria` | editable list | AI extraction from narrative | Review, edit |

**UI Pattern for Deliverables Confirmation:**
- Display as numbered editable list
- Drag to reorder
- Click to edit inline
- Button to add new deliverable
- Each deliverable can be deleted

#### 2c. Skill Gap Analysis (Confirmation)

The system should display a visual comparison:

```
LEARNER'S CURRENT SKILLS          PROJECT REQUIREMENTS
------------------------          --------------------
[Social media management] ────────► [Social media marketing] ✓ Match
[Basic graphic design]    ────────► [Content creation] ✓ Partial
[Written communication]   ────────► [Professional communication] ✓ Match
                                   [Google Analytics] ⚠ Gap - Development Area
                                   [Data visualization] ⚠ Gap - Development Area
                                   [B2B marketing] ⚠ Gap - Development Area
```

This visualization helps users confirm:
1. The skill matching is accurate
2. The identified gaps make sense as learning objectives
3. The project is appropriate for this learner's level

---

### Step 3: Generation

After user confirms extracted data, combine all inputs and call the curriculum generation API.

---

## Output Specifications

The system should generate a comprehensive course shell document with the following sections:

### 1. Course Header
- Course title (generated from project + institution)
- Credit hours and term length
- Course description (2-3 paragraphs synthesizing project and learning goals)

### 2. Learning Objectives

#### Fixed Objectives (always included, adapted to project context)
Generate 4-6 objectives covering transferable professional skills:
- Project management and organization
- Professional communication
- Time management and accountability
- Collaboration/teamwork (if team project)
- Critical thinking and problem-solving
- Self-reflection and metacognition

#### Variable Objectives (derived from project)
Generate 3-5 objectives specific to:
- Technical/functional skills required by the project
- Domain knowledge for the industry
- Specialized professional practices

**All objectives must:**
- Begin with a Bloom's taxonomy action verb
- Be measurable and specific
- Include the cognitive level in parentheses (e.g., "Apply", "Analyze", "Evaluate", "Create")

### 3. Weekly Schedule

Generate a week-by-week structure that:
- Spans the full `term_length_weeks`
- Follows Kolb's Experiential Learning Cycle in each week or module
- Includes specific activities for each phase

**Each week should include:**

```
## Week [N]: [Theme/Focus]

### Concrete Experience
[Description of project work, employer interactions, or hands-on activities for this week]

### Reflective Observation  
[DEAL-model reflection prompt for this week]

### Abstract Conceptualization
[Connection to frameworks, concepts, or skill articulation activities]

### Active Experimentation
[How students will apply insights or iterate on their work]

### Deliverables Due
- [List any deliverables due this week]

### Milestone Check-in
[Description of any check-ins with employer or instructor]
```

**Pacing guidance:**
- Weeks 1-2: Onboarding, context-setting, initial planning
- Weeks 3 to N-2: Core project execution cycles
- Week N-1: Synthesis, final deliverable preparation
- Week N: Presentation, final reflection, wrap-up

### 4. Reflection Prompts (DEAL Model)

Generate a reflection prompt for each week using the DEAL framework:

**Describe:** What happened? What did you do? What did you observe?

**Examine:** Analyze the experience through one or more lenses:
- Personal growth (What did this reveal about your strengths, challenges, or interests?)
- Academic connection (How does this connect to concepts from your coursework?)
- Professional development (What did you learn about workplace norms, communication, or collaboration?)

**Articulate Learning:** What specifically did you learn? How will you apply this going forward?

Each reflection prompt should be specific to that week's activities, not generic.

### 5. Assessment Package

#### 5a. Deliverable Rubric

Generate a detailed rubric for evaluating the primary project deliverable(s). Format as a table:

| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|-----------|---------------|----------------|----------------|---------------|
| [Criterion 1] | [Description] | [Description] | [Description] | [Description] |
| [Criterion 2] | [Description] | [Description] | [Description] | [Description] |
| ... | ... | ... | ... | ... |

Include criteria for:
- Technical quality of deliverable
- Alignment with project requirements/employer expectations
- Professional presentation
- Evidence of iteration based on feedback

#### 5b. Professional Skills Rubric

Generate a rubric for evaluating transferable skills demonstrated throughout the project:

| Skill Area | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|------------|---------------|----------------|----------------|---------------|
| Communication | ... | ... | ... | ... |
| Time Management | ... | ... | ... | ... |
| Collaboration | ... | ... | ... | ... |
| Problem-Solving | ... | ... | ... | ... |
| Professionalism | ... | ... | ... | ... |

#### 5c. Reflection Quality Rubric

Generate a rubric for evaluating reflection submissions based on DEAL model:

| Dimension | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|-----------|---------------|----------------|----------------|---------------|
| Description (accuracy, detail) | ... | ... | ... | ... |
| Examination (depth of analysis) | ... | ... | ... | ... |
| Articulated Learning (specificity, application) | ... | ... | ... | ... |

#### 5d. Employer Evaluation Form

Generate a structured form for the employer mentor to evaluate the student:

```
EMPLOYER EVALUATION FORM

Student Name: _________________
Project: _________________
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

Generate a self-assessment instrument aligned to the learning objectives:

```
STUDENT SELF-ASSESSMENT

Reflect on your growth over the course of this project.

For each learning objective, rate your proficiency at the START and END of the project (1-5):

| Learning Objective | Start | End | Evidence of Growth |
|--------------------|-------|-----|-------------------|
| [Objective 1] | [ ] | [ ] | _________________ |
| [Objective 2] | [ ] | [ ] | _________________ |
| ... | ... | ... | ... |

Reflection Questions:
1. Which objective did you make the most progress on? What contributed to that growth?
2. Which objective remains an area for development? What would help you improve?
3. How has this experience influenced your career goals or interests?
4. What would you do differently if you were starting this project again?
```

### 6. Grading Breakdown

Generate a suggested grading breakdown based on the grading scale selected:

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

## Learning Science Implementation Requirements

The prompt construction must embed these frameworks. This is critical—the output should demonstrably reflect these principles, not just mention them.

### Kolb's Experiential Learning Cycle

Every week/module must include activities mapped to all four phases:
1. **Concrete Experience (CE):** Active engagement with project work
2. **Reflective Observation (RO):** Structured reflection on what happened
3. **Abstract Conceptualization (AC):** Connecting experience to concepts/frameworks
4. **Active Experimentation (AE):** Planning how to apply learning

The prompt should instruct the model to explicitly label which phase each activity addresses.

### DEAL Model for Reflection

All reflection prompts must follow the three-phase structure:
- **Describe:** Objective recounting of experience
- **Examine:** Analysis through personal, academic, and/or professional lenses
- **Articulate Learning:** Specific insights and implications for future action

Prompts should NOT be generic (e.g., "What did you learn?"). They should reference specific activities or challenges from that week.

### Bloom's Taxonomy

All learning objectives must:
- Use appropriate action verbs from Bloom's taxonomy
- Indicate the cognitive level being targeted
- Progress appropriately (foundational skills early, synthesis/evaluation later)

**Bloom's Levels and Example Verbs:**
- **Remember:** Define, list, identify, recall
- **Understand:** Explain, describe, summarize, interpret
- **Apply:** Implement, execute, use, demonstrate
- **Analyze:** Differentiate, organize, compare, examine
- **Evaluate:** Critique, judge, assess, justify
- **Create:** Design, construct, develop, produce

### Zone of Proximal Development (Scaffolding)

The prompt should adjust scaffolding based on:
- `academic_level`: Lower levels get more structured guidance
- `existing_skills`: More scaffolding for skill gaps
- `mentorship_level`: Less scaffolding if high mentorship available

### Authentic Assessment

Rubrics should evaluate:
- Actual work products (not tests about work)
- Process AND product
- Growth over time (via self-assessment)
- Multiple perspectives (self, peer, employer, instructor)

---

## Prompt Construction

### Extraction Prompts (Step 1 → Step 2)

These prompts extract structured data from unstructured inputs. They should return JSON for easy parsing.

#### Resume Extraction Prompt

```
You are an expert at analyzing resumes to extract skills, experience, and educational background relevant to workplace learning experiences.

Analyze the following resume and extract structured data. Be thorough but accurate—only extract skills and experience that are clearly evidenced in the resume.

## RESUME TEXT
{resume_text}

## ADDITIONAL CONTEXT
- Student's Major/Program: {major_or_program}
- Academic Level: {academic_level}
- Career Goals (if provided): {career_goals}

## TASK
Extract the following and return as JSON:

```json
{
  "technical_skills": [
    {"skill": "skill name", "evidence": "brief quote or context from resume", "proficiency": "beginner|intermediate|advanced"}
  ],
  "professional_skills": [
    {"skill": "skill name", "evidence": "brief quote or context from resume"}
  ],
  "tools_and_platforms": [
    {"tool": "tool name", "context": "how they used it"}
  ],
  "relevant_coursework": ["course 1", "course 2"],
  "work_experience_summary": "2-3 sentence summary of relevant work experience",
  "experience_level": "entry|some_experience|experienced",
  "notable_achievements": ["achievement 1", "achievement 2"],
  "inferred_strengths": ["strength 1", "strength 2"],
  "potential_growth_areas": ["area 1", "area 2"]
}
```

Be conservative—if a skill is only implied but not demonstrated, note it in potential_growth_areas rather than technical_skills. Proficiency should be based on depth of evidence (one mention = beginner, project leadership = advanced).
```

#### Project Narrative Extraction Prompt

```
You are an expert at analyzing project descriptions to extract structured requirements for experiential learning curriculum design.

Analyze the following project narrative provided by an employer and extract structured data about the project scope, deliverables, and skill requirements.

## PROJECT NARRATIVE
{project_narrative}

## CONTEXT
- Company: {company_name}
- Industry: {industry}
- Project Title: {project_title}
- Mentorship Level: {mentorship_level}
- Team Size: {team_size}

## TASK
Extract the following and return as JSON:

```json
{
  "project_summary": "2-3 sentence clear summary of what the student will do",
  "problem_or_opportunity": "What business problem or opportunity does this address?",
  "deliverables": [
    {"deliverable": "name", "description": "brief description", "type": "document|presentation|analysis|design|code|campaign|other"}
  ],
  "success_criteria": ["criterion 1", "criterion 2"],
  "technical_skills_required": [
    {"skill": "skill name", "importance": "required|helpful", "context": "why needed"}
  ],
  "professional_skills_required": [
    {"skill": "skill name", "context": "how it will be used"}
  ],
  "domain_knowledge": [
    {"area": "knowledge area", "context": "why relevant"}
  ],
  "weekly_activities_suggested": [
    {"phase": "early|middle|late", "activity": "description"}
  ],
  "potential_challenges": ["challenge 1", "challenge 2"],
  "learning_opportunities": ["opportunity 1", "opportunity 2"]
}
```

Infer skills even if not explicitly stated—for example, a data analysis project implies Excel or data visualization skills. Flag required vs. helpful skills based on how central they are to the deliverables.
```

#### Skill Gap Analysis Prompt

```
You are an expert at matching learner capabilities to project requirements and identifying development opportunities.

Compare the learner's current skills to the project requirements and produce a gap analysis.

## LEARNER SKILLS (extracted from resume)
{extracted_learner_skills_json}

## PROJECT REQUIREMENTS (extracted from narrative)
{extracted_project_requirements_json}

## TASK
Analyze the match between learner and project and return as JSON:

```json
{
  "strong_matches": [
    {"learner_skill": "skill", "project_need": "requirement", "match_quality": "direct|transferable"}
  ],
  "partial_matches": [
    {"learner_skill": "skill", "project_need": "requirement", "gap_description": "what's missing"}
  ],
  "skill_gaps": [
    {"project_need": "requirement", "importance": "critical|important|nice_to_have", "learning_opportunity": "how this becomes a learning objective"}
  ],
  "fit_assessment": {
    "overall_fit": "excellent|good|stretch|challenging",
    "rationale": "2-3 sentence explanation",
    "scaffolding_recommendation": "minimal|moderate|significant",
    "key_development_areas": ["area 1", "area 2", "area 3"]
  }
}
```

Be encouraging but honest. A "stretch" project is good for learning; a "challenging" fit may need additional support structures or scope adjustment.
```

---

### Main Curriculum Generation Prompt (Step 3)

The prompt should be constructed from the **confirmed** extracted data, not raw inputs. This ensures the curriculum reflects user-verified information.

```
You are an expert instructional designer specializing in experiential learning and work-integrated learning curriculum. You design credit-bearing courses that transform workplace projects into structured educational experiences.

Your designs are grounded in established learning science:
- Kolb's Experiential Learning Cycle (every module includes Concrete Experience, Reflective Observation, Abstract Conceptualization, and Active Experimentation)
- The DEAL reflection model (Describe, Examine, Articulate Learning)
- Bloom's Taxonomy for learning objectives
- Authentic assessment principles
- Zone of Proximal Development for appropriate scaffolding

## LEARNER PROFILE (Confirmed)
- Name: {learner_name}
- Academic Level: {academic_level}
- Major/Program: {major_or_program}
- Current Skills: {confirmed_skills_list}
- Experience Level: {experience_level}
- Relevant Coursework: {confirmed_coursework}
- Career Goals: {career_goals}
- Learning Preferences: {learning_preferences}

## PROJECT DETAILS (Confirmed)
- Company: {company_name}
- Industry: {industry}
- Project Title: {project_title}
- Project Summary: {confirmed_project_summary}
- Deliverables: {confirmed_deliverables_list}
- Technical Skills Required: {confirmed_technical_skills}
- Professional Skills Required: {confirmed_professional_skills}
- Domain Knowledge: {confirmed_domain_knowledge}
- Success Criteria: {confirmed_success_criteria}
- Mentorship Level: {mentorship_level}
- Team Size: {team_size}

## SKILL GAP ANALYSIS (Confirmed)
- Strong Matches: {strong_matches}
- Development Areas: {skill_gaps}
- Scaffolding Recommendation: {scaffolding_recommendation}
- Overall Fit: {overall_fit}

## INSTITUTIONAL CONSTRAINTS
- Credit Hours: {credit_hours}
- Term Length: {term_length_weeks} weeks
- Hours Per Week: {hours_per_week}
- Institution: {institution_name}
- Grading Scale: {grading_scale}
- Competency Framework(s): {competency_framework}

## TASK

Generate a complete course shell including:

1. **Course Header**: Title, description, credit information

2. **Learning Objectives**: 
   - 4-6 Fixed Objectives (transferable professional skills)
   - 3-5 Variable Objectives (derived from confirmed skill gaps and project requirements)
   - All objectives must use Bloom's action verbs with cognitive level noted

3. **Weekly Schedule**: 
   - Full {term_length_weeks}-week structure
   - Each week follows Kolb's cycle with labeled phases
   - Include specific activities, deliverable due dates, and check-ins
   - Scaffolding level: {scaffolding_recommendation} (adjust structure accordingly)
   - Reference actual deliverables: {confirmed_deliverables_list}

4. **Reflection Prompts**:
   - One DEAL-model reflection per week
   - Specific to that week's activities (reference actual project work)
   - Connect to identified development areas: {skill_gaps}

5. **Assessment Package**:
   - Deliverable rubric for: {confirmed_deliverables_list}
   - Professional skills rubric
   - Reflection quality rubric
   - Employer evaluation form customized for {company_name}
   - Student self-assessment aligned to learning objectives

6. **Grading Breakdown**: Based on {grading_scale} scale

Format the output in clean Markdown with clear section headers.
```

### Assessment-Specific Prompt (if generating separately)

```
You are an assessment design specialist creating evaluation instruments for experiential learning courses.

Your assessment designs follow authentic assessment principles:
- Evaluate actual work products, not proxies
- Assess both process and product
- Include multiple evaluator perspectives
- Measure growth over time
- Align directly to stated learning objectives

## Context
[Insert course context, learning objectives, and deliverables from curriculum generation]

## Task
Generate the following assessment instruments:

1. **Deliverable Rubric**: 4-point scale evaluating {deliverables}
2. **Professional Skills Rubric**: Evaluating transferable skills
3. **Reflection Quality Rubric**: Based on DEAL model
4. **Employer Evaluation Form**: Structured feedback form
5. **Student Self-Assessment**: Pre/post proficiency ratings with reflection questions

Ensure all rubric criteria are:
- Specific and observable
- Differentiated clearly across performance levels
- Aligned to at least one learning objective
```

---

## UI/UX Requirements

### Step 1: Raw Intake Form

**Layout:**
- Single-page form with three collapsible sections (Learner, Project, Institution)
- All sections expanded by default on desktop; collapsed on mobile
- Clear visual hierarchy with section headers

**Learner Section:**
- Prominent file upload zone for resume (drag-and-drop + click to browse)
- Accepted formats clearly labeled: "PDF or DOCX"
- Fallback textarea: "Or paste your resume text here"
- One of the two (file OR paste) is required
- Other fields below with helpful placeholder text

**Project Section:**
- Large textarea for project narrative with helper prompt displayed above
- Character count or word count indicator
- Minimum length guidance: "Please provide at least 100 words"

**Validation:**
- Required field indicators
- Client-side validation before submission
- Helpful error messages
- File type validation for resume upload

**Loading State:**
- Show progress indicator during extraction API calls
- Message: "Analyzing your inputs... this typically takes 15-30 seconds"
- Consider showing which step is processing (Analyzing resume → Analyzing project → Matching skills)

### Step 2: Confirmation/Edit Form

**Layout:**
- Three-column or tabbed layout showing Learner, Project, and Gap Analysis side by side (desktop)
- Single column with sections on mobile
- Each section clearly labeled as "Review & Edit"

**Skill Display (Learner & Project):**
- Display skills as editable tag/chip components
- Each chip has an "×" to remove
- "Add skill" button at end of each skill list
- Click on chip to edit text inline
- Color coding by category (Technical = blue, Professional = green, etc.)
- Subtle confidence indicator if available (solid border = explicit, dashed = inferred)

**Deliverables Display:**
- Numbered editable list
- Each item has edit (pencil) and delete (trash) icons
- Drag handles for reordering
- "Add deliverable" button at bottom

**Gap Analysis Display:**
- Visual matching diagram (see spec in Input Specifications)
- Matches shown in green, gaps shown in amber
- Gaps are selectable to confirm as learning objectives
- Scaffolding recommendation displayed with explanation

**Confirmation Actions:**
- "Looks Good - Generate Course" primary button
- "Go Back & Edit Inputs" secondary link
- Summary of what will be generated

### Step 3: Output Display

**Layout:**
- Professional document-style display
- Sticky table of contents / section navigation on left (desktop)
- Collapsible sections for long content (weekly schedule, rubrics)
- Print-friendly styling

**Header:**
- Course title prominently displayed
- Institution name and Riipen logo placeholder
- Credit hours, term length summary

**Navigation:**
- Jump links to: Objectives, Weekly Schedule, Assessments
- "Expand All" / "Collapse All" for weekly schedule
- Back-to-top button

**Actions:**
- "Download as Markdown" button (prominent)
- "Download as PDF" button (stretch goal)
- "Copy Section" buttons for individual sections
- "Start Over" link (returns to Step 1)
- "Edit Inputs" link (returns to Step 2 with data preserved)

**Responsive:**
- Full document view on desktop
- Simplified navigation on mobile
- Sections stack vertically

---

## Example Input/Output

### Example Step 1 Input (Raw Intake)

**Learner Resume Text (from uploaded PDF):**
```
JORDAN SMITH
Marketing Major | State University | Class of 2025
jordan.smith@email.com | (555) 123-4567

EDUCATION
State University, Bachelor of Science in Marketing
Expected Graduation: May 2025 | GPA: 3.4

Relevant Coursework: Consumer Behavior, Marketing Research, Digital Marketing 
Fundamentals, Business Statistics, Brand Management

EXPERIENCE

Marketing Intern | Local Nonprofit Organization | Summer 2024
- Managed organization's Instagram and Facebook accounts, growing followers by 25%
- Created weekly social media content including graphics using Canva
- Assisted with email newsletter campaigns using Mailchimp
- Conducted basic analytics reporting on social media performance

Student Marketing Assistant | University Admissions Office | 2023-Present
- Create promotional materials for campus events
- Write copy for student recruitment emails
- Coordinate campus tour social media takeovers

SKILLS
Social Media: Instagram, Facebook, LinkedIn, TikTok
Design: Canva, basic Adobe Photoshop
Tools: Microsoft Office, Google Workspace, Mailchimp
Languages: English (native), Spanish (conversational)

ACTIVITIES
- Marketing Club, Member
- Volunteer, Local Food Bank
```

**Project Narrative (from employer):**
```
We're looking for a student to help us develop and execute a digital marketing 
campaign for our new residential solar panel financing product. GreenTech 
Solutions is a growing renewable energy company, and we're trying to reach 
homeowners who are interested in solar but worried about upfront costs.

The student would start by researching our target customers - we think they're 
probably homeowners aged 35-55 in suburban areas who care about the environment 
but are also practical about finances. We'd love for them to create detailed 
customer personas based on research.

Then they'd develop a campaign strategy - which channels make sense (we're 
thinking social media and maybe some content marketing), what messaging would 
resonate, and how we'd measure success. We want to see an actual content 
calendar they create and ideally have them execute at least part of the 
campaign during their time with us.

We'd also like them to set up some kind of tracking dashboard so we can see 
how things are performing - leads generated, engagement rates, that kind of 
thing. They'll need to learn Google Analytics if they don't know it already.

At the end, we'd want them to present their results to our marketing team 
with recommendations for what we should do next.

Our marketing manager Sarah would meet with them every other week to provide 
guidance and feedback. They'd work independently most of the time but can 
always reach out with questions.
```

### Example Step 2: Extracted & Confirmed Data

**Extracted Learner Skills:**
```json
{
  "technical_skills": [
    {"skill": "Social media management", "evidence": "Managed Instagram and Facebook accounts", "proficiency": "intermediate"},
    {"skill": "Content creation", "evidence": "Created weekly social media content", "proficiency": "intermediate"},
    {"skill": "Canva", "evidence": "Created graphics using Canva", "proficiency": "intermediate"},
    {"skill": "Mailchimp", "evidence": "Assisted with email newsletter campaigns", "proficiency": "beginner"},
    {"skill": "Basic analytics", "evidence": "Conducted basic analytics reporting", "proficiency": "beginner"}
  ],
  "professional_skills": [
    {"skill": "Written communication", "evidence": "Write copy for student recruitment emails"},
    {"skill": "Team collaboration", "evidence": "Multiple team-based roles"}
  ],
  "relevant_coursework": ["Consumer Behavior", "Marketing Research", "Digital Marketing Fundamentals", "Brand Management"],
  "experience_level": "some_experience",
  "potential_growth_areas": ["Advanced analytics", "Campaign strategy", "B2B marketing", "Data visualization"]
}
```

**Extracted Project Requirements:**
```json
{
  "project_summary": "Develop and execute a digital marketing campaign to promote GreenTech Solutions' residential solar financing product, including customer research, campaign strategy, content creation, and performance measurement.",
  "deliverables": [
    {"deliverable": "Customer Persona Documents", "type": "document"},
    {"deliverable": "Campaign Strategy Brief", "type": "document"},
    {"deliverable": "4-Week Social Media Content Calendar", "type": "document"},
    {"deliverable": "Performance Tracking Dashboard", "type": "analysis"},
    {"deliverable": "Final Presentation to Marketing Team", "type": "presentation"}
  ],
  "technical_skills_required": [
    {"skill": "Google Analytics", "importance": "required"},
    {"skill": "Social media advertising", "importance": "helpful"},
    {"skill": "Data visualization", "importance": "required"},
    {"skill": "Content management", "importance": "required"}
  ],
  "professional_skills_required": [
    {"skill": "Customer research", "context": "Developing personas"},
    {"skill": "Strategic thinking", "context": "Campaign planning"},
    {"skill": "Presentation skills", "context": "Final presentation"}
  ],
  "domain_knowledge": [
    {"area": "Renewable energy market", "context": "Understanding product positioning"},
    {"area": "B2C marketing", "context": "Reaching homeowner audience"}
  ]
}
```

**Gap Analysis:**
```json
{
  "strong_matches": [
    {"learner_skill": "Social media management", "project_need": "Content management", "match_quality": "direct"},
    {"learner_skill": "Content creation", "project_need": "Social media content", "match_quality": "direct"},
    {"learner_skill": "Basic analytics", "project_need": "Performance tracking", "match_quality": "transferable"}
  ],
  "skill_gaps": [
    {"project_need": "Google Analytics", "importance": "required", "learning_opportunity": "Technical skill development"},
    {"project_need": "Data visualization/dashboards", "importance": "required", "learning_opportunity": "Expand analytics capabilities"},
    {"project_need": "Campaign strategy", "importance": "critical", "learning_opportunity": "Strategic thinking development"},
    {"project_need": "Customer research methods", "importance": "important", "learning_opportunity": "Apply coursework to practice"}
  ],
  "fit_assessment": {
    "overall_fit": "good",
    "rationale": "Student has strong foundation in social media and content creation. Campaign strategy and analytics represent appropriate stretch goals aligned with career interests.",
    "scaffolding_recommendation": "moderate",
    "key_development_areas": ["Google Analytics proficiency", "Campaign strategy development", "Data-driven decision making"]
  }
}
```

### Example Step 3 Output (Abbreviated)

```markdown
# MKT 495: Experiential Marketing Project
## GreenTech Solutions Customer Acquisition Campaign

**Institution:** State University  
**Credits:** 3 credit hours  
**Duration:** 14 weeks  
**Effort:** Approximately 9 hours per week  

### Course Description

This experiential learning course partners students with GreenTech Solutions, 
a renewable energy company, to develop and execute a customer acquisition 
campaign for their residential solar financing product. Building on existing 
strengths in social media management and content creation, students will 
extend their capabilities into campaign strategy, customer research, and 
data analytics. The project culminates in a presentation of campaign results 
and strategic recommendations to the company's marketing leadership...

---

## Learning Objectives

### Fixed Objectives (Transferable Professional Skills)

Upon successful completion of this course, students will be able to:

1. **Manage project timelines and deliverables** using professional planning 
   tools and techniques (Apply)
2. **Communicate effectively** with workplace stakeholders through written 
   briefs, presentations, and professional correspondence (Apply)
3. **Analyze feedback** from mentors and stakeholders to iterate and improve 
   work products (Analyze)
4. **Evaluate personal growth** through structured reflection on professional 
   skill development (Evaluate)

### Variable Objectives (Project-Specific)

5. **Develop customer personas** using research methods and data analysis 
   to inform marketing strategy (Create) [Addresses gap: Customer research methods]
6. **Design a multi-channel digital marketing campaign** with clear objectives,
   target audience definition, and success metrics (Create) [Addresses gap: Campaign strategy]
7. **Implement Google Analytics tracking** to measure campaign performance 
   and generate actionable insights (Apply) [Addresses gap: Google Analytics proficiency]
8. **Create data visualizations** that communicate campaign results to 
   stakeholders (Apply) [Addresses gap: Data visualization]
9. **Present marketing recommendations** supported by performance data and 
   strategic rationale (Apply)

---

## Weekly Schedule

### Week 1: Orientation & Foundation Setting

#### Concrete Experience
- Virtual onboarding meeting with Sarah (Marketing Manager) and GreenTech team
- Tour GreenTech's current digital presence and review existing marketing materials
- Access setup: Google Analytics, social media accounts, shared drives

#### Reflective Observation
**DEAL Reflection Prompt:**

*Describe:* What did you learn about GreenTech's business model, target market, 
and current marketing approach during onboarding? What specific materials or 
data did you review?

*Examine (Professional Lens):* How does this onboarding experience compare to 
your previous internship at the nonprofit? What aspects of GreenTech's marketing 
operation seem more sophisticated, and where do you see your social media 
experience being directly applicable?

*Articulate Learning:* Identify two specific ways your existing social media 
skills will transfer to this project, and one area where you anticipate needing 
to develop new capabilities. What will you do in Week 2 to start addressing 
that development area?

#### Abstract Conceptualization
- Complete Google Analytics for Beginners certification (free online course)
- Review assigned readings on B2C customer persona development
- Connect persona methodology to Consumer Behavior coursework

#### Active Experimentation
- Draft initial project timeline in Trello/Asana
- Identify 3 questions about GreenTech's target customer to explore in Week 2

#### Deliverables Due
- Reflection Journal Entry #1
- Google Analytics certification screenshot
- Draft project timeline

---

[... Weeks 2-14 continue with similar structure ...]

---

## Assessment Package

### Deliverable Rubric: Customer Persona Documents

| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |
|-----------|---------------|----------------|----------------|---------------|
| **Research Foundation** | Personas are grounded in multiple data sources (analytics, secondary research, stakeholder input); methodology is documented | Personas draw on adequate research; some methodology documentation | Limited research basis; methodology unclear | Personas appear based on assumptions rather than research |
| **Demographic & Psychographic Depth** | Rich detail across demographics, psychographics, behaviors, and pain points; directly relevant to solar financing decision | Adequate detail across most dimensions; generally relevant to product | Some dimensions underdeveloped; connections to product unclear | Superficial or generic; could apply to any product |
| **Actionability** | Clear implications for messaging, channel selection, and content strategy; specific enough to guide campaign decisions | Generally actionable with some specific guidance | Vague implications; limited campaign guidance | No actionable insights |
| **Presentation Quality** | Professional formatting; visual elements enhance comprehension; suitable for stakeholder presentation | Clear formatting; readable and organized | Some formatting issues; adequate but not polished | Poorly organized or formatted |

[... additional rubrics ...]

### Employer Evaluation Form

**GREENTECH SOLUTIONS - STUDENT EVALUATION**

Student Name: Jordan Smith
Project: Customer Acquisition Campaign Development  
Evaluator: _________________  
Evaluation Period: _________________

[... form continues as specified ...]
```

---

## Technical Implementation Notes

### File Structure (Updated for Multi-Step Flow)

```
/adaptive-learning-engine/
├── app.py                   # Main Flask/FastAPI application
├── templates/
│   ├── index.html           # Step 1: Raw intake form
│   ├── confirm.html         # Step 2: Confirmation/edit form
│   └── result.html          # Step 3: Output display
├── static/
│   └── styles.css           # Styling
├── prompts/
│   ├── extraction.py        # Resume and project extraction prompts
│   ├── gap_analysis.py      # Skill gap analysis prompt
│   ├── curriculum.py        # Curriculum generation prompt
│   └── assessment.py        # Assessment generation prompt (if separate)
├── utils/
│   ├── file_parser.py       # Resume PDF/DOCX text extraction
│   ├── input_processor.py   # Input validation and structuring
│   └── output_formatter.py  # Format API response for display
├── requirements.txt
└── README.md
```

### Resume File Parsing

```python
# utils/file_parser.py

import io
from pypdf import PdfReader
from docx import Document as DocxDocument

def extract_text_from_file(file_storage) -> str:
    """Extract text from uploaded PDF or DOCX file."""
    filename = file_storage.filename.lower()
    
    if filename.endswith('.pdf'):
        return extract_from_pdf(file_storage)
    elif filename.endswith('.docx'):
        return extract_from_docx(file_storage)
    else:
        raise ValueError(f"Unsupported file type: {filename}")

def extract_from_pdf(file_storage) -> str:
    """Extract text from PDF file."""
    pdf_reader = PdfReader(io.BytesIO(file_storage.read()))
    text_parts = []
    for page in pdf_reader.pages:
        text_parts.append(page.extract_text())
    return "\n".join(text_parts)

def extract_from_docx(file_storage) -> str:
    """Extract text from DOCX file."""
    doc = DocxDocument(io.BytesIO(file_storage.read()))
    text_parts = []
    for paragraph in doc.paragraphs:
        text_parts.append(paragraph.text)
    return "\n".join(text_parts)
```

### Multi-Step API Flow

```python
# app.py - Core flow

import anthropic
from flask import Flask, request, render_template, session
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for session
client = anthropic.Anthropic()

@app.route('/', methods=['GET'])
def intake_form():
    """Step 1: Display raw intake form."""
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_and_confirm():
    """Step 1 → Step 2: Process inputs and show confirmation."""
    
    # Handle resume
    if 'resume_file' in request.files and request.files['resume_file'].filename:
        resume_text = extract_text_from_file(request.files['resume_file'])
    else:
        resume_text = request.form.get('resume_text', '')
    
    # Collect other raw inputs
    raw_inputs = {
        'learner': {
            'learner_name': request.form.get('learner_name'),
            'academic_level': request.form.get('academic_level'),
            'major_or_program': request.form.get('major_or_program'),
            'resume_text': resume_text,
            'career_goals': request.form.get('career_goals'),
            'skills_to_develop': request.form.get('skills_to_develop'),
            'learning_preferences': request.form.getlist('learning_preferences')
        },
        'project': {
            'company_name': request.form.get('company_name'),
            'industry': request.form.get('industry'),
            'project_title': request.form.get('project_title'),
            'project_narrative': request.form.get('project_narrative'),
            'mentorship_level': request.form.get('mentorship_level'),
            'team_size': request.form.get('team_size')
        },
        'institution': {
            'credit_hours': request.form.get('credit_hours'),
            'term_length_weeks': request.form.get('term_length_weeks'),
            'hours_per_week': request.form.get('hours_per_week'),
            'institution_name': request.form.get('institution_name'),
            'grading_scale': request.form.get('grading_scale'),
            'competency_framework': request.form.getlist('competency_framework')
        }
    }
    
    # Call extraction APIs
    learner_extraction = extract_from_resume(raw_inputs['learner'])
    project_extraction = extract_from_narrative(raw_inputs['project'])
    gap_analysis = analyze_skill_gaps(learner_extraction, project_extraction)
    
    # Store in session for confirmation step
    session['raw_inputs'] = raw_inputs
    session['learner_extraction'] = learner_extraction
    session['project_extraction'] = project_extraction
    session['gap_analysis'] = gap_analysis
    
    return render_template('confirm.html',
        raw=raw_inputs,
        learner=learner_extraction,
        project=project_extraction,
        gaps=gap_analysis
    )

@app.route('/generate', methods=['POST'])
def generate_curriculum():
    """Step 2 → Step 3: Generate curriculum from confirmed data."""
    
    # Get confirmed/edited data from form
    confirmed_data = {
        'learner': {
            'learner_name': request.form.get('learner_name'),
            'academic_level': request.form.get('academic_level'),
            'major_or_program': request.form.get('major_or_program'),
            'confirmed_skills': request.form.getlist('confirmed_skills'),
            'experience_level': request.form.get('experience_level'),
            'confirmed_coursework': request.form.getlist('confirmed_coursework'),
            'career_goals': request.form.get('career_goals'),
            'learning_preferences': request.form.getlist('learning_preferences')
        },
        'project': {
            'company_name': request.form.get('company_name'),
            'industry': request.form.get('industry'),
            'project_title': request.form.get('project_title'),
            'confirmed_summary': request.form.get('confirmed_summary'),
            'confirmed_deliverables': request.form.getlist('confirmed_deliverables'),
            'confirmed_technical_skills': request.form.getlist('confirmed_technical_skills'),
            'confirmed_professional_skills': request.form.getlist('confirmed_professional_skills'),
            'confirmed_domain_knowledge': request.form.getlist('confirmed_domain_knowledge'),
            'confirmed_success_criteria': request.form.getlist('confirmed_success_criteria'),
            'mentorship_level': request.form.get('mentorship_level'),
            'team_size': request.form.get('team_size')
        },
        'gaps': {
            'strong_matches': request.form.getlist('strong_matches'),
            'skill_gaps': request.form.getlist('skill_gaps'),
            'scaffolding_recommendation': request.form.get('scaffolding_recommendation'),
            'overall_fit': request.form.get('overall_fit')
        },
        'institution': session['raw_inputs']['institution']
    }
    
    # Generate curriculum
    curriculum = generate_curriculum_from_confirmed(confirmed_data)
    
    return render_template('result.html', curriculum=curriculum, data=confirmed_data)

def extract_from_resume(learner_data: dict) -> dict:
    """Call Claude to extract structured data from resume."""
    prompt = build_resume_extraction_prompt(learner_data)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse JSON from response
    response_text = message.content[0].text
    # Extract JSON from response (may be wrapped in markdown code blocks)
    json_str = extract_json_from_response(response_text)
    return json.loads(json_str)

def extract_from_narrative(project_data: dict) -> dict:
    """Call Claude to extract structured data from project narrative."""
    prompt = build_project_extraction_prompt(project_data)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text
    json_str = extract_json_from_response(response_text)
    return json.loads(json_str)

def analyze_skill_gaps(learner: dict, project: dict) -> dict:
    """Call Claude to analyze skill gaps between learner and project."""
    prompt = build_gap_analysis_prompt(learner, project)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )
    
    response_text = message.content[0].text
    json_str = extract_json_from_response(response_text)
    return json.loads(json_str)

def generate_curriculum_from_confirmed(data: dict) -> str:
    """Call Claude to generate full curriculum from confirmed data."""
    prompt = build_curriculum_prompt(data)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,  # Course shells are long
        messages=[{"role": "user", "content": prompt}]
    )
    
    return message.content[0].text

def extract_json_from_response(text: str) -> str:
    """Extract JSON from a response that may have markdown formatting."""
    # Handle ```json ... ``` blocks
    if '```json' in text:
        start = text.find('```json') + 7
        end = text.find('```', start)
        return text[start:end].strip()
    elif '```' in text:
        start = text.find('```') + 3
        end = text.find('```', start)
        return text[start:end].strip()
    return text.strip()
```

### Error Handling

```python
# Wrap API calls with retry logic

import time
from anthropic import APIError, RateLimitError

def call_with_retry(func, max_retries=3):
    """Call function with exponential backoff retry."""
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 1  # 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise
        except APIError as e:
            if attempt < max_retries - 1 and e.status_code >= 500:
                wait_time = (2 ** attempt) * 1
                time.sleep(wait_time)
            else:
                raise
```

### Environment Variables

```
ANTHROPIC_API_KEY=your_key_here
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

### Dependencies (requirements.txt)

```
flask>=2.0.0
anthropic>=0.18.0
python-dotenv>=1.0.0
markdown>=3.4.0
pypdf>=3.0.0
python-docx>=0.8.11
```

---

## Success Criteria

The prototype is successful if:

1. **Functional:** 
   - Accepts resume upload (PDF/DOCX) and extracts text correctly
   - Parses project narrative and extracts structured data
   - Generates skill gap analysis with reasonable accuracy
   - Produces complete course shell without errors
   
2. **User Experience:**
   - A learner can upload their resume instead of manually tagging skills
   - An employer can write a narrative instead of filling out detailed forms
   - Users can easily review, edit, and confirm extracted data
   - The confirmation step feels helpful, not burdensome
   
3. **Pedagogically Sound:** 
   - Output demonstrably reflects Kolb's cycle (all four phases per week)
   - Reflection prompts follow DEAL model structure
   - Learning objectives use Bloom's taxonomy with cognitive levels noted
   - Skill gaps translate into specific learning objectives
   
4. **Professional Quality:** 
   - Output looks like a real course syllabus
   - Could be shared with university stakeholders without embarrassment
   - Rubrics are specific and useful, not generic
   
5. **Reasonable Performance:** 
   - Extraction step completes in under 30 seconds
   - Curriculum generation completes in under 90 seconds
   - Total flow (including user review) under 5 minutes
   
6. **Usable:** 
   - A non-technical user (Bruce) can complete the flow without help
   - Error messages are clear and actionable
   - The prototype works on modern browsers (Chrome, Firefox, Safari)

---

## Future Enhancements (Out of Scope for Prototype)

- PDF export with professional formatting
- Save/load previous generations
- Multiple curriculum variants for A/B comparison
- Direct LMS export (Canvas, Blackboard)
- Batch generation for multiple students
- Feedback loop to improve generation quality
- Integration with Riipen's employer/project database
