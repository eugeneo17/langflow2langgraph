#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangGraph Code Validator
------------------------

This module provides validation for generated LangGraph code.
"""

import ast
import re
from typing import Dict, List, Tuple, Optional, Any

class CodeValidationError(Exception):
    """Exception raised for code validation errors."""
    pass

def validate_python_syntax(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate Python syntax of the generated code.

    Args:
        code: The Python code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}, column {e.offset}: {e.msg}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"

def validate_state_schema(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate the state schema in the generated code.

    Args:
        code: The Python code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if GraphState is defined
    if "class GraphState(TypedDict):" not in code:
        return False, "Missing GraphState definition"

    # Check if StateGraph is initialized with GraphState
    if "graph = StateGraph(GraphState)" not in code:
        return False, "StateGraph not initialized with GraphState"

    return True, None

def validate_node_definitions(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate node definitions in the generated code.

    Args:
        code: The Python code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Extract all function definitions
    function_pattern = r"def\s+(\w+)\s*\(\s*state\s*\):"
    functions = re.findall(function_pattern, code)

    # Extract all node additions
    node_pattern = r"graph\.add_node\s*\(\s*\"(\w+)\"\s*,\s*(\w+)\s*\)"
    nodes = re.findall(node_pattern, code)

    # Check if all node functions are defined
    for node_name, func_name in nodes:
        if func_name not in functions:
            return False, f"Node '{node_name}' references undefined function '{func_name}'"

    return True, None

def validate_edge_definitions(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate edge definitions in the generated code.

    Args:
        code: The Python code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Extract all node additions to get valid node names
    node_pattern = r"graph\.add_node\s*\(\s*\"(\w+)\"\s*,\s*\w+\s*\)"
    nodes = set(re.findall(node_pattern, code))

    # Extract all edge definitions
    edge_pattern = r"graph\.add_edge\s*\(\s*\"(\w+)\"\s*,\s*\"(\w+)\"\s*\)"
    edges = re.findall(edge_pattern, code)

    # Check if all edge endpoints are defined nodes
    for source, target in edges:
        if source not in nodes:
            return False, f"Edge references undefined source node '{source}'"
        if target not in nodes:
            return False, f"Edge references undefined target node '{target}'"

    # Extract all conditional edge definitions
    cond_edge_pattern = r"graph\.add_conditional_edges\s*\(\s*\"(\w+)\"\s*,"
    cond_sources = re.findall(cond_edge_pattern, code)

    # Check if all conditional edge sources are defined nodes
    for source in cond_sources:
        if source not in nodes:
            return False, f"Conditional edge references undefined source node '{source}'"

    return True, None

def validate_entry_exit_points(code: str) -> Tuple[bool, Optional[str]]:
    """
    Validate entry and exit points in the generated code.

    Args:
        code: The Python code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Extract all node additions to get valid node names
    node_pattern = r"graph\.add_node\s*\(\s*\"(\w+)\"\s*,\s*\w+\s*\)"
    nodes = set(re.findall(node_pattern, code))

    # Check entry point
    entry_pattern = r"graph\.set_entry_point\s*\(\s*\"(\w+)\"\s*\)"
    entry_matches = re.findall(entry_pattern, code)

    if not entry_matches:
        return False, "Missing entry point definition"

    entry_point = entry_matches[0]
    if entry_point not in nodes:
        return False, f"Entry point references undefined node '{entry_point}'"

    # Check finish point
    finish_pattern = r"graph\.set_finish_point\s*\(\s*\"(\w+)\"\s*\)"
    finish_matches = re.findall(finish_pattern, code)

    if not finish_matches:
        return False, "Missing finish point definition"

    finish_point = finish_matches[0]
    if finish_point not in nodes:
        return False, f"Finish point references undefined node '{finish_point}'"

    return True, None

