# Testing Guide

## Overview

This guide covers best practices for testing Large Language Models (LLMs) using this framework.

## Test Categories

### Unit Tests

Unit tests focus on testing individual components in isolation:

- **LLM Clients**: Test mock clients, API wrappers
- **Evaluators**: Test scoring and evaluation logic
- **Utilities**: Test helper functions

Run unit tests:
```bash
pytest tests/unit/ -v
```

### Integration Tests

Integration tests verify that different components work together correctly:

- **Complete workflows**: End-to-end prompt-response-evaluation cycles
- **Batch processing**: Multiple prompts in sequence
- **Data persistence**: Loading and saving results

Run integration tests:
```bash
pytest tests/integration/ -v
```

### End-to-End Tests

E2E tests simulate real-world usage scenarios with actual LLM APIs (when configured).

## Writing Tests

### Test Structure

```python
import pytest
from src.llm_client.base import MockLLMClient

@pytest.mark.unit
def test_example():
    # Arrange
    client = MockLLMClient()
    
    # Act
    response = client.generate("test prompt")
    
    # Assert
    assert response is not None
```

### Using Fixtures

```python
@pytest.fixture
def mock_client():
    return MockLLMClient(responses=["test response"])

def test_with_fixture(mock_client):
    response = mock_client.generate("prompt")
    assert "test" in response
```

## Best Practices

1. **Use Mock Clients**: For unit tests, use `MockLLMClient` to avoid API calls
2. **Test Edge Cases**: Include tests for empty inputs, special characters, etc.
3. **Verify Metrics**: Always validate evaluation metrics and scores
4. **Document Test Cases**: Use clear test names and docstrings
5. **Keep Tests Fast**: Unit tests should run quickly

## Continuous Testing

Run tests automatically on code changes:

```bash
# Watch mode (requires pytest-watch)
pytest-watch

# With coverage
pytest --cov=src --cov-report=html tests/
```

## Debugging Failed Tests

```bash
# Verbose output
pytest -vv

# Show print statements
pytest -s

# Run specific test
pytest tests/unit/test_llm_client.py::TestMockLLMClient::test_initialization
```
