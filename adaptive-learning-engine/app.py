"""
Adaptive Learning Design Engine - Main Flask Application

A prototype that demonstrates AI-powered curriculum generation for experiential learning.
"""

import os
import sys

# Ensure the app directory is in the path for imports
app_dir = os.path.dirname(os.path.abspath(__file__))
if app_dir not in sys.path:
    sys.path.insert(0, app_dir)

from flask import Flask, render_template, request, session, redirect, url_for, Response, flash
import json

from config import Config
from utils import extract_text_from_file, ClaudeClient, markdown_to_html, prepare_download
from prompts import (
    build_resume_extraction_prompt,
    build_project_extraction_prompt,
    build_gap_analysis_prompt,
    build_curriculum_prompt
)

# Initialize Flask with explicit template and static paths
app = Flask(__name__,
            template_folder=os.path.join(app_dir, 'templates'),
            static_folder=os.path.join(app_dir, 'static'))
app.config.from_object(Config)
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# Initialize Claude client
claude_client = None


def get_claude_client():
    """Get or initialize Claude client."""
    global claude_client
    if claude_client is None:
        Config.validate()
        claude_client = ClaudeClient()
    return claude_client


def safe_json_loads(value: str, default=None):
    """Safely parse JSON, returning default on failure."""
    if default is None:
        default = []
    if not value or value.strip() == '':
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default


def merge_user_project_inputs(ai_extraction: dict, user_inputs: dict) -> dict:
    """
    Merge user-provided optional fields with AI extraction results.
    User input takes priority when provided.
    """
    result = ai_extraction.copy() if ai_extraction else {}

    # Merge deliverables - user input takes priority if provided
    user_deliverables = user_inputs.get('expected_deliverables', '').strip()
    if user_deliverables:
        user_list = [d.strip() for d in user_deliverables.split(',') if d.strip()]
        # Convert to expected format
        result['deliverables'] = [{'deliverable': d, 'description': '', 'type': 'other'} for d in user_list]

    # Merge required skills - user input takes priority if provided
    user_skills = user_inputs.get('required_skills', '').strip()
    if user_skills:
        user_list = [s.strip() for s in user_skills.split(',') if s.strip()]
        result['technical_skills_required'] = [{'skill': s, 'importance': 'required', 'context': ''} for s in user_list]

    # Merge success criteria - user input takes priority if provided
    user_criteria = user_inputs.get('success_criteria_input', '').strip()
    if user_criteria:
        result['success_criteria'] = [c.strip() for c in user_criteria.split(',') if c.strip()]

    return result


@app.route('/', methods=['GET'])
def intake_form():
    """Step 1: Display raw intake form."""
    return render_template('index.html')


