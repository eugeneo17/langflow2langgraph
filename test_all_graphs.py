#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test All Converted Graphs
------------------------

This script tests all the converted LangGraph Python files in the output_graphs directory.
"""

import os
import sys
import importlib.util
import glob

def import_module_from_file(file_path):
    """Import a module from a file path."""
    module_name = os.path.basename(file_path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def test_graph(graph_file):
    """Test a single graph."""
    try:
        # Import the module
        module = import_module_from_file(graph_file)
        
        # Get the base filename without extension
        base_name = os.path.basename(graph_file).replace(".py", "")
        
        print(f"\n=== Testing {base_name} ===\n")
        
        # Check if the module has a create_graph function
        if not hasattr(module, "create_graph"):
            print(f"Error: {base_name} does not have a create_graph function")
            return False
        
        # Create the graph
        graph = module.create_graph()
        
        # Test with a simple input
        test_input = {
            "input": f"Test input for {base_name}"
        }
        
        print("Input:", test_input)
        print("\nProcessing...\n")
        
        # Run the graph
        result = graph.invoke(test_input)
        
        print("Output:", result)
        print("\nStatus: Success ✅")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nStatus: Failed ❌")
        return False

def main():
    """Main function to test all converted graphs."""
    # Get all Python files in the output_graphs directory
    graph_files = glob.glob("output_graphs/*.py")
    
    if not graph_files:
        print("No Python files found in output_graphs directory")
        return 1
    
    print(f"Found {len(graph_files)} graphs to test")
    
    # Test each graph
    success_count = 0
    for graph_file in graph_files:
        if test_graph(graph_file):
            success_count += 1
    
    print(f"\nTest Summary: {success_count}/{len(graph_files)} tests passed")
    
    if success_count == len(graph_files):
        print("\nAll tests passed! 🎉")
        return 0
    else:
        print("\nSome tests failed. 😢")
        return 1

if __name__ == "__main__":
    sys.exit(main())
