"""Configuration management for the Adaptive Learning Design Engine."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # Flask settings
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

    # Anthropic API settings
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20250929')

    # API call settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    # Token limits
    EXTRACTION_MAX_TOKENS = 2000
    GAP_ANALYSIS_MAX_TOKENS = 3000  # Increased for Bloom's taxonomy learning objectives
    CURRICULUM_MAX_TOKENS = 8000  # Legacy: monolithic curriculum generation

    # Modular curriculum generation token limits
    OBJECTIVES_ASSESSMENT_MAX_TOKENS = 2000  # Step 1: Objectives + assessment strategy
    COURSE_OUTLINE_MAX_TOKENS = 2000         # Step 2: High-level syllabus outline
    WEEK_DETAIL_MAX_TOKENS = 800             # Step 3: Detailed week content (per week)

    # File upload settings
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return True
