#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test All Projects
----------------

This script tests all the LangGraph projects in the projects directory.
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

def test_project(project_dir):
    """Test all graphs in a project."""
    project_name = os.path.basename(os.path.dirname(project_dir))
    print(f"\n=== Testing Project: {project_name} ===\n")
    
    # Get all Python files in the output_graphs directory
    output_dir = os.path.join(project_dir, "output_graphs")
    graph_files = glob.glob(os.path.join(output_dir, "*.py"))
    
    if not graph_files:
        print(f"No Python files found in {output_dir}")
        return 0, 0
    
    print(f"Found {len(graph_files)} graphs to test")
    
    # Test each graph
    success_count = 0
    for graph_file in graph_files:
        if test_graph(graph_file, project_name):
            success_count += 1
    
    print(f"\nProject Summary: {success_count}/{len(graph_files)} tests passed")
    
    return success_count, len(graph_files)

def test_graph(graph_file, project_name):
    """Test a single graph."""
    try:
        # Import the module
        module = import_module_from_file(graph_file)
        
        # Get the base filename without extension
        base_name = os.path.basename(graph_file).replace(".py", "")
        
        print(f"\n=== Testing {project_name}/{base_name} ===\n")
        
        # Check if the module has a create_graph function
        if not hasattr(module, "create_graph"):
            print(f"Error: {base_name} does not have a create_graph function")
            return False
        
        # Create the graph
        graph = module.create_graph()
        
        # Test with a simple input
        test_input = {
            "input": f"Test input for {project_name}/{base_name}"
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
    """Main function to test all projects."""
    # Get all project directories
    project_dirs = [d for d in glob.glob("projects/*/") if os.path.isdir(d)]
    
    if not project_dirs:
        print("No project directories found")
        return 1
    
    print(f"Found {len(project_dirs)} projects to test")
    
    # Test each project
    total_success = 0
    total_tests = 0
    
    for project_dir in project_dirs:
        success, tests = test_project(project_dir)
        total_success += success
        total_tests += tests
    
    print(f"\nOverall Summary: {total_success}/{total_tests} tests passed")
    
    if total_success == total_tests:
        print("\nAll tests passed! 🎉")
        return 0
    else:
        print("\nSome tests failed. 😢")
        return 1

if __name__ == "__main__":
    sys.exit(main())
