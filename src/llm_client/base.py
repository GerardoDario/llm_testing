"""Base LLM Client interface."""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    def __init__(self, model: str, api_key: Optional[str] = None):
        """Initialize the LLM client.
        
        Args:
            model: The model identifier
            api_key: Optional API key for authentication
        """
        self.model = model
        self.api_key = api_key
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters for generation
            
        Returns:
            The generated response text
        """
        pass
    
    @abstractmethod
    def generate_with_metadata(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a response with metadata.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters for generation
            
        Returns:
            Dictionary containing response and metadata
        """
        pass


class MockLLMClient(LLMClient):
    """Mock LLM client for testing purposes."""
    
    def __init__(self, model: str = "mock-model", responses: Optional[list] = None):
        """Initialize mock client.
        
        Args:
            model: Model name
            responses: List of predefined responses
        """
        super().__init__(model)
        self.responses = responses or ["This is a mock response."]
        self.call_count = 0
    
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate a mock response.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters (ignored)
            
        Returns:
            A mock response
        """
        response = self.responses[self.call_count % len(self.responses)]
        self.call_count += 1
        return response
    
    def generate_with_metadata(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Generate a mock response with metadata.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters (ignored)
            
        Returns:
            Dictionary with response and mock metadata
        """
        response = self.generate(prompt, **kwargs)
        return {
            "response": response,
            "model": self.model,
            "tokens_used": len(prompt.split()) + len(response.split()),
            "prompt": prompt
        }
