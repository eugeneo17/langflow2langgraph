#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Batch Converter for Langflow to LangGraph
-----------------------------------------

This script converts all Langflow JSON files in the input_flows directory
to LangGraph Python files in the output_graphs directory.
"""

import os
import sys
import glob
from langflow2langgraph import convert_langflow_to_langgraph

def main():
    """Main function to batch convert Langflow JSON files to LangGraph Python files."""
    # Create input_flows and output_graphs directories if they don't exist
    if not os.path.exists("input_flows"):
        os.makedirs("input_flows")
        print("Created input_flows directory")
    
    if not os.path.exists("output_graphs"):
        os.makedirs("output_graphs")
        print("Created output_graphs directory")
    
    # Get all JSON files in the input_flows directory
    input_files = glob.glob("input_flows/*.json")
    
    if not input_files:
        print("No JSON files found in input_flows directory")
        return 1
    
    print(f"Found {len(input_files)} JSON files to convert")
    
    # Convert each JSON file
    success_count = 0
    for input_file in input_files:
        # Get the base filename without extension
        base_name = os.path.basename(input_file).replace(".json", "")
        
        # Create the output filename
        output_file = f"output_graphs/{base_name}.py"
        
        print(f"\nConverting {input_file} -> {output_file}")
        
        try:
            # Convert the file
            convert_langflow_to_langgraph(input_file, output_file, validate=True)
            print(f"Successfully converted {base_name}")
            success_count += 1
        except Exception as e:
            print(f"Error converting {base_name}: {str(e)}")
    
    print(f"\nConversion complete: {success_count}/{len(input_files)} files converted successfully")
    
    if success_count == len(input_files):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
