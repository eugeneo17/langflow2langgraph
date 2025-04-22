#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Add output_graphs directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'output_graphs'))

from simple_chat import create_graph as create_simple_chat
from retrieval_qa import create_graph as create_retrieval_qa

def test_simple_chat():
    print("\n=== Testing Simple Chat ===\n")
    app = create_simple_chat()

    test_input = {
        "input": "What is LangGraph?"
    }

    print("Input:", test_input)
    print("\nProcessing...\n")

    try:
        result = app.invoke(test_input)
        print("Output:", result)
        print("\nStatus: Success ✅")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nStatus: Failed ❌")
        return False

def test_retrieval_qa():
    print("\n=== Testing Retrieval QA ===\n")
    app = create_retrieval_qa()

    test_input = {
        "input": "What is LangGraph and what are its key features?"
    }

    print("Input:", test_input)
    print("\nProcessing...\n")

    try:
        result = app.invoke(test_input)
        print("Output:", result)
        print("\nStatus: Success ✅")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nStatus: Failed ❌")
        return False

def main():
    print("Running all example tests...")

    success_count = 0
    total_tests = 2

    if test_simple_chat():
        success_count += 1

    if test_retrieval_qa():
        success_count += 1

    print(f"\nTest Summary: {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("\nAll tests passed! 🎉")
        return 0
    else:
        print("\nSome tests failed. 😢")
        return 1

if __name__ == "__main__":
    sys.exit(main())
