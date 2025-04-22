#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Batch Converter for Langflow to LangGraph (Project-based)
--------------------------------------------------------

This script converts Langflow JSON files in project-based input_flows directories
to LangGraph Python files in the corresponding output_graphs directories.
"""

import os
import sys
import glob
from langflow2langgraph import convert_langflow_to_langgraph

def main():
    """Main function to batch convert Langflow JSON files to LangGraph Python files."""
    # Get all project directories
    project_dirs = [d for d in glob.glob("projects/*/") if os.path.isdir(d)]
    
    if not project_dirs:
        print("No project directories found")
        return 1
    
    print(f"Found {len(project_dirs)} project directories")
    
    total_files = 0
    success_count = 0
    
    # Process each project directory
    for project_dir in project_dirs:
        project_name = os.path.basename(os.path.dirname(project_dir))
        print(f"\nProcessing project: {project_name}")
        
        # Create input_flows and output_graphs directories if they don't exist
        input_dir = os.path.join(project_dir, "input_flows")
        output_dir = os.path.join(project_dir, "output_graphs")
        
        if not os.path.exists(input_dir):
            os.makedirs(input_dir)
            print(f"Created {input_dir} directory")
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created {output_dir} directory")
        
        # Get all JSON files in the input_flows directory
        input_files = glob.glob(os.path.join(input_dir, "*.json"))
        
        if not input_files:
            print(f"No JSON files found in {input_dir}")
            continue
        
        print(f"Found {len(input_files)} JSON files to convert")
        total_files += len(input_files)
        
        # Convert each JSON file
        for input_file in input_files:
            # Get the base filename without extension
            base_name = os.path.basename(input_file).replace(".json", "")
            
            # Create the output filename
            output_file = os.path.join(output_dir, f"{base_name}.py")
            
            print(f"\nConverting {input_file} -> {output_file}")
            
            try:
                # Convert the file
                convert_langflow_to_langgraph(input_file, output_file, validate=True)
                print(f"Successfully converted {base_name}")
                success_count += 1
            except Exception as e:
                print(f"Error converting {base_name}: {str(e)}")
    
    print(f"\nConversion complete: {success_count}/{total_files} files converted successfully")
    
    if success_count == total_files:
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main())
