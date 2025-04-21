#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow to LangGraph Utilities
------------------------------

This module contains utility functions for the LangFlow to LangGraph converter.
"""

import re
from typing import Dict, Any, List, Set, Optional


def clean_label_for_python(label: str) -> str:
    """
    Clean a label to make it a valid Python identifier.
    
    Args:
        label: The label to clean
        
    Returns:
        A valid Python identifier
    """
    # Replace non-alphanumeric characters with underscores
    clean = ''.join(c if c.isalnum() else '_' for c in label).lower()
    
    # Ensure it starts with a letter or underscore
    if clean[0].isdigit():
        clean = 'f_' + clean
        
    # Ensure it's not a Python keyword
    python_keywords = {
        'False', 'None', 'True', 'and', 'as', 'assert', 'async', 'await', 
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 
        'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 
        'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 
        'with', 'yield'
    }
    
    if clean in python_keywords:
        clean = clean + '_'
        
    return clean


def extract_python_variables(code: str) -> Set[str]:
    """
    Extract variable names from Python code.
    
    Args:
        code: Python code
        
    Returns:
        Set of variable names
    """
    # Find variable assignments
    assignments = re.findall(r'(\w+)\s*=', code)
    
    # Find function parameters
    func_params = []
    func_defs = re.findall(r'def\s+\w+\s*\(([^)]*)\)', code)
    for params in func_defs:
        for param in params.split(','):
            param = param.strip()
            if param and param != 'self' and param != 'state':
                # Handle type annotations
                if ':' in param:
                    param = param.split(':')[0].strip()
                # Handle default values
                if '=' in param:
                    param = param.split('=')[0].strip()
                func_params.append(param)
    
    # Find for loop variables
    for_vars = re.findall(r'for\s+(\w+)\s+in', code)
    
    # Combine all variables
    all_vars = set(assignments + func_params + for_vars)
    
    return all_vars


def infer_type_from_value(value: str) -> str:
    """
    Infer the Python type from a value string.
    
    Args:
        value: String representation of a value
        
    Returns:
        Type name as a string
    """
    value = value.strip()
    
    if value in ('True', 'False'):
        return 'bool'
    elif value.isdigit():
        return 'int'
    elif re.match(r'^-?\d+(\.\d+)?$', value):
        return 'float'
    elif value.startswith('[') and value.endswith(']'):
        return 'list'
    elif value.startswith('{') and value.endswith('}'):
        return 'dict'
    elif value.startswith('"') and value.endswith('"'):
        return 'str'
    elif value.startswith("'") and value.endswith("'"):
        return 'str'
    elif value == 'None':
        return 'None'
    else:
        return 'Any'


def format_python_code(code: str, indent_level: int = 0) -> str:
    """
    Format Python code with proper indentation.
    
    Args:
        code: Python code to format
        indent_level: Base indentation level
        
    Returns:
        Formatted code
    """
    lines = code.split('\n')
    formatted_lines = []
    current_indent = indent_level
    
    for line in lines:
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            formatted_lines.append('')
            continue
        
        # Check if this line decreases indentation
        if stripped.startswith(('else:', 'elif', 'except:', 'finally:', 'except ', 'finally ')):
            current_indent -= 1
        
        # Add the line with proper indentation
        formatted_lines.append('    ' * current_indent + stripped)
        
        # Check if this line increases indentation
        if stripped.endswith(':') and not stripped.startswith(('#', '"""', "'''")):
            current_indent += 1
            
        # Check if this line decreases indentation for the next line
        if stripped.startswith(('return', 'break', 'continue', 'raise', 'pass')):
            current_indent = max(current_indent - 1, indent_level)
    
    return '\n'.join(formatted_lines)


def extract_docstring(code: str) -> Optional[str]:
    """
    Extract docstring from Python code.
    
    Args:
        code: Python code
        
    Returns:
        Docstring if found, None otherwise
    """
    # Look for triple-quoted strings
    triple_quote_match = re.search(r'"""(.*?)"""', code, re.DOTALL)
    if triple_quote_match:
        return triple_quote_match.group(1).strip()
    
    triple_single_quote_match = re.search(r"'''(.*?)'''", code, re.DOTALL)
    if triple_single_quote_match:
        return triple_single_quote_match.group(1).strip()
    
    return None
