"""Unit tests for LLM clients."""

import pytest
from src.llm_client.base import MockLLMClient


@pytest.mark.unit
class TestMockLLMClient:
    """Tests for MockLLMClient."""
    
    def test_initialization(self):
        """Test client initialization."""
        client = MockLLMClient(model="test-model")
        assert client.model == "test-model"
        assert client.call_count == 0
    
    def test_generate_single_response(self):
        """Test generating a single response."""
        client = MockLLMClient(responses=["Hello, world!"])
        response = client.generate("Test prompt")
        assert response == "Hello, world!"
        assert client.call_count == 1
    
    def test_generate_multiple_responses(self):
        """Test generating multiple responses."""
        responses = ["Response 1", "Response 2", "Response 3"]
        client = MockLLMClient(responses=responses)
        
        for i, expected in enumerate(responses):
            response = client.generate(f"Prompt {i}")
            assert response == expected
            assert client.call_count == i + 1
    
    def test_generate_cycles_through_responses(self):
        """Test that responses cycle when exhausted."""
        responses = ["First", "Second"]
        client = MockLLMClient(responses=responses)
        
        # First cycle
        assert client.generate("prompt") == "First"
        assert client.generate("prompt") == "Second"
        
        # Second cycle
        assert client.generate("prompt") == "First"
        assert client.call_count == 3
    
    def test_generate_with_metadata(self):
        """Test generating response with metadata."""
        client = MockLLMClient(responses=["Test response"])
        result = client.generate_with_metadata("What is AI?")
        
        assert result["response"] == "Test response"
        assert result["model"] == "mock-model"
        assert result["prompt"] == "What is AI?"
        assert "tokens_used" in result
        assert result["tokens_used"] > 0
