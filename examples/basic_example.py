"""Basic example of using the LLM testing framework."""

from src.llm_client.base import MockLLMClient
from src.evaluators.response_evaluator import ResponseEvaluator, AccuracyEvaluator


def main():
    """Run a basic LLM testing example."""
    print("=== LLM Testing Example ===\n")
    
    # Initialize client and evaluators
    responses = [
        "Paris is the capital of France.",
        "The answer is 42.",
        "Python was created by Guido van Rossum."
    ]
    client = MockLLMClient(responses=responses)
    evaluator = ResponseEvaluator()
    accuracy = AccuracyEvaluator()
    
    # Define test cases
    test_cases = [
        {
            "prompt": "What is the capital of France?",
            "expected": "Paris"
        },
        {
            "prompt": "What is the answer to life, universe, and everything?",
            "expected": "42"
        },
        {
            "prompt": "Who created Python?",
            "expected": "Guido van Rossum"
        }
    ]
    
    # Run tests
    print("Running tests...\n")
    for i, test_case in enumerate(test_cases, 1):
        print(f"Test {i}:")
        print(f"  Prompt: {test_case['prompt']}")
        
        # Generate response
        response = client.generate(test_case["prompt"])
        print(f"  Response: {response}")
        
        # Evaluate
        result = evaluator.evaluate_with_details(response, test_case["expected"])
        print(f"  Score: {result['score']:.2f}")
        print(f"  Passed: {result['passed']}")
        
        accuracy.add_result(result["passed"])
        print()
    
    # Print summary
    stats = accuracy.get_stats()
    print("=== Summary ===")
    print(f"Total tests: {stats['total']}")
    print(f"Passed: {stats['correct']}")
    print(f"Failed: {stats['incorrect']}")
    print(f"Accuracy: {stats['accuracy']:.2%}")


if __name__ == "__main__":
    main()
