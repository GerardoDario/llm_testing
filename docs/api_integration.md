# API Integration Guide

## Supported LLM Providers

This framework can be extended to work with various LLM providers:

- OpenAI (GPT models)
- Anthropic (Claude)
- Local models
- Custom APIs

## Setting Up API Keys

### Environment Variables

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-api-key-here
ANTHROPIC_API_KEY=your-api-key-here
```

### Loading Configuration

```python
from src.utils.helpers import load_env_var

api_key = load_env_var("OPENAI_API_KEY")
```

## Implementing Custom Clients

To add support for a new LLM provider, extend the `LLMClient` base class:

```python
from src.llm_client.base import LLMClient

class CustomLLMClient(LLMClient):
    def __init__(self, model: str, api_key: str):
        super().__init__(model, api_key)
        # Initialize your custom client
    
    def generate(self, prompt: str, **kwargs) -> str:
        # Implement generation logic
        pass
    
    def generate_with_metadata(self, prompt: str, **kwargs):
        # Implement with metadata
        pass
```

## Example: OpenAI Integration

```python
import openai
from src.llm_client.base import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: str = None):
        super().__init__(model, api_key)
        openai.api_key = api_key or os.getenv("OPENAI_API_KEY")
    
    def generate(self, prompt: str, **kwargs) -> str:
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content
    
    def generate_with_metadata(self, prompt: str, **kwargs):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        return {
            "response": response.choices[0].message.content,
            "model": self.model,
            "tokens_used": response.usage.total_tokens,
            "prompt": prompt
        }
```

## Rate Limiting and Retries

When working with real APIs, implement rate limiting:

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        last_called = [0.0]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            min_interval = 60.0 / calls_per_minute
            
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        
        return wrapper
    return decorator
```

## Best Practices

1. **Never commit API keys**: Use environment variables
2. **Implement error handling**: Handle API errors gracefully
3. **Use rate limiting**: Respect API rate limits
4. **Log API calls**: Track usage and costs
5. **Cache responses**: Save money on repeated queries