@app.route('/extract', methods=['POST'])
def extract_and_confirm():
    """Step 1 → Step 2: Process inputs and show confirmation."""
    try:
        # Handle resume - file upload or text paste
        resume_text = ''
        if 'resume_file' in request.files:
            file = request.files['resume_file']
            if file and file.filename:
                resume_text = extract_text_from_file(file)

        if not resume_text:
            resume_text = request.form.get('resume_text', '')

        if not resume_text.strip():
            flash('Please upload a resume file or paste resume text.', 'error')
            return redirect(url_for('intake_form'))

        # Collect raw inputs
        raw_inputs = {
            'learner': {
                'learner_name': request.form.get('learner_name', ''),
                'academic_level': request.form.get('academic_level', ''),
                'major_or_program': request.form.get('major_or_program', ''),
                'resume_text': resume_text,
                'career_goals': request.form.get('career_goals', ''),
                'skills_to_develop': request.form.get('skills_to_develop', ''),
                'learning_preferences': request.form.getlist('learning_preferences')
            },
            'project': {
                'company_name': request.form.get('company_name', ''),
                'industry': request.form.get('industry', ''),
                'project_title': request.form.get('project_title', ''),
                'project_narrative': request.form.get('project_narrative', ''),
                'mentorship_level': request.form.get('mentorship_level', ''),
                'team_size': request.form.get('team_size', ''),
                # Optional advanced fields
                'expected_deliverables': request.form.get('expected_deliverables', ''),
                'required_skills': request.form.get('required_skills', ''),
                'success_criteria_input': request.form.get('success_criteria_input', '')
            },
            'institution': {
                'credit_hours': request.form.get('credit_hours', '3'),
                'term_length_weeks': request.form.get('term_length_weeks', '14'),
                'hours_per_week': request.form.get('hours_per_week', '9'),
                'institution_name': request.form.get('institution_name', ''),
                'grading_scale': request.form.get('grading_scale', 'Letter Grade (A-F)'),
                'competency_framework': request.form.getlist('competency_framework'),
                'fixed_objectives': request.form.getlist('fixed_objectives') or [
                    'project_management', 'professional_communication', 'time_management',
                    'critical_thinking', 'collaboration', 'self_reflection'
                ]
            }
        }

        # Handle project file upload or text
        project_narrative = ''
        if 'project_file' in request.files:
            project_file = request.files['project_file']
            if project_file and project_file.filename:
                project_narrative = extract_text_from_file(project_file)

        if not project_narrative:
            project_narrative = request.form.get('project_narrative', '')

        raw_inputs['project']['project_narrative'] = project_narrative

        # Validate required fields
        if not project_narrative.strip():
            flash('Please upload a project document or provide a project description.', 'error')
            return redirect(url_for('intake_form'))

        # Get Claude client and call extraction APIs
        client = get_claude_client()

        learner_extraction = client.extract_from_resume(raw_inputs['learner'])
        project_extraction = client.extract_from_narrative(raw_inputs['project'])

        # Merge user-provided optional fields with AI extraction
        project_extraction = merge_user_project_inputs(project_extraction, raw_inputs['project'])

        gap_analysis = client.analyze_gaps(learner_extraction, project_extraction)

        # Store in session
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

    except ValueError as e:
        flash(f'Configuration error: {str(e)}', 'error')
        return redirect(url_for('intake_form'))
    except Exception as e:
        flash(f'Error processing inputs: {str(e)}', 'error')
        return redirect(url_for('intake_form'))


@app.route('/generate', methods=['POST'])
def generate_curriculum():
    """Step 2 → Step 3: Redirect to incremental builder."""
    try:
        # Build confirmed data from form submission (using safe JSON parsing)
        confirmed_data = {
            'learner': {
                'learner_name': request.form.get('learner_name', ''),
                'academic_level': request.form.get('academic_level', ''),
                'major_or_program': request.form.get('major_or_program', ''),
                'confirmed_skills': safe_json_loads(request.form.get('confirmed_skills', '[]')),
                'experience_level': request.form.get('experience_level', ''),
                'confirmed_coursework': safe_json_loads(request.form.get('confirmed_coursework', '[]')),
                'career_goals': request.form.get('career_goals', ''),
                'learning_preferences': safe_json_loads(request.form.get('learning_preferences', '[]'))
            },
            'project': {
                'company_name': request.form.get('company_name', ''),
                'industry': request.form.get('industry', ''),
                'project_title': request.form.get('project_title', ''),
                'confirmed_summary': request.form.get('confirmed_summary', ''),
                'confirmed_deliverables': safe_json_loads(request.form.get('confirmed_deliverables', '[]')),
                'confirmed_technical_skills': safe_json_loads(request.form.get('confirmed_technical_skills', '[]')),
                'confirmed_professional_skills': safe_json_loads(request.form.get('confirmed_professional_skills', '[]')),
                'confirmed_domain_knowledge': safe_json_loads(request.form.get('confirmed_domain_knowledge', '[]')),
                'confirmed_success_criteria': safe_json_loads(request.form.get('confirmed_success_criteria', '[]')),
                'mentorship_level': request.form.get('mentorship_level', ''),
                'team_size': request.form.get('team_size', '')
            },
            'gaps': {
                'strong_matches': safe_json_loads(request.form.get('strong_matches', '[]')),
                'skill_gaps': safe_json_loads(request.form.get('skill_gaps', '[]')),
                'scaffolding_recommendation': request.form.get('scaffolding_recommendation', 'moderate'),
                'overall_fit': request.form.get('overall_fit', 'good')
            },
            'institution': {
                **session.get('raw_inputs', {}).get('institution', {
                    'credit_hours': '3',
                    'term_length_weeks': '14',
                    'hours_per_week': '9',
                    'institution_name': '',
                    'grading_scale': 'Letter Grade (A-F)',
                    'competency_framework': []
                }),
                # Override with form submission to capture user's final selection
                'fixed_objectives': request.form.getlist('fixed_objectives') or [
                    'project_management', 'professional_communication', 'time_management',
                    'critical_thinking', 'collaboration', 'self_reflection'
                ]
            }
        }

        # Store confirmed data and initialize build state
        session['confirmed_data'] = confirmed_data
        session['build_state'] = {
            'current_step': 1,
            'objectives': None,
            'assessment_strategy': None,
            'outline': None,
            'week_details': {}
        }
        session.modified = True

        # Redirect to incremental builder
        return redirect(url_for('build_curriculum_page'))

    except Exception as e:
        flash(f'Error processing data: {str(e)}', 'error')
        return redirect(url_for('intake_form'))


