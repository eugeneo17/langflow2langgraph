#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fix All Files
------------

This script fixes all the Python files in the output_graphs directory.
"""

import os
import sys
import glob
import re

def fix_file(file_path):
    """Fix a Python file."""
    print(f"Fixing {file_path}...")
    
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        
        # Check for indentation issues
        if re.match(r'^\s+if\s+.*:$', line) or \
           re.match(r'^\s+elif\s+.*:$', line) or \
           re.match(r'^\s+else:$', line) or \
           re.match(r'^\s+for\s+.*:$', line) or \
           re.match(r'^\s+while\s+.*:$', line) or \
           re.match(r'^\s+try:$', line) or \
           re.match(r'^\s+except\s+.*:$', line) or \
           re.match(r'^\s+finally:$', line):
            # Add the control statement
            fixed_lines.append(line + '\n')
            
            # Check the next line
            if i + 1 < len(lines):
                next_line = lines[i + 1].rstrip()
                current_indent = len(line) - len(line.lstrip())
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # If the next line is not properly indented
                if next_indent <= current_indent and next_line and not next_line.lstrip().startswith(('elif', 'else', 'except', 'finally')):
                    # Add proper indentation
                    indent = ' ' * (current_indent + 4)
                    fixed_lines.append(indent + next_line.lstrip() + '\n')
                    i += 1  # Skip the next line
                    
        # Check for main block indentation
        elif line.strip() == 'if __name__ == "__main__":':
            fixed_lines.append(line + '\n')
            
            # Fix indentation in the main block
            j = i + 1
            while j < len(lines) and lines[j].strip():
                main_line = lines[j].rstrip()
                main_indent = len(main_line) - len(main_line.lstrip())
                
                # If the line is not properly indented
                if main_indent != 4:
                    fixed_lines.append(' ' * 4 + main_line.lstrip() + '\n')
                else:
                    fixed_lines.append(main_line + '\n')
                
                j += 1
                i = j - 1  # Update i to skip the processed lines
                
        else:
            fixed_lines.append(line + '\n')
        
        i += 1
    
    with open(file_path, 'w') as f:
        f.writelines(fixed_lines)
    
    print(f"Fixed {file_path}")

def main():
    """Main function to fix all files."""
    # Get all Python files in the output_graphs directory
    graph_files = glob.glob("output_graphs/*.py")
    
    if not graph_files:
        print("No Python files found in output_graphs directory")
        return 1
    
    print(f"Found {len(graph_files)} files to fix")
    
    # Fix each file
    for file_path in graph_files:
        fix_file(file_path)
    
    print(f"\nFixed {len(graph_files)} files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
