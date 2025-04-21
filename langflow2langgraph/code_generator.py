#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangGraph Code Generator
-----------------------

This module handles generating LangGraph Python code from parsed LangFlow nodes and edges.
"""

import re
from typing import Dict, List, Any, Optional

class CodeGenerationError(Exception):
    """Exception raised for errors during code generation."""
    pass

def generate_imports() -> List[str]:
    """
    Generate import statements for LangGraph code.

    Returns:
        List of import statement lines
    """
    return [
        "from langgraph.graph import StateGraph",
        "from typing import TypedDict, List, Dict, Any",
        ""
    ]

def generate_state_class(state_fields: Dict[str, str]) -> List[str]:
    """
    Generate the GraphState TypedDict class definition.

    Args:
        state_fields: Dictionary mapping field names to their types

    Returns:
        List of code lines for the class definition
    """
    lines = ["class GraphState(TypedDict):"]

    # Add fields with type annotations
    for field, field_type in state_fields.items():
        # Convert Python types to TypedDict annotation syntax
        if field_type == "str":
            lines.append(f"    {field}: str")
        elif field_type == "int":
            lines.append(f"    {field}: int")
        elif field_type == "float":
            lines.append(f"    {field}: float")
        elif field_type == "bool":
            lines.append(f"    {field}: bool")
        elif field_type == "list":
            lines.append(f"    {field}: List[Any]")
        elif field_type == "dict":
            lines.append(f"    {field}: Dict[str, Any]")
        else:
            lines.append(f"    {field}: Any")

    lines.append("")
    return lines

def generate_function_header() -> List[str]:
    """
    Generate the create_graph function header.

    Returns:
        List of code lines for the function header
    """
    return [
        "def create_graph():",
        "    # Define the graph with proper state schema",
        "    graph = StateGraph(GraphState)",
        ""
    ]

def generate_node_function(node_name: str, node_data: Dict[str, Any], has_node_mappings: bool) -> List[str]:
    """
    Generate a node function for a LangGraph node.

    Args:
        node_name: The name of the node
        node_data: The node data from LangFlow
        has_node_mappings: Whether node mappings are available

    Returns:
        List of code lines for the node function
    """
    lines = []

    # Check if the node has custom code
    if "inputs" in node_data and "code" in node_data["inputs"]:
        # Use the custom code
        func_code = node_data["inputs"]["code"]

        # Extract function name and signature
        func_match = re.search(r'def\s+(\w+)\s*\([^)]*\):', func_code)
        if func_match:
            func_name = func_match.group(1)

            # Format the function code with proper indentation
            fixed_func_lines = []
            for line in func_code.split('\n'):
                if line.startswith('def '):
                    fixed_func_lines.append(f"    {line}")
                else:
                    fixed_func_lines.append(f"        {line}")

            lines.extend(fixed_func_lines)
            lines.append(f"    graph.add_node(\"{node_name}\", {func_name})")
        else:
            # If no function definition found, create a wrapper
            lines.append(f"    def {node_name}(state):")
            lines.append(f"        # Custom code")
            for code_line in func_code.split('\n'):
                lines.append(f"        {code_line}")
            lines.append(f"        return state")
            lines.append(f"    graph.add_node(\"{node_name}\", {node_name})")
    else:
        # Use node mappings if available
        if has_node_mappings:
            # Import is done at runtime to avoid circular imports
            from langflow2langgraph.mapping import generate_node_code, get_state_fields_for_node

            # Get node-specific state fields
            node_state_fields = get_state_fields_for_node(node_data)

            # Generate code for this node
            node_code = generate_node_code(node_name, node_data)

            # Format the code and add it to lines
            # Check if the code already has the function definition
            code_lines = node_code.strip().split('\n')
            if code_lines and code_lines[0].strip().startswith('def '):
                # Remove the function definition line
                func_def = code_lines[0].strip()
                # Extract just the function name
                func_name_match = re.search(r'def\s+(\w+)\s*\(', func_def)
                if func_name_match:
                    func_name = func_name_match.group(1)
                    # Add our own function definition
                    lines.append(f"    def {node_name}(state):")
                    # Add the rest of the lines with proper indentation
                    for line in code_lines[1:]:
                        if line.strip():
                            lines.append(f"        {line.strip()}")
                else:
                    # Fallback if we can't extract the function name
                    for line in code_lines:
                        if line.strip():
                            lines.append(f"    {line.strip()}")
            else:
                # No function definition, just add the lines
                for line in code_lines:
                    if line.strip():
                        lines.append(f"    {line.strip()}")

            lines.append(f"    graph.add_node(\"{node_name}\", {node_name})")
        else:
            # Fallback to basic implementation
            class_path = node_data.get("class_path", "")
            lines.append(f"    def {node_name}(state):")
            lines.append(f"        # TODO: implement logic from class {class_path}")
            lines.append(f"        return state")
            lines.append(f"    graph.add_node(\"{node_name}\", {node_name})")

    lines.append("")
    return lines

def generate_main_block() -> List[str]:
    """
    Generate the main block for the LangGraph code.

    Returns:
        List of code lines for the main block
    """
    return [
        "if __name__ == \"__main__\":",
        "    app = create_graph()",
        "    result = app.invoke({\"input\": \"Test input\"})",
        "    print(result)"
    ]

def generate_return_statement() -> List[str]:
    """
    Generate the return statement for the create_graph function.

    Returns:
        List of code lines for the return statement
    """
    return [
        "",
        "    return graph.compile()",
        ""
    ]
