#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow to LangGraph Converter
-------------------------------

This script converts LangFlow JSON exports to LangGraph Python code.
"""

import sys
from pathlib import Path

# Import from the modular package
from langflow2langgraph.converter import convert_langflow_to_langgraph, LangGraphConversionError

def main():
    """Main entry point for the script"""
    if len(sys.argv) < 2:
        print("Usage: python langgraph2langflow.py <input_file> [output_file]")
        return 1
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        # Convert the file
        print(f"Converting {input_file}...")
        result = convert_langflow_to_langgraph(input_file, output_file)
        
        # If no output file specified, print to stdout
        if not output_file:
            print("\nGenerated LangGraph code:")
            print("=" * 40)
            print(result)
            print("=" * 40)
            print("\nNote: No output file specified. Use a second argument to save to a file.")
        else:
            print(f"Successfully converted {input_file} to {output_file}")
            
        return 0
    except LangGraphConversionError as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
