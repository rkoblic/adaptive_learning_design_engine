"""
Adaptive Learning Design Engine - Main Flask Application

A prototype that demonstrates AI-powered curriculum generation for experiential learning.
"""

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

app = Flask(__name__)
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
                'team_size': request.form.get('team_size', '')
            },
            'institution': {
                'credit_hours': request.form.get('credit_hours', '3'),
                'term_length_weeks': request.form.get('term_length_weeks', '14'),
                'hours_per_week': request.form.get('hours_per_week', '9'),
                'institution_name': request.form.get('institution_name', ''),
                'grading_scale': request.form.get('grading_scale', 'Letter Grade (A-F)'),
                'competency_framework': request.form.getlist('competency_framework')
            }
        }

        # Validate required fields
        if not raw_inputs['project']['project_narrative'].strip():
            flash('Please provide a project narrative.', 'error')
            return redirect(url_for('intake_form'))

        # Get Claude client and call extraction APIs
        client = get_claude_client()

        learner_extraction = client.extract_from_resume(raw_inputs['learner'])
        project_extraction = client.extract_from_narrative(raw_inputs['project'])
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
    """Step 2 → Step 3: Generate curriculum from confirmed data."""
    try:
        # Build confirmed data from form submission
        confirmed_data = {
            'learner': {
                'learner_name': request.form.get('learner_name', ''),
                'academic_level': request.form.get('academic_level', ''),
                'major_or_program': request.form.get('major_or_program', ''),
                'confirmed_skills': json.loads(request.form.get('confirmed_skills', '[]')),
                'experience_level': request.form.get('experience_level', ''),
                'confirmed_coursework': json.loads(request.form.get('confirmed_coursework', '[]')),
                'career_goals': request.form.get('career_goals', ''),
                'learning_preferences': json.loads(request.form.get('learning_preferences', '[]'))
            },
            'project': {
                'company_name': request.form.get('company_name', ''),
                'industry': request.form.get('industry', ''),
                'project_title': request.form.get('project_title', ''),
                'confirmed_summary': request.form.get('confirmed_summary', ''),
                'confirmed_deliverables': json.loads(request.form.get('confirmed_deliverables', '[]')),
                'confirmed_technical_skills': json.loads(request.form.get('confirmed_technical_skills', '[]')),
                'confirmed_professional_skills': json.loads(request.form.get('confirmed_professional_skills', '[]')),
                'confirmed_domain_knowledge': json.loads(request.form.get('confirmed_domain_knowledge', '[]')),
                'confirmed_success_criteria': json.loads(request.form.get('confirmed_success_criteria', '[]')),
                'mentorship_level': request.form.get('mentorship_level', ''),
                'team_size': request.form.get('team_size', '')
            },
            'gaps': {
                'strong_matches': json.loads(request.form.get('strong_matches', '[]')),
                'skill_gaps': json.loads(request.form.get('skill_gaps', '[]')),
                'scaffolding_recommendation': request.form.get('scaffolding_recommendation', 'moderate'),
                'overall_fit': request.form.get('overall_fit', 'good')
            },
            'institution': session.get('raw_inputs', {}).get('institution', {
                'credit_hours': '3',
                'term_length_weeks': '14',
                'hours_per_week': '9',
                'institution_name': '',
                'grading_scale': 'Letter Grade (A-F)',
                'competency_framework': []
            })
        }

        # Generate curriculum
        client = get_claude_client()
        curriculum_markdown = client.generate_curriculum(confirmed_data)

        # Store for download
        session['curriculum'] = curriculum_markdown
        session['confirmed_data'] = confirmed_data

        # Convert to HTML for display
        curriculum_html = markdown_to_html(curriculum_markdown)

        return render_template('result.html',
            curriculum_html=curriculum_html,
            curriculum_markdown=curriculum_markdown,
            data=confirmed_data
        )

    except Exception as e:
        flash(f'Error generating curriculum: {str(e)}', 'error')
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
