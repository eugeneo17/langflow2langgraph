#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow to LangGraph Converter
-------------------------------

This module contains the core functionality for converting LangFlow JSON exports
into LangGraph Python code.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple, List, Any

# Import node mappings if available
try:
    from langflow2langgraph.mapping import generate_node_code, get_state_fields_for_node, convert_edge_condition
    HAS_NODE_MAPPINGS = True
except ImportError:
    HAS_NODE_MAPPINGS = False

# Import validator if available
try:
    from langflow2langgraph.validator import validate_code, fix_common_issues
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False

# Import other modules
from langflow2langgraph.parser import load_langflow_json, extract_nodes_and_edges, LangFlowParsingError
from langflow2langgraph.code_generator import generate_imports, generate_state_class, generate_function_header, generate_node_function, generate_main_block, generate_return_statement
from langflow2langgraph.edge_handler import process_edges, generate_entry_finish_points


class LangGraphConversionError(Exception):
    """Custom exception for conversion errors"""
    pass

def generate_langgraph_code(nodes: Dict, edges: List, state_fields: Dict[str, str]) -> str:
    """
    Generate LangGraph Python code from nodes and edges.

    Args:
        nodes: Dictionary of node definitions
        edges: List of edge definitions
        state_fields: Dictionary of state fields and their types

    Returns:
        String containing the generated Python code

    Raises:
        LangGraphConversionError: If there's an error during code generation
    """
    try:
        # Generate clean node names
        node_names = {}
        for node_id, node in nodes.items():
            label = node.get("data", {}).get("label", f"Node_{node_id}")
            # Clean label for Python function name
            clean_label = ''.join(c if c.isalnum() else '_' for c in label).lower()
            if clean_label[0].isdigit():
                clean_label = 'f_' + clean_label
            node_names[node_id] = clean_label

        # Start building the code
        code_lines = []

        # Add imports
        code_lines.extend(generate_imports())

        # Add state class definition
        code_lines.extend(generate_state_class(state_fields))

        # Add function header
        code_lines.extend(generate_function_header())

        # Add node functions
        for node_id, node in nodes.items():
            clean_label = node_names.get(node_id)
            node_code_lines = generate_node_function(clean_label, node, HAS_NODE_MAPPINGS)
            code_lines.extend(node_code_lines)

        # Add edges
        edge_code_lines = process_edges(edges, node_names, HAS_NODE_MAPPINGS)
        code_lines.extend(edge_code_lines)

        # Add entry and finish points
        entry_finish_lines = generate_entry_finish_points(node_names)
        code_lines.extend(entry_finish_lines)

        # Add return statement
        code_lines.extend(generate_return_statement())

        # Add main block
        code_lines.extend(generate_main_block())

        return "\n".join(code_lines)
    except Exception as e:
        raise LangGraphConversionError(f"Error generating code: {str(e)}")


def convert_langflow_to_langgraph(json_path: str, output_path: Optional[str] = None, validate: bool = True) -> str:
    """
    Convert LangFlow JSON to LangGraph code with error handling and validation

    Args:
        json_path: Path to the LangFlow JSON file
        output_path: Optional path to save the generated code
        validate: Whether to validate and fix the generated code

    Returns:
        The generated Python code as a string

    Raises:
        LangGraphConversionError: If there's an error during conversion
    """
    try:
        data = load_langflow_json(json_path)
        nodes, edges, state_fields = extract_nodes_and_edges(data)
        langgraph_code = generate_langgraph_code(nodes, edges, state_fields)

        # Validate and fix code if validator is available
        if validate and HAS_VALIDATOR:
            # First try to fix common issues
            langgraph_code = fix_common_issues(langgraph_code)

            # Then validate the code
            is_valid, errors = validate_code(langgraph_code)
            if not is_valid:
                error_msg = "\n".join([f"- {error}" for error in errors])
                print(f"Warning: Generated code has validation issues:\n{error_msg}")
                print("Attempting to fix issues automatically...")

                # Try to fix issues again after validation
                langgraph_code = fix_common_issues(langgraph_code)

        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(langgraph_code, encoding='utf-8')

        return langgraph_code

    except Exception as e:
        raise LangGraphConversionError(f"Conversion failed: {str(e)}")
