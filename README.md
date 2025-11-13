# LLM Testing Repository

A comprehensive repository for testing Large Language Models (LLMs). This project provides tools, utilities, and test cases for evaluating LLM performance, accuracy, and behavior.

## Overview

This repository is designed to facilitate systematic testing of LLM models across various scenarios including:
- Response quality evaluation
- Prompt engineering validation
- Performance benchmarking
- Bias and safety testing
- API integration testing

## Project Structure

```
llm_testing/
├── src/
│   ├── llm_client/          # LLM client wrappers
│   ├── evaluators/          # Evaluation metrics
│   └── utils/               # Utility functions
├── tests/
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── e2e/                 # End-to-end tests
├── examples/                # Example usage scripts
├── data/                    # Test data and prompts
└── docs/                    # Documentation
```

## Installation

```bash
# Clone the repository
git clone https://github.com/GerardoDario/llm_testing.git
cd llm_testing

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Running Tests

```bash
# Run all tests
pytest

# Run specific test category
pytest tests/unit/
pytest tests/integration/

# Run with coverage
pytest --cov=src tests/
```

### Example Usage

```python
from src.llm_client import LLMClient
from src.evaluators import ResponseEvaluator

# Initialize client
client = LLMClient(model="gpt-3.5-turbo")

# Test prompt
response = client.generate("What is the capital of France?")

# Evaluate response
evaluator = ResponseEvaluator()
score = evaluator.evaluate(response, expected="Paris")
```

## Testing Categories

### 1. Unit Tests
Test individual components in isolation.

### 2. Integration Tests
Test interactions between different components.

### 3. End-to-End Tests
Test complete workflows from prompt to evaluation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License

## Contact

For questions or issues, please open an issue on GitHub.