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
    CLAUDE_MODEL = os.getenv('CLAUDE_MODEL', 'claude-sonnet-4-5-20241022')

    # API call settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds

    # Token limits
    EXTRACTION_MAX_TOKENS = 2000
    GAP_ANALYSIS_MAX_TOKENS = 1500
    CURRICULUM_MAX_TOKENS = 8000

    # File upload settings
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx'}

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
        return True
