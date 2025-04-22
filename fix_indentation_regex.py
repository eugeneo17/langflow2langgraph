#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fix Indentation in Generated Python Files Using Regex
---------------------------------------------------

This script fixes indentation issues in the generated Python files using regular expressions.
"""

import os
import sys
import glob
import re

def fix_indentation(file_path):
    """Fix indentation issues in a Python file using regex."""
    print(f"Fixing indentation in {file_path}...")
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix indentation after if statements
    pattern = r'(\s+if\s+.*?:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', content, flags=re.DOTALL)
    
    # Fix indentation after elif statements
    pattern = r'(\s+elif\s+.*?:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    # Fix indentation after else statements
    pattern = r'(\s+else:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    # Fix indentation after for statements
    pattern = r'(\s+for\s+.*?:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    # Fix indentation after while statements
    pattern = r'(\s+while\s+.*?:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    # Fix indentation after try statements
    pattern = r'(\s+try:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    # Fix indentation after except statements
    pattern = r'(\s+except\s+.*?:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    # Fix indentation after finally statements
    pattern = r'(\s+finally:)\s*\n\s*([^\s])'
    fixed_content = re.sub(pattern, r'\1\n        \2', fixed_content, flags=re.DOTALL)
    
    with open(file_path, 'w') as f:
        f.write(fixed_content)
    
    print(f"Fixed indentation in {file_path}")

def main():
    """Main function to fix indentation in all Python files."""
    # Get all Python files in the output_graphs directory
    graph_files = glob.glob("output_graphs/*.py")
    
    if not graph_files:
        print("No Python files found in output_graphs directory")
        return 1
    
    print(f"Found {len(graph_files)} files to fix")
    
    # Fix indentation in each file
    for file_path in graph_files:
        fix_indentation(file_path)
    
    print(f"\nFixed indentation in {len(graph_files)} files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
