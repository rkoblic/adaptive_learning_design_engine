# Adaptive Learning Design Engine

An AI-powered curriculum generation prototype that transforms workplace projects into structured educational experiences. Built for Riipen's business development conversations with university partners.

## Features

- **Resume Parsing**: Upload PDF/DOCX resumes or paste text directly
- **AI-Powered Extraction**: Automatically extracts skills, experience, and coursework from resumes
- **Project Analysis**: Parses project narratives to identify deliverables and requirements
- **Skill Gap Analysis**: Compares learner capabilities to project needs
- **Curriculum Generation**: Creates complete course shells with:
  - Learning objectives (Bloom's Taxonomy)
  - Weekly schedule (Kolb's Experiential Learning Cycle)
  - Reflection prompts (DEAL Model)
  - Assessment rubrics
  - Employer evaluation forms
  - Student self-assessments

## Learning Science Frameworks

The system embeds established learning science principles:

- **Kolb's Experiential Learning Cycle**: Every week includes Concrete Experience, Reflective Observation, Abstract Conceptualization, and Active Experimentation
- **DEAL Reflection Model**: Describe, Examine, Articulate Learning
- **Bloom's Taxonomy**: Learning objectives use appropriate action verbs with cognitive levels
- **Zone of Proximal Development**: Scaffolding adjusts based on learner-project fit

## Quick Start

### Prerequisites

- Python 3.9+
- Anthropic API key

### Installation

1. Clone or download this repository:
   ```bash
   cd adaptive-learning-engine
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   FLASK_SECRET_KEY=your-random-secret-key
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser to `http://localhost:5000`

## Usage

### Step 1: Input Details

1. **Learner Profile**: Upload a resume (PDF/DOCX) or paste resume text
2. **Project Details**: Describe the project, including deliverables and success criteria
3. **Institutional Constraints**: Set credit hours, term length, and grading scale

### Step 2: Review & Confirm

1. Review AI-extracted skills and deliverables
2. Edit, add, or remove items as needed
3. Confirm the skill gap analysis
4. Click "Generate Course Shell"

### Step 3: Generated Course

1. View the complete curriculum document
2. Download as Markdown
3. Copy to clipboard
4. Start over or edit inputs

## Project Structure

```
adaptive-learning-engine/
├── app.py                   # Main Flask application
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Step 1: Input form
│   ├── confirm.html         # Step 2: Confirmation
│   └── result.html          # Step 3: Output display
├── static/
│   └── styles.css           # Custom styles
├── prompts/
│   ├── __init__.py
│   ├── extraction.py        # Resume/project extraction prompts
│   ├── gap_analysis.py      # Skill gap analysis prompt
│   └── curriculum.py        # Curriculum generation prompt
└── utils/
    ├── __init__.py
    ├── file_parser.py       # PDF/DOCX text extraction
    ├── api_client.py        # Claude API wrapper
    └── output_formatter.py  # Output formatting utilities
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Required |
| `FLASK_SECRET_KEY` | Flask session secret | `dev-secret-key` |
| `CLAUDE_MODEL` | Claude model to use | `claude-sonnet-4-20250514` |

## API Usage

The application makes the following Claude API calls:

1. **Resume Extraction** (~15s): Extracts skills, experience, coursework
2. **Project Extraction** (~15s): Extracts deliverables, requirements
3. **Gap Analysis** (~10s): Compares learner to project needs
4. **Curriculum Generation** (~60-90s): Generates full course shell

Total time for complete flow: ~2-3 minutes

## Customization

### Modifying Prompts

Edit files in the `prompts/` directory to customize:

- `extraction.py`: Change how skills and deliverables are extracted
- `gap_analysis.py`: Adjust fit assessment criteria
- `curriculum.py`: Modify course shell structure and content

### Styling

- Edit `static/styles.css` for custom styles
- Templates use Tailwind CSS via CDN for rapid styling

## Troubleshooting

### Common Issues

**"ANTHROPIC_API_KEY environment variable is required"**
- Ensure `.env` file exists with your API key
- Restart the Flask server after adding the key

**Resume upload fails**
- Check file is PDF or DOCX format
- Ensure file is under 10MB
- Try pasting resume text directly instead

**Generation takes too long**
- Claude API calls can take 60-90 seconds for curriculum generation
- This is normal for comprehensive output

## License

Prototype for demonstration purposes.

## Support

For issues or questions, please contact the development team.
