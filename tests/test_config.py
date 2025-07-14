"""
Test configuration utilities for handling environment variables and API keys.
"""

import os
import pytest
from pathlib import Path
from dotenv import load_dotenv


def load_test_env():
    """Load environment variables from .env file for testing."""
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
    return {
        'openai_api_key': os.getenv('OPENAI_API_KEY'),
        'run_integration_tests': os.getenv('RUN_INTEGRATION_TESTS', 'false').lower() == 'true',
        'test_audio_file': os.getenv('TEST_AUDIO_FILE', 'tests/fixtures/test_audio.wav'),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        'debug': os.getenv('DEBUG', 'false').lower() == 'true'
    }


def requires_openai_key(test_func):
    """Decorator to skip tests that require OpenAI API key if not available."""
    def wrapper(*args, **kwargs):
        config = load_test_env()
        if not config['openai_api_key']:
            pytest.skip("OpenAI API key not found in .env file. Set OPENAI_API_KEY to run this test.")
        return test_func(*args, **kwargs)
    return wrapper


def requires_integration_tests(test_func):
    """Decorator to skip integration tests unless explicitly enabled."""
    def wrapper(*args, **kwargs):
        config = load_test_env()
        if not config['run_integration_tests']:
            pytest.skip("Integration tests disabled. Set RUN_INTEGRATION_TESTS=true in .env to run.")
        return test_func(*args, **kwargs)
    return wrapper


def create_test_audio_file(filepath: str, duration: float = 2.0, sample_rate: int = 22050):
    """Create a simple test audio file for testing purposes."""
    try:
        import numpy as np
        import soundfile as sf
        
        # Generate a simple sine wave
        t = np.linspace(0, duration, int(sample_rate * duration))
        frequency = 440  # A4 note
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Write audio file
        sf.write(filepath, audio, sample_rate)
        return filepath
    except ImportError:
        pytest.skip("soundfile and numpy required for audio file generation")


class TestConfig:
    """Test configuration class for consistent test setup."""
    
    def __init__(self):
        self.config = load_test_env()
        self.openai_api_key = self.config['openai_api_key']
        self.run_integration_tests = self.config['run_integration_tests']
        self.test_audio_file = self.config['test_audio_file']
        self.openai_model = self.config['openai_model']
        self.debug = self.config['debug']
    
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is available."""
        return bool(self.openai_api_key)
    
    def should_run_integration_tests(self) -> bool:
        """Check if integration tests should be run."""
        return self.run_integration_tests
    
    def get_test_audio_file(self) -> str:
        """Get path to test audio file, creating it if necessary."""
        if not os.path.exists(self.test_audio_file):
            return create_test_audio_file(self.test_audio_file)
        return self.test_audio_file
