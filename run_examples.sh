#!/bin/bash
# Script to run examples with proper PYTHONPATH

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

echo "Running LLM Testing Examples"
echo "=============================="
echo ""

echo "1. Basic Example"
echo "----------------"
python "$SCRIPT_DIR/examples/basic_example.py"
echo ""

echo "2. Batch Testing Example"
echo "------------------------"
python "$SCRIPT_DIR/examples/batch_testing.py"
echo ""

echo "All examples completed!"
