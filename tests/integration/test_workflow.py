"""Integration tests for LLM testing workflow."""

import pytest
from src.llm_client.base import MockLLMClient
from src.evaluators.response_evaluator import ResponseEvaluator, AccuracyEvaluator


@pytest.mark.integration
class TestLLMWorkflow:
    """Test complete LLM testing workflow."""
    
    def test_basic_workflow(self):
        """Test basic question-answer workflow."""
        # Setup
        client = MockLLMClient(responses=["Paris is the capital of France"])
        evaluator = ResponseEvaluator()
        
        # Execute
        prompt = "What is the capital of France?"
        response = client.generate(prompt)
        score = evaluator.evaluate(response, "Paris")
        
        # Verify
        assert score == 1.0
    
    def test_batch_evaluation(self):
        """Test evaluating multiple prompts."""
        # Setup test cases
        test_cases = [
            {"prompt": "What is 2+2?", "expected": "4"},
            {"prompt": "What is the capital of Spain?", "expected": "Madrid"},
            {"prompt": "Who wrote Romeo and Juliet?", "expected": "Shakespeare"}
        ]
        
        responses = ["The answer is 4", "Madrid", "William Shakespeare"]
        client = MockLLMClient(responses=responses)
        evaluator = ResponseEvaluator()
        accuracy = AccuracyEvaluator()
        
        # Execute
        results = []
        for test_case in test_cases:
            response = client.generate(test_case["prompt"])
            score = evaluator.evaluate(response, test_case["expected"])
            passed = score >= 0.8
            accuracy.add_result(passed)
            results.append({"score": score, "passed": passed})
        
        # Verify
        assert len(results) == 3
        assert all(r["passed"] for r in results)
        assert accuracy.get_accuracy() == 1.0
    
    def test_workflow_with_metadata(self):
        """Test workflow with metadata tracking."""
        client = MockLLMClient(responses=["The capital of France is Paris."])
        evaluator = ResponseEvaluator()
        
        # Generate with metadata
        result = client.generate_with_metadata("What is the capital of France?")
        
        # Evaluate
        eval_result = evaluator.evaluate_with_details(
            result["response"], 
            "Paris"
        )
        
        # Verify both response and evaluation metadata
        assert result["model"] == "mock-model"
        assert eval_result["passed"] is True
        assert eval_result["exact_match"] is True
