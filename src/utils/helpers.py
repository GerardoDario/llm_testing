"""Helper utilities for LLM testing."""

import json
from pathlib import Path
from typing import List, Dict, Any
import os


def load_prompts(filepath: str) -> List[Dict[str, Any]]:
    """Load prompts from a JSON file.
    
    Args:
        filepath: Path to the JSON file
        
    Returns:
        List of prompt dictionaries
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_results(results: List[Dict[str, Any]], filepath: str):
    """Save test results to a JSON file.
    
    Args:
        results: List of result dictionaries
        filepath: Path to save the results
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)


def load_env_var(var_name: str, default: str = None) -> str:
    """Load environment variable with optional default.
    
    Args:
        var_name: Name of the environment variable
        default: Default value if not found
        
    Returns:
        The environment variable value
        
    Raises:
        ValueError: If variable not found and no default provided
    """
    value = os.getenv(var_name, default)
    if value is None:
        raise ValueError(f"Environment variable {var_name} not set")
    return value