@app.route('/download', methods=['GET'])
def download_curriculum():
    """Download generated curriculum as markdown file."""
    curriculum = session.get('curriculum', '')
    if not curriculum:
        flash('No curriculum to download. Please generate one first.', 'error')
        return redirect(url_for('intake_form'))

    data = session.get('confirmed_data', {})
    filename = prepare_download(data)

    return Response(
        curriculum,
        mimetype='text/markdown',
        headers={'Content-Disposition': f'attachment;filename={filename}'}
    )


@app.route('/back-to-confirm', methods=['GET'])
def back_to_confirm():
    """Return to confirmation page with preserved data."""
    raw = session.get('raw_inputs')
    learner = session.get('learner_extraction')
    project = session.get('project_extraction')
    gaps = session.get('gap_analysis')

    if not all([raw, learner, project, gaps]):
        flash('Session expired. Please start over.', 'error')
        return redirect(url_for('intake_form'))

    return render_template('confirm.html',
        raw=raw,
        learner=learner,
        project=project,
        gaps=gaps
    )


# --- Incremental Course Builder Routes ---

@app.route('/build', methods=['GET'])
def build_curriculum_page():
    """Display the incremental course builder page."""
    confirmed_data = session.get('confirmed_data')
    if not confirmed_data:
        flash('Please complete the confirmation step first.', 'error')
        return redirect(url_for('intake_form'))

    # Initialize build state if not present
    if 'build_state' not in session:
        session['build_state'] = {
            'current_step': 1,
            'objectives': None,
            'assessment_strategy': None,
            'outline': None,
            'week_details': {}
        }

    return render_template('build.html',
        data=confirmed_data,
        build_state=session.get('build_state', {})
    )


@app.route('/api/generate-objectives', methods=['POST'])
def api_generate_objectives():
    """Step 1 API: Generate learning objectives and assessment strategy."""
    try:
        confirmed_data = session.get('confirmed_data')
        if not confirmed_data:
            return json.dumps({'error': 'No confirmed data in session'}), 400

        client = get_claude_client()
        result = client.generate_objectives_and_assessment(confirmed_data)

        # Store in build state
        if 'build_state' not in session:
            session['build_state'] = {}
        session['build_state']['objectives'] = {
            'fixed_objectives': result.get('fixed_objectives', []),
            'variable_objectives': result.get('variable_objectives', [])
        }
        session['build_state']['assessment_strategy'] = result.get('assessment_strategy', {})
        session.modified = True

        return json.dumps({
            'status': 'success',
            'objectives': session['build_state']['objectives'],
            'assessment_strategy': session['build_state']['assessment_strategy']
        })

    except Exception as e:
        return json.dumps({'error': str(e)}), 500


@app.route('/api/generate-outline', methods=['POST'])
def api_generate_outline():
    """Step 2 API: Generate course outline."""
    try:
        confirmed_data = session.get('confirmed_data')
        build_state = session.get('build_state', {})
        objectives = build_state.get('objectives')

        if not confirmed_data:
            return json.dumps({'error': 'No confirmed data in session'}), 400
        if not objectives:
            return json.dumps({'error': 'Objectives not generated yet'}), 400

        client = get_claude_client()
        result = client.generate_course_outline(confirmed_data, objectives)

        # Store in build state
        session['build_state']['outline'] = result
        session['build_state']['current_step'] = 2
        session.modified = True

        return json.dumps({
            'status': 'success',
            'outline': result
        })

    except Exception as e:
        return json.dumps({'error': str(e)}), 500


