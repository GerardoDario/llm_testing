"""Unit tests for response evaluators."""

import pytest
from src.evaluators.response_evaluator import ResponseEvaluator, AccuracyEvaluator


@pytest.mark.unit
class TestResponseEvaluator:
    """Tests for ResponseEvaluator."""
    
    def test_exact_match(self):
        """Test exact match evaluation."""
        evaluator = ResponseEvaluator()
        score = evaluator.evaluate("The capital is Paris", "Paris")
        assert score == 1.0
    
    def test_case_insensitive_match(self):
        """Test case-insensitive matching."""
        evaluator = ResponseEvaluator(case_sensitive=False)
        score = evaluator.evaluate("The capital is PARIS", "paris")
        assert score == 1.0
    
    def test_case_sensitive_no_match(self):
        """Test case-sensitive matching fails on different cases."""
        evaluator = ResponseEvaluator(case_sensitive=True)
        score = evaluator.evaluate("The capital is PARIS", "paris")
        assert score < 1.0
    
    def test_partial_match(self):
        """Test partial word overlap."""
        evaluator = ResponseEvaluator()
        score = evaluator.evaluate("Paris is a beautiful city", "Paris France")
        assert 0 < score < 1.0
    
    def test_no_match(self):
        """Test no overlap."""
        evaluator = ResponseEvaluator()
        score = evaluator.evaluate("London is great", "Paris")
        assert score == 0.0
    
    def test_evaluate_with_details(self):
        """Test detailed evaluation."""
        evaluator = ResponseEvaluator()
        result = evaluator.evaluate_with_details("Paris is the capital", "Paris")
        
        assert "score" in result
        assert "passed" in result
        assert "response_length" in result
        assert "expected_length" in result
        assert "exact_match" in result
        assert result["exact_match"] is True


@pytest.mark.unit
class TestAccuracyEvaluator:
    """Tests for AccuracyEvaluator."""
    
    def test_initial_state(self):
        """Test initial evaluator state."""
        evaluator = AccuracyEvaluator()
        assert evaluator.get_accuracy() == 0.0
        assert evaluator.correct == 0
        assert evaluator.total == 0
    
    def test_add_correct_result(self):
        """Test adding correct results."""
        evaluator = AccuracyEvaluator()
        evaluator.add_result(True)
        assert evaluator.get_accuracy() == 1.0
        assert evaluator.correct == 1
        assert evaluator.total == 1
    
    def test_add_incorrect_result(self):
        """Test adding incorrect results."""
        evaluator = AccuracyEvaluator()
        evaluator.add_result(False)
        assert evaluator.get_accuracy() == 0.0
        assert evaluator.correct == 0
        assert evaluator.total == 1
    
    def test_mixed_results(self):
        """Test mixed correct and incorrect results."""
        evaluator = AccuracyEvaluator()
        evaluator.add_result(True)
        evaluator.add_result(False)
        evaluator.add_result(True)
        
        assert evaluator.get_accuracy() == pytest.approx(0.666, rel=0.01)
        assert evaluator.correct == 2
        assert evaluator.total == 3
    
    def test_reset(self):
        """Test resetting the evaluator."""
        evaluator = AccuracyEvaluator()
        evaluator.add_result(True)
        evaluator.add_result(False)
        evaluator.reset()
        
        assert evaluator.get_accuracy() == 0.0
        assert evaluator.correct == 0
        assert evaluator.total == 0
    
    def test_get_stats(self):
        """Test getting statistics."""
        evaluator = AccuracyEvaluator()
        evaluator.add_result(True)
        evaluator.add_result(True)
        evaluator.add_result(False)
        
        stats = evaluator.get_stats()
        assert stats["accuracy"] == pytest.approx(0.666, rel=0.01)
        assert stats["correct"] == 2
        assert stats["total"] == 3
        assert stats["incorrect"] == 1
