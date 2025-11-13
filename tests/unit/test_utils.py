"""Unit tests for utility functions."""

import pytest
import json
import tempfile
from pathlib import Path
from src.utils.helpers import load_prompts, save_results, load_env_var
import os


@pytest.mark.unit
class TestHelpers:
    """Tests for helper utilities."""
    
    def test_load_prompts_success(self, tmp_path):
        """Test loading prompts from file."""
        # Create a temporary prompts file
        prompts_file = tmp_path / "prompts.json"
        test_prompts = [
            {"id": 1, "text": "What is AI?"},
            {"id": 2, "text": "Explain machine learning"}
        ]
        
        with open(prompts_file, 'w') as f:
            json.dump(test_prompts, f)
        
        loaded = load_prompts(str(prompts_file))
        assert len(loaded) == 2
        assert loaded[0]["text"] == "What is AI?"
    
    def test_load_prompts_file_not_found(self):
        """Test loading prompts from non-existent file."""
        with pytest.raises(FileNotFoundError):
            load_prompts("/nonexistent/file.json")
    
    def test_save_results_success(self, tmp_path):
        """Test saving results to file."""
        results_file = tmp_path / "results.json"
        test_results = [
            {"score": 0.95, "passed": True},
            {"score": 0.70, "passed": False}
        ]
        
        save_results(test_results, str(results_file))
        
        # Verify file was created and contains correct data
        assert results_file.exists()
        with open(results_file, 'r') as f:
            loaded = json.load(f)
        assert len(loaded) == 2
        assert loaded[0]["score"] == 0.95
    
    def test_save_results_creates_directory(self, tmp_path):
        """Test that save_results creates parent directories."""
        results_file = tmp_path / "nested" / "dir" / "results.json"
        test_results = [{"test": "data"}]
        
        save_results(test_results, str(results_file))
        
        assert results_file.exists()
        assert results_file.parent.exists()
    
    def test_load_env_var_exists(self):
        """Test loading existing environment variable."""
        os.environ["TEST_VAR"] = "test_value"
        value = load_env_var("TEST_VAR")
        assert value == "test_value"
        del os.environ["TEST_VAR"]
    
    def test_load_env_var_with_default(self):
        """Test loading non-existent var with default."""
        value = load_env_var("NONEXISTENT_VAR", default="default_value")
        assert value == "default_value"
    
    def test_load_env_var_missing_no_default(self):
        """Test loading non-existent var without default."""
        with pytest.raises(ValueError):
            load_env_var("NONEXISTENT_VAR")
