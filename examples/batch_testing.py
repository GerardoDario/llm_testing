"""Example of batch testing with prompts from file."""

import json
from pathlib import Path
from src.llm_client.base import MockLLMClient
from src.evaluators.response_evaluator import ResponseEvaluator
from src.utils.helpers import save_results


def main():
    """Run batch testing example."""
    print("=== Batch Testing Example ===\n")
    
    # Create sample prompts
    prompts = [
        {"id": 1, "text": "What is Python?", "expected": "programming language"},
        {"id": 2, "text": "What is 10 + 5?", "expected": "15"},
        {"id": 3, "text": "Name a color", "expected": "blue"}
    ]
    
    # Mock responses
    responses = [
        "Python is a high-level programming language.",
        "10 + 5 equals 15.",
        "Blue is a nice color."
    ]
    
    # Initialize
    client = MockLLMClient(responses=responses)
    evaluator = ResponseEvaluator()
    
    # Run batch tests
    results = []
    for prompt_data in prompts:
        response = client.generate(prompt_data["text"])
        eval_result = evaluator.evaluate_with_details(
            response, 
            prompt_data["expected"]
        )
        
        results.append({
            "prompt_id": prompt_data["id"],
            "prompt": prompt_data["text"],
            "response": response,
            "expected": prompt_data["expected"],
            "score": eval_result["score"],
            "passed": eval_result["passed"]
        })
        
        print(f"Test {prompt_data['id']}: {'✓' if eval_result['passed'] else '✗'}")
    
    # Save results
    output_file = "/tmp/test_results.json"
    save_results(results, output_file)
    print(f"\nResults saved to: {output_file}")
    
    # Print summary
    passed = sum(1 for r in results if r["passed"])
    print(f"\nPassed: {passed}/{len(results)}")


if __name__ == "__main__":
    main()