@app.route('/api/generate-week/<int:week>', methods=['POST'])
def api_generate_week(week):
    """Step 3 API: Generate detailed content for a single week."""
    try:
        confirmed_data = session.get('confirmed_data')
        build_state = session.get('build_state', {})
        objectives = build_state.get('objectives')
        outline = build_state.get('outline')

        if not confirmed_data:
            return json.dumps({'error': 'No confirmed data in session'}), 400
        if not objectives:
            return json.dumps({'error': 'Objectives not generated yet'}), 400
        if not outline:
            return json.dumps({'error': 'Outline not generated yet'}), 400

        # Validate week number
        term_length = int(confirmed_data.get('institution', {}).get('term_length_weeks', 14))
        if week < 1 or week > term_length:
            return json.dumps({'error': f'Week must be between 1 and {term_length}'}), 400

        client = get_claude_client()
        content = client.generate_week_detail(confirmed_data, objectives, outline, week)

        # Store in build state
        if 'week_details' not in session['build_state']:
            session['build_state']['week_details'] = {}
        session['build_state']['week_details'][str(week)] = content
        session['build_state']['current_step'] = 3
        session.modified = True

        return json.dumps({
            'status': 'success',
            'week': week,
            'content': content,
            'html': markdown_to_html(content)
        })

    except Exception as e:
        return json.dumps({'error': str(e)}), 500


@app.route('/api/regenerate-week/<int:week>', methods=['POST'])
def api_regenerate_week(week):
    """Regenerate a specific week with optional user feedback."""
    try:
        confirmed_data = session.get('confirmed_data')
        build_state = session.get('build_state', {})
        objectives = build_state.get('objectives')
        outline = build_state.get('outline')

        if not confirmed_data:
            return json.dumps({'error': 'No confirmed data in session'}), 400
        if not objectives:
            return json.dumps({'error': 'Objectives not generated yet'}), 400
        if not outline:
            return json.dumps({'error': 'Outline not generated yet'}), 400

        # Get feedback from request
        data = request.get_json() or {}
        feedback = data.get('feedback', '')

        # Validate week number
        term_length = int(confirmed_data.get('institution', {}).get('term_length_weeks', 14))
        if week < 1 or week > term_length:
            return json.dumps({'error': f'Week must be between 1 and {term_length}'}), 400

        client = get_claude_client()
        content = client.regenerate_week(confirmed_data, objectives, outline, week, feedback)

        # Update in build state
        session['build_state']['week_details'][str(week)] = content
        session.modified = True

        return json.dumps({
            'status': 'success',
            'week': week,
            'content': content,
            'html': markdown_to_html(content)
        })

    except Exception as e:
        return json.dumps({'error': str(e)}), 500


@app.route('/api/save-step', methods=['POST'])
def api_save_step():
    """Save user edits for the current step."""
    try:
        data = request.get_json() or {}
        step = data.get('step')
        content = data.get('content')

        if not step:
            return json.dumps({'error': 'Step not specified'}), 400

        build_state = session.get('build_state', {})

        if step == 'objectives':
            build_state['objectives'] = content.get('objectives', {})
            build_state['assessment_strategy'] = content.get('assessment_strategy', {})
        elif step == 'outline':
            build_state['outline'] = content
        elif step.startswith('week_'):
            week_num = step.replace('week_', '')
            if 'week_details' not in build_state:
                build_state['week_details'] = {}
            build_state['week_details'][week_num] = content

        session['build_state'] = build_state
        session.modified = True

        return json.dumps({'status': 'success'})

    except Exception as e:
        return json.dumps({'error': str(e)}), 500


