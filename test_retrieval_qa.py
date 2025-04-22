#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

# Add output_graphs directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'output_graphs'))

from retrieval_qa import create_graph

def test_retrieval_qa():
    # Create the graph
    app = create_graph()

    # Test with a simple input
    test_input = {
        "input": "What is LangGraph and what are its key features?"
    }

    print("Input:", test_input)
    print("\nProcessing...\n")

    try:
        # Run the graph
        result = app.invoke(test_input)
        print("Output:", result)
        print("\nStatus: Success ✅")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nStatus: Failed ❌")

if __name__ == "__main__":
    print("=== Testing Retrieval QA ===\n")
    test_retrieval_qa()
