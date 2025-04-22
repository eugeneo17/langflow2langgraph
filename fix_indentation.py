#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import os

def fix_indentation(file_path):
    """Fix indentation issues in the generated Python file."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    fixed_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        fixed_lines.append(line)
        
        # Check for if statements without proper indentation
        if re.match(r'^\s+if\s+.*:$', line.strip()):
            # Look ahead to see if the next line is indented
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                current_indent = len(line) - len(line.lstrip())
                next_indent = len(next_line) - len(next_line.lstrip())
                
                # If the next line is not indented more than the current line
                if next_indent <= current_indent and next_line.strip() and not next_line.strip().startswith(('elif', 'else')):
                    # Insert proper indentation
                    indent = ' ' * (current_indent + 4)
                    fixed_lines.append(f"{indent}{next_line.strip()}\\n")
                    i += 1  # Skip the next line since we've handled it
        
        i += 1
    
    with open(file_path, 'w') as f:
        f.writelines(fixed_lines)

def main():
    """Main function to fix indentation in generated files."""
    files_to_fix = [
        "generated_simple_chat.py",
        "generated_retrieval_qa.py",
        "generated_agent.py",
        "generated_loop_graph.py",
        "generated_conditional_graph.py"
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            print(f"Fixing indentation in {file_path}...")
            fix_indentation(file_path)
            print(f"Fixed {file_path}")
        else:
            print(f"File {file_path} not found")

if __name__ == "__main__":
    main()
