#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangGraph Code Validator
-----------------------

This module validates and fixes common issues in generated LangGraph code.
"""

import re
import ast
from typing import Dict, List, Tuple, Any, Optional

class LangGraphValidationError(Exception):
    """Exception raised for errors during LangGraph code validation."""
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

def fix_indentation(code: str) -> str:
    """
    Fix indentation issues in the generated code.

    Args:
        code: The Python code to fix

    Returns:
        Fixed code with proper indentation
    """
    lines = code.split('\n')
    fixed_lines = []

    # Track indentation level
    indent_level = 0
    in_function = False
    in_class = False

    for line in lines:
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            fixed_lines.append('')
            continue

        # Determine indentation level based on context
        if stripped.startswith('def ') and stripped.endswith(':'):
            # Function definition
            if in_class:
                # Method in a class
                indent_level = 1
            else:
                # Top-level function
                indent_level = 0
            in_function = True
        elif stripped.startswith('class ') and stripped.endswith(':'):
            # Class definition
            indent_level = 0
            in_class = True
        elif stripped.startswith('if ') and stripped.endswith(':'):
            # If statement
            if in_function:
                indent_level = 2 if in_class else 1
            else:
                indent_level = 1 if in_class else 0
        elif stripped.startswith('elif ') or stripped.startswith('else:'):
            # Maintain current indentation for elif/else
            pass
        elif stripped.startswith('return '):
            # Return statement
            if in_function:
                indent_level = 1 if in_class else 0

        # Apply indentation
        if stripped.startswith('def ') or stripped.startswith('class '):
            # No indentation for function/class definitions
            fixed_lines.append(stripped)
        else:
            # Apply appropriate indentation
            fixed_lines.append('    ' * indent_level + stripped)

    return '\n'.join(fixed_lines)

def fix_common_issues(code: str) -> str:
    """
    Fix common issues in the generated code.

    Args:
        code: The Python code to fix

    Returns:
        Fixed code
    """
    # Completely rewrite the code with proper indentation
    # First, parse the code into logical sections
    sections = {
        'imports': [],
        'class_def': [],
        'functions': [],
        'edges': [],
        'entry_finish': [],
        'return': [],
        'main': []
    }

    # Create a mapping of node names to function names
    node_name_mapping = {}

    lines = code.split('\n')
    current_section = 'imports'
    current_function = None
    function_lines = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Determine section
        if line.startswith('import ') or line.startswith('from '):
            sections['imports'].append(line)
        elif line.startswith('class GraphState'):
            current_section = 'class_def'
            sections['class_def'].append(line)
        elif line.startswith('def create_graph'):
            current_section = 'functions'
        elif line.startswith('def ') and '(state)' in line and current_section == 'functions':
            # Start of a new function
            if current_function:
                # Save previous function
                sections['functions'].append((current_function, function_lines))
            current_function = line.split('def ')[1].split('(')[0].strip()
            function_lines = []
        elif line.startswith('# --- Edges ---'):
            # End of functions section, start of edges
            if current_function:
                sections['functions'].append((current_function, function_lines))
                current_function = None
            current_section = 'edges'
        elif line.startswith('# --- Entry and Finish ---'):
            current_section = 'entry_finish'
        elif line.startswith('return graph.compile'):
            current_section = 'return'
            sections['return'].append(line)
        elif line.startswith('if __name__ =='):
            current_section = 'main'
            sections['main'].append(line)
        else:
            # Add line to current section
            if current_section == 'class_def':
                sections['class_def'].append(line)
            elif current_section == 'functions' and current_function:
                function_lines.append(line)

                # Extract node name mappings from graph.add_node calls
                if 'graph.add_node' in line:
                    node_match = re.search(r'graph\.add_node\("([^"]+)",\s*([^\)]+)\)', line)
                    if node_match:
                        node_name = node_match.group(1)
                        func_name = node_match.group(2).strip()
                        node_name_mapping[node_name] = func_name

            elif current_section == 'edges':
                sections['edges'].append(line)
            elif current_section == 'entry_finish':
                sections['entry_finish'].append(line)
            elif current_section == 'main':
                sections['main'].append(line)

        i += 1

    # If there's a function being processed at the end
    if current_function and function_lines:
        sections['functions'].append((current_function, function_lines))

    # Extract function names for additional node name mapping
    function_names = [func_name for func_name, _ in sections['functions']]

    # Add function names to node name mapping if not already present
    for func_name in function_names:
        if func_name not in node_name_mapping.values():
            # Check if there's a similar node name already in the mapping
            similar_node = None
            for node_name in list(node_name_mapping.keys()):
                if node_name in func_name or func_name in node_name:
                    similar_node = node_name
                    break

            if similar_node:
                # Update the mapping
                node_name_mapping[similar_node] = func_name
            else:
                # Add a new mapping
                node_name_mapping[func_name] = func_name

    # Now rebuild the code with proper formatting
    fixed_code = []

    # Add imports
    for imp in sections['imports']:
        fixed_code.append(imp)
    fixed_code.append('')

    # Add class definition with proper indentation
    if sections['class_def']:
        # First line is the class definition
        fixed_code.append(sections['class_def'][0])
        # Remaining lines are the class fields, which need indentation
        for line in sections['class_def'][1:]:
            fixed_code.append(f'    {line}')
    fixed_code.append('')

    # Add create_graph function
    fixed_code.append('def create_graph():')
    fixed_code.append('    """Create and configure the LangGraph."""')
    fixed_code.append('    # Initialize the graph')
    fixed_code.append('    graph = StateGraph(GraphState)')
    fixed_code.append('')

    # Add node functions
    fixed_code.append('    # --- Node Functions ---')
    for func_name, func_lines in sections['functions']:
        # Check if this is a generated function from our code generators
        is_generated = False
        for line in func_lines:
            if line.strip().startswith('def ') and line.strip().endswith('(state):'):
                is_generated = True
                break

        if is_generated:
            # For generated functions, we need to extract the function body and indent it properly
            # First, find the function definition line
            func_def_idx = -1
            for i, line in enumerate(func_lines):
                if line.strip().startswith('def ') and line.strip().endswith('(state):'):
                    func_def_idx = i
                    break

            if func_def_idx >= 0:
                # Add our own function definition
                fixed_code.append(f'    def {func_name}(state):')

                # Process the rest of the lines with proper indentation
                for i, line in enumerate(func_lines[func_def_idx+1:]):
                    # Skip node registration lines
                    if 'graph.add_node' in line:
                        continue

                    # Skip empty lines
                    if not line.strip():
                        fixed_code.append('')
                        continue

                    # Add proper indentation to all lines
                    # Check if this is a line that needs indentation
                    if line.strip().startswith('if ') or line.strip().startswith('for ') or line.strip().startswith('while ') or line.strip().startswith('try:'):
                        # Control statement - no extra indentation needed
                        fixed_code.append(f'        {line.strip()}')
                    elif i > 0 and clean_func_lines[i-1].strip().endswith(':'):
                        # This line follows a control statement and needs indentation
                        fixed_code.append(f'            {line.strip()}')
                    else:
                        # Regular line
                        fixed_code.append(f'        {line.strip()}')
        else:
            # For regular functions, use the existing approach
            fixed_code.append(f'    def {func_name}(state):')

            # Process function body with proper indentation
            has_content = False

            # First, clean up the function lines and remove node registrations
            clean_func_lines = []
            for line in func_lines:
                # Skip node registration lines inside the function body
                if 'graph.add_node' in line:
                    continue
                clean_func_lines.append(line.strip())

            # If we have content, add proper indentation
            if clean_func_lines:
                has_content = True

                # Skip docstring if present as first line
                start_idx = 0
                if clean_func_lines and (clean_func_lines[0].startswith('"""') or clean_func_lines[0].startswith("'''")):
                    # Find the end of the docstring
                    for i, line in enumerate(clean_func_lines[1:], 1):
                        if line.endswith('"""') or line.endswith("'''"):
                            start_idx = i + 1
                            break
                    # Add the docstring with proper indentation
                    for i in range(start_idx):
                        fixed_code.append(f'        {clean_func_lines[i]}')
                else:
                    # Add a default docstring if none is present
                    fixed_code.append('        """Process the state in this node."""')

                # Process each line with proper indentation
                current_indent = 0
                for i, line in enumerate(clean_func_lines[start_idx:], start_idx):
                    # Skip empty lines
                    if not line:
                        fixed_code.append('')
                        continue

                    # Determine indentation level
                    if line.startswith('if ') or line.startswith('for ') or line.startswith('while ') or line.startswith('try:'):
                        # Start of a new block
                        fixed_code.append(f'        {line}')
                        current_indent = 1
                    elif line.startswith('elif ') or line.startswith('else:') or line.startswith('except ') or line.startswith('finally:'):
                        # Continue a block at the same level
                        fixed_code.append(f'        {line}')
                        current_indent = 1
                    elif line.startswith('return '):
                        # Return statement
                        fixed_code.append(f'        {line}')
                    else:
                        # Regular line - use current indentation
                        # Check if this line follows a control statement
                        prev_line_idx = i - 1
                        while prev_line_idx >= start_idx and not clean_func_lines[prev_line_idx].strip():
                            prev_line_idx -= 1

                        if prev_line_idx >= start_idx and clean_func_lines[prev_line_idx].strip().endswith(':'):
                            # This line follows a control statement and needs indentation
                            fixed_code.append(f'            {line}')
                        else:
                            # Regular indentation
                            fixed_code.append(f'        {"    " * current_indent}{line}')

            # If no content, add a placeholder
            if not has_content:
                fixed_code.append('        # Implementation for this node')
                fixed_code.append('        return state')

        # Add node registration (only once)
        # Check if this node registration is already in the function body
        if not any(f'graph.add_node("{func_name}"' in line for line in func_lines):
            fixed_code.append(f'    graph.add_node("{func_name}", {func_name})')
        fixed_code.append('')

    # Add edges section
    fixed_code.append('    # --- Edges ---')

    # Process edges with proper indentation and fix node names
    i = 0
    while i < len(sections['edges']):
        line = sections['edges'][i]

        # Fix node names in edges to match function names
        if 'graph.add_edge' in line or 'graph.add_conditional_edges' in line or 'graph.set_entry_point' in line or 'graph.set_finish_point' in line:
            # Extract node names from the line
            node_names = re.findall(r'"([^"]+)"', line)

            # Replace old node names with function names using the mapping
            for old_name in node_names:
                # Skip if the name is already a function name
                if old_name in function_names:
                    continue

                # Check if we have a direct mapping
                if old_name in node_name_mapping:
                    line = line.replace(f'"{old_name}"', f'"{node_name_mapping[old_name]}"')
                else:
                    # Try to find a similar function name
                    for func_name in function_names:
                        # Check for similarity (e.g., 'inputprocessor' vs 'process_input')
                        if old_name in func_name or func_name in old_name:
                            line = line.replace(f'"{old_name}"', f'"{func_name}"')
                            # Add to mapping for future references
                            node_name_mapping[old_name] = func_name
                            break

        # Add the line with proper indentation
        if line.startswith('graph.add_edge'):
            fixed_code.append(f'    {line}')
        elif line.startswith('graph.add_conditional_edges'):
            # Handle multi-line conditional edges
            fixed_code.append(f'    {line}')
            i += 1
            while i < len(sections['edges']) and not sections['edges'][i].endswith(')'):
                edge_line = sections['edges'][i]

                # Fix node names in the conditional edges
                node_names = re.findall(r'"([^"]+)"', edge_line)
                for old_name in node_names:
                    if old_name in function_names:
                        continue

                    # Check if we have a direct mapping
                    if old_name in node_name_mapping:
                        edge_line = edge_line.replace(f'"{old_name}"', f'"{node_name_mapping[old_name]}"')
                    else:
                        # Try to find a similar function name
                        for func_name in function_names:
                            # Check for similarity
                            if old_name in func_name or func_name in old_name:
                                edge_line = edge_line.replace(f'"{old_name}"', f'"{func_name}"')
                                # Add to mapping for future references
                                node_name_mapping[old_name] = func_name
                                break

                fixed_code.append(f'    {edge_line}')
                i += 1
            if i < len(sections['edges']):
                edge_line = sections['edges'][i]

                # Fix node names in the last line
                node_names = re.findall(r'"([^"]+)"', edge_line)
                for old_name in node_names:
                    if old_name in function_names:
                        continue

                    # Check if we have a direct mapping
                    if old_name in node_name_mapping:
                        edge_line = edge_line.replace(f'"{old_name}"', f'"{node_name_mapping[old_name]}"')
                    else:
                        # Try to find a similar function name
                        for func_name in function_names:
                            # Check for similarity
                            if old_name in func_name or func_name in old_name:
                                edge_line = edge_line.replace(f'"{old_name}"', f'"{func_name}"')
                                # Add to mapping for future references
                                node_name_mapping[old_name] = func_name
                                break

                fixed_code.append(f'    {edge_line}')
        elif line.startswith('# Conditional'):
            fixed_code.append(f'    {line}')
        else:
            fixed_code.append(f'    {line}')

        i += 1

    fixed_code.append('')

    # Add entry and finish points
    fixed_code.append('    # --- Entry and Finish ---')
    if sections['entry_finish']:
        for line in sections['entry_finish']:
            if line.startswith('graph.set_'):
                # Fix node names in entry/finish points
                node_names = re.findall(r'"([^"]+)"', line)
                for old_name in node_names:
                    if old_name in function_names:
                        continue

                    # Check if we have a direct mapping
                    if old_name in node_name_mapping:
                        line = line.replace(f'"{old_name}"', f'"{node_name_mapping[old_name]}"')
                    else:
                        # Try to find a similar function name
                        for func_name in function_names:
                            # Check for similarity
                            if old_name in func_name or func_name in old_name:
                                line = line.replace(f'"{old_name}"', f'"{func_name}"')
                                # Add to mapping for future references
                                node_name_mapping[old_name] = func_name
                                break
                fixed_code.append(f'    {line}')
    else:
        # Default entry and finish points - use first and last function names
        if function_names:
            fixed_code.append(f'    graph.set_entry_point("{function_names[0]}")')
            fixed_code.append(f'    graph.set_finish_point("{function_names[-1]}")')
        else:
            # Fallback to default names
            fixed_code.append('    graph.set_entry_point("process_input")')
            fixed_code.append('    graph.set_finish_point("format_output")')

    fixed_code.append('')

    # Add return statement
    fixed_code.append('    return graph.compile()')
    fixed_code.append('')

    # Add main block
    fixed_code.append('if __name__ == "__main__":')
    if sections['main'] and len(sections['main']) > 1:
        for line in sections['main'][1:]:
            fixed_code.append(f'    {line}')
    else:
        fixed_code.append('    app = create_graph()')
        fixed_code.append('    result = app.invoke({"input": "Test input"})')
        fixed_code.append('    print(result)')

    return '\n'.join(fixed_code)

def validate_and_fix_code(code: str) -> str:
    """
    Validate and fix the generated LangGraph code.

    Args:
        code: The Python code to validate and fix

    Returns:
        Fixed code

    Raises:
        LangGraphValidationError: If the code cannot be fixed
    """
    # First, try to fix common issues
    fixed_code = fix_common_issues(code)

    # Validate the fixed code
    is_valid, error = validate_python_syntax(fixed_code)

    if not is_valid:
        # If still invalid, try to fix indentation
        fixed_code = fix_indentation(fixed_code)
        is_valid, error = validate_python_syntax(fixed_code)

        if not is_valid:
            raise LangGraphValidationError(f"Failed to fix code: {error}")

    return fixed_code
