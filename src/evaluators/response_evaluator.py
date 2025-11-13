"""Response evaluators for LLM outputs."""

from typing import Optional, Dict, Any


class ResponseEvaluator:
    """Evaluator for LLM responses."""
    
    def __init__(self, case_sensitive: bool = False):
        """Initialize evaluator.
        
        Args:
            case_sensitive: Whether to perform case-sensitive comparison
        """
        self.case_sensitive = case_sensitive
    
    def evaluate(self, response: str, expected: str) -> float:
        """Evaluate response against expected output.
        
        Args:
            response: The LLM response
            expected: The expected output
            
        Returns:
            Score between 0 and 1
        """
        if not self.case_sensitive:
            response = response.lower()
            expected = expected.lower()
        
        # Simple exact match scoring
        if expected in response:
            return 1.0
        
        # Partial match based on word overlap
        response_words = set(response.split())
        expected_words = set(expected.split())
        
        if not expected_words:
            return 0.0
        
        overlap = len(response_words.intersection(expected_words))
        return overlap / len(expected_words)
    
    def evaluate_with_details(self, response: str, expected: str) -> Dict[str, Any]:
        """Evaluate with detailed results.
        
        Args:
            response: The LLM response
            expected: The expected output
            
        Returns:
            Dictionary with score and details
        """
        score = self.evaluate(response, expected)
        
        return {
            "score": score,
            "passed": score >= 0.8,
            "response_length": len(response),
            "expected_length": len(expected),
            "exact_match": expected.lower() in response.lower() if not self.case_sensitive else expected in response
        }


class AccuracyEvaluator:
    """Evaluator for calculating accuracy metrics."""
    
    def __init__(self):
        """Initialize accuracy evaluator."""
        self.correct = 0
        self.total = 0
    
    def add_result(self, is_correct: bool):
        """Add a test result.
        
        Args:
            is_correct: Whether the response was correct
        """
        self.total += 1
        if is_correct:
            self.correct += 1
    
    def get_accuracy(self) -> float:
        """Get current accuracy.
        
        Returns:
            Accuracy between 0 and 1
        """
        if self.total == 0:
            return 0.0
        return self.correct / self.total
    
    def reset(self):
        """Reset the evaluator."""
        self.correct = 0
        self.total = 0
    
    def get_stats(self) -> Dict[str, Any]:
        """Get detailed statistics.
        
        Returns:
            Dictionary with statistics
        """
        return {
            "accuracy": self.get_accuracy(),
            "correct": self.correct,
            "total": self.total,
            "incorrect": self.total - self.correct
        }
