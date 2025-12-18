"""Output formatting utilities for display and download."""

import markdown
import re


def markdown_to_html(md_content: str) -> str:
    """
    Convert markdown content to HTML for display.

    Args:
        md_content: Markdown string

    Returns:
        HTML string with proper formatting
    """
    # Configure markdown extensions for tables and code blocks
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br'
    ]

    md = markdown.Markdown(extensions=extensions)
    html = md.convert(md_content)

    return html


def prepare_download(data: dict) -> str:
    """
    Prepare filename for curriculum download.

    Args:
        data: Confirmed data dict with project and learner info

    Returns:
        Sanitized filename string
    """
    # Build filename from project and learner data
    project_title = data.get('project', {}).get('project_title', 'course')
    learner_name = data.get('learner', {}).get('learner_name', '')

    # Sanitize for filename
    project_title = sanitize_filename(project_title)
    learner_name = sanitize_filename(learner_name)

    if learner_name:
        filename = f"{project_title}_{learner_name}_curriculum.md"
    else:
        filename = f"{project_title}_curriculum.md"

    return filename


def sanitize_filename(text: str) -> str:
    """
    Sanitize text for use in filename.

    Args:
        text: Raw text string

    Returns:
        Sanitized string safe for filenames
    """
    # Remove or replace invalid characters
    text = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace spaces and multiple underscores
    text = re.sub(r'\s+', '_', text)
    text = re.sub(r'_+', '_', text)
    # Limit length
    text = text[:50].strip('_')
    return text or 'course'


def extract_toc_from_curriculum(md_content: str) -> list:
    """
    Extract table of contents from curriculum markdown.

    Args:
        md_content: Markdown string

    Returns:
        List of dicts with 'level', 'title', 'anchor' keys
    """
    toc = []
    lines = md_content.split('\n')

    for line in lines:
        # Match markdown headers
        match = re.match(r'^(#{1,3})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            # Create anchor from title
            anchor = re.sub(r'[^a-z0-9\s-]', '', title.lower())
            anchor = re.sub(r'\s+', '-', anchor)

            toc.append({
                'level': level,
                'title': title,
                'anchor': anchor
            })

    return toc