@app.route('/finalize', methods=['POST'])
def finalize_curriculum():
    """Combine all generated sections into final curriculum."""
    try:
        confirmed_data = session.get('confirmed_data')
        build_state = session.get('build_state', {})

        if not confirmed_data:
            flash('Session expired. Please start over.', 'error')
            return redirect(url_for('intake_form'))

        objectives = build_state.get('objectives', {})
        assessment = build_state.get('assessment_strategy', {})
        outline = build_state.get('outline', {})
        week_details = build_state.get('week_details', {})

        # Build the final curriculum markdown
        curriculum_parts = []

        # Course header
        header = outline.get('course_header', {})
        curriculum_parts.append(f"# {header.get('title', 'Experiential Learning Course')}")
        curriculum_parts.append(f"\n**Credits:** {header.get('credits', '3')}")
        curriculum_parts.append(f"\n## Course Description\n{header.get('description', '')}")

        # Grading breakdown
        grading = assessment.get('grading_breakdown', {})
        if grading:
            curriculum_parts.append("\n## Grading Breakdown")
            for key, value in grading.items():
                if isinstance(value, dict):
                    curriculum_parts.append(f"- **{key.replace('_', ' ').title()}**: {value.get('weight', 0)}% - {value.get('description', '')}")
                else:
                    curriculum_parts.append(f"- **{key.replace('_', ' ').title()}**: {value}")

        # Learning objectives
        curriculum_parts.append("\n## Learning Objectives")
        curriculum_parts.append("\n### Professional Skills Objectives")
        for obj in objectives.get('fixed_objectives', []):
            text = obj.get('text', obj) if isinstance(obj, dict) else obj
            curriculum_parts.append(f"- {text}")

        curriculum_parts.append("\n### Project-Specific Objectives")
        for obj in objectives.get('variable_objectives', []):
            text = obj.get('text', obj) if isinstance(obj, dict) else obj
            bloom = obj.get('bloom_level', '') if isinstance(obj, dict) else ''
            bloom_str = f" ({bloom})" if bloom else ""
            curriculum_parts.append(f"- {text}{bloom_str}")

        # Weekly schedule
        curriculum_parts.append("\n## Weekly Schedule")
        term_length = int(confirmed_data.get('institution', {}).get('term_length_weeks', 14))
        for week_num in range(1, term_length + 1):
            week_content = week_details.get(str(week_num), '')
            if week_content:
                curriculum_parts.append(f"\n{week_content}")
            else:
                # Fall back to outline if detailed content not generated
                weeks = outline.get('weeks', [])
                week_info = next((w for w in weeks if w.get('week') == week_num), {})
                theme = week_info.get('theme', f'Week {week_num}')
                curriculum_parts.append(f"\n### Week {week_num}: {theme}")
                curriculum_parts.append("*(Detailed content not yet generated)*")

        # Assessment rubrics
        curriculum_parts.append("\n## Assessment Package")

        # Deliverable rubric
        deliverable_criteria = assessment.get('deliverable_rubric_criteria', [])
        if deliverable_criteria:
            curriculum_parts.append("\n### Deliverable Rubric")
            curriculum_parts.append("| Criterion | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |")
            curriculum_parts.append("|-----------|--------------|----------------|----------------|---------------|")
            for crit in deliverable_criteria:
                name = crit.get('criterion', 'Criterion')
                curriculum_parts.append(f"| {name} | Exceeds expectations | Meets expectations | Approaching expectations | Below expectations |")

        # Reflection rubric
        reflection_criteria = assessment.get('reflection_rubric_criteria', [])
        if reflection_criteria:
            curriculum_parts.append("\n### Reflection Quality Rubric (DEAL Model)")
            curriculum_parts.append("| Dimension | Excellent (4) | Proficient (3) | Developing (2) | Beginning (1) |")
            curriculum_parts.append("|-----------|--------------|----------------|----------------|---------------|")
            for crit in reflection_criteria:
                name = crit.get('criterion', 'Criterion')
                curriculum_parts.append(f"| {name} | Exceeds expectations | Meets expectations | Approaching expectations | Below expectations |")

        # Employer evaluation dimensions
        employer_dims = assessment.get('employer_evaluation_dimensions', [])
        if employer_dims:
            curriculum_parts.append("\n### Employer Evaluation Form")
            curriculum_parts.append("Please rate the student on the following dimensions (1-5 scale):")
            for dim in employer_dims:
                name = dim.get('dimension', 'Dimension')
                desc = dim.get('description', '')
                curriculum_parts.append(f"- **{name}**: {desc}")

        # Combine all parts
        curriculum_markdown = "\n".join(curriculum_parts)

        # Store for download
        session['curriculum'] = curriculum_markdown
        session.modified = True

        # Convert to HTML for display
        curriculum_html = markdown_to_html(curriculum_markdown)

        return render_template('result.html',
            curriculum_html=curriculum_html,
            curriculum_markdown=curriculum_markdown,
            data=confirmed_data
        )

    except Exception as e:
        flash(f'Error finalizing curriculum: {str(e)}', 'error')
        return redirect(url_for('build_curriculum_page'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