def validate_code(code: str) -> Tuple[bool, List[str]]:
    """
    Validate the generated LangGraph code.

    Args:
        code: The Python code to validate

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # Validate Python syntax
    is_valid, error = validate_python_syntax(code)
    if not is_valid:
        errors.append(error)
        # If syntax is invalid, don't continue with other validations
        return False, errors

    # Validate state schema
    is_valid, error = validate_state_schema(code)
    if not is_valid:
        errors.append(error)

    # Validate node definitions
    is_valid, error = validate_node_definitions(code)
    if not is_valid:
        errors.append(error)

    # Validate edge definitions
    is_valid, error = validate_edge_definitions(code)
    if not is_valid:
        errors.append(error)

    # Validate entry and exit points
    is_valid, error = validate_entry_exit_points(code)
    if not is_valid:
        errors.append(error)

    return len(errors) == 0, errors

def fix_common_issues(code: str) -> str:
    """
    Fix common issues in the generated code.

    Args:
        code: The Python code to fix

    Returns:
        Fixed code
    """
    # Complete rewrite of the code with proper indentation
    lines = code.split('\n')
    fixed_code = []

    # Extract imports and class definition
    imports_and_class = []
    i = 0
    while i < len(lines) and not lines[i].strip().startswith('def create_graph'):
        imports_and_class.append(lines[i])
        i += 1

    # Add create_graph function definition
    fixed_code.extend(imports_and_class)
    fixed_code.append('def create_graph():')  # Start of create_graph function
    fixed_code.append('    # Define the graph with proper state schema')
    fixed_code.append('    graph = StateGraph(GraphState)')
    fixed_code.append('')

    # Extract node functions and add them with proper indentation
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Look for node function definitions
        if line.startswith('def ') and '(state)' in line:
            func_name = line.split('def ')[1].split('(')[0].strip()
            fixed_code.append(f'    def {func_name}(state):')  # Function definition

            # Extract function body
            i += 1
            func_body = []

            # Handle if statements properly
            in_if_block = False
            if_indent = 0

            while i < len(lines) and not lines[i].strip().startswith('def ') and not lines[i].strip().startswith('graph.add_node'):
                body_line = lines[i].strip()

                # Skip empty lines but keep track of them
                if not body_line:
                    i += 1
                    continue

                # Handle if statements and their blocks
                if body_line.startswith('if ') and body_line.endswith(':'):
                    func_body.append(f'        {body_line}')  # Indent if statement
                    in_if_block = True
                    if_indent = 8  # Base indent (4) + if block indent (4)
                elif in_if_block:
                    # Lines inside if block get extra indentation
                    func_body.append(f'{" " * if_indent}{body_line}')

                    # Check if we're exiting the if block
                    if body_line.startswith('return '):
                        in_if_block = False
                else:
                    # Normal function body line
                    func_body.append(f'        {body_line}')  # Indent function body

                i += 1

            # Add return statement if missing
            if not any('return' in line for line in func_body):
                func_body.append('        return state')

            fixed_code.extend(func_body)
            fixed_code.append('')  # Empty line after function

            # Add node registration
            if i < len(lines) and lines[i].strip().startswith('graph.add_node'):
                node_line = lines[i].strip()
                fixed_code.append(f'    {node_line}')
                fixed_code.append('')  # Empty line after node registration
                i += 1
        else:
            i += 1

    # Add edges section
    fixed_code.append('    # --- Edges ---')

    # Extract and add edges with proper indentation
    i = 0
    in_edges_section = False
    while i < len(lines):
        line = lines[i].strip()

        if line == '# --- Edges ---' or line == '    # --- Edges ---':
            in_edges_section = True
            i += 1
            continue

        if in_edges_section and (line.startswith('graph.add_edge') or
                                line.startswith('graph.add_conditional_edges') or
                                line.startswith('# Conditional')):
            # Extract edge definition block
            if line.startswith('graph.add_conditional_edges'):
                # Handle multi-line conditional edges
                edge_block = [f'    {line}']
                i += 1
                indent_level = 1
                while i < len(lines) and indent_level > 0:
                    edge_line = lines[i].strip()
                    if '{' in edge_line:
                        indent_level += 1
                    if '}' in edge_line:
                        indent_level -= 1
                    edge_block.append(f'    {edge_line}')
                    i += 1
                fixed_code.extend(edge_block)
                fixed_code.append('')  # Empty line after edge block
            elif line.startswith('# Conditional'):
                # Comment line
                fixed_code.append(f'    {line}')
                i += 1
            else:
                # Simple edge
                fixed_code.append(f'    {line}')
                i += 1
                fixed_code.append('')  # Empty line after edge
        elif in_edges_section and line.startswith('# --- Entry and Finish ---'):
            # End of edges section
            in_edges_section = False
            fixed_code.append('')  # Empty line before entry/finish section
            fixed_code.append('    # --- Entry and Finish ---')
            i += 1
        elif in_edges_section and line.startswith('graph.set_entry_point') or line.startswith('graph.set_finish_point'):
            fixed_code.append(f'    {line}')
            i += 1
        else:
            i += 1

    # Add entry and finish points if missing
    if not any('graph.set_entry_point' in line for line in fixed_code):
        fixed_code.append('    # --- Entry and Finish ---')
        fixed_code.append('    graph.set_entry_point("inputprocessor")')
        fixed_code.append('    graph.set_finish_point("outputformatter")')

    # Add return statement
    fixed_code.append('')
    fixed_code.append('    return graph.compile()')

    # Add main block
    fixed_code.append('')
    fixed_code.append('if __name__ == "__main__":')
    fixed_code.append('    app = create_graph()')
    fixed_code.append('    result = app.invoke({"input": "Test input"})')
    fixed_code.append('    print(result)')

    return '\n'.join(fixed_code)
