#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangGraph Edge Handler
---------------------

This module handles processing and generating code for edges in LangGraph.
"""

import re
from typing import Dict, List, Any, Set, Tuple

class EdgeProcessingError(Exception):
    """Exception raised for errors during edge processing."""
    pass

def process_edges(edges: List[Dict[str, Any]], node_names: Dict[str, str], has_node_mappings: bool) -> List[str]:
    """
    Process edges and generate code for LangGraph.
    
    Args:
        edges: List of edges from LangFlow
        node_names: Dictionary mapping node IDs to clean names
        has_node_mappings: Whether node mappings are available
        
    Returns:
        List of code lines for edges
    """
    code_lines = ["    # --- Edges ---"]
    
    # Group edges by source to identify conditional branches
    edges_by_source = {}
    for edge in edges:
        source = edge["source"]
        if source not in edges_by_source:
            edges_by_source[source] = []
        edges_by_source[source].append(edge)
    
    # Process edges, looking for conditional branches
    for source, source_edges in edges_by_source.items():
        src = node_names.get(source)
        
        # Check if these edges have conditions
        conditional_edges = [e for e in source_edges if "data" in e and "condition" in e["data"]]
        
        if len(conditional_edges) > 0 and len(conditional_edges) == len(source_edges):
            # All edges from this source have conditions - use conditional_edges
            process_conditional_edges(conditional_edges, src, node_names, code_lines, has_node_mappings)
        else:
            # Regular edges
            for edge in source_edges:
                src = node_names.get(edge["source"])
                tgt = node_names.get(edge["target"])
                code_lines.append(f"    graph.add_edge(\"{src}\", \"{tgt}\")")
    
    return code_lines

def process_conditional_edges(
    conditional_edges: List[Dict[str, Any]], 
    src: str, 
    node_names: Dict[str, str], 
    code_lines: List[str],
    has_node_mappings: bool
) -> None:
    """
    Process conditional edges and generate appropriate code.
    
    Args:
        conditional_edges: List of edges with conditions
        src: Source node name
        node_names: Dictionary mapping node IDs to clean names
        code_lines: List to append code lines to
        has_node_mappings: Whether node mappings are available
    """
    # First, identify the condition fields
    conditions = [e["data"]["condition"] for e in conditional_edges]
    
    # Try to identify common patterns in conditions
    eq_field_matches = extract_equality_fields(conditions)
    comp_field_matches = extract_comparison_fields(conditions)
    func_field_matches = extract_function_fields(conditions)
    has_logical_ops = any(re.search(r'\s+(?:and|or|not)\s+', condition) for condition in conditions)
    
    # Determine the best approach for handling these conditions
    if len(eq_field_matches) == 1 and not comp_field_matches and not func_field_matches and not has_logical_ops:
        # Simple equality conditions on a single field - use conditional_edges
        handle_simple_equality_conditions(
            conditional_edges, src, node_names, code_lines, eq_field_matches, has_node_mappings
        )
    elif len(eq_field_matches) > 0 or len(comp_field_matches) > 0 or len(func_field_matches) > 0:
        # More complex conditions - use a router function
        handle_complex_conditions(
            conditional_edges, src, node_names, code_lines, 
            eq_field_matches, comp_field_matches, func_field_matches, has_node_mappings
        )
    else:
        # Fallback to regular edges with comments
        for edge in conditional_edges:
            src = node_names.get(edge["source"])
            tgt = node_names.get(edge["target"])
            condition = edge["data"].get("condition", "")
            code_lines.append(f"    # Condition: {condition}")
            code_lines.append(f"    graph.add_edge(\"{src}\", \"{tgt}\")")

def extract_equality_fields(conditions: List[str]) -> Set[str]:
    """
    Extract field names used in equality conditions.
    
    Args:
        conditions: List of condition strings
        
    Returns:
        Set of field names
    """
    eq_field_matches = set()
    for condition in conditions:
        matches = re.findall(r'(\w+)\s*==\s*["\']', condition)
        eq_field_matches.update(matches)
    return eq_field_matches

def extract_comparison_fields(conditions: List[str]) -> Set[str]:
    """
    Extract field names used in comparison conditions.
    
    Args:
        conditions: List of condition strings
        
    Returns:
        Set of field names
    """
    comp_field_matches = set()
    for condition in conditions:
        matches = re.findall(r'(\w+)\s*(?:>|<|>=|<=|!=)\s*', condition)
        comp_field_matches.update(matches)
    return comp_field_matches

def extract_function_fields(conditions: List[str]) -> Set[str]:
    """
    Extract field names used in function calls.
    
    Args:
        conditions: List of condition strings
        
    Returns:
        Set of field names
    """
    func_field_matches = set()
    for condition in conditions:
        # Method calls like field.startswith()
        matches = re.findall(r'(\w+)\.(\w+)\(', condition)
        for field, _ in matches:
            func_field_matches.add(field)
        
        # Function calls like len(field)
        matches = re.findall(r'(\w+)\s*\(\s*(\w+)', condition)
        for func, field in matches:
            if func != 'len':
                continue
            func_field_matches.add(field)
    
    return func_field_matches

def handle_simple_equality_conditions(
    conditional_edges: List[Dict[str, Any]], 
    src: str, 
    node_names: Dict[str, str], 
    code_lines: List[str],
    eq_field_matches: Set[str],
    has_node_mappings: bool
) -> None:
    """
    Handle simple equality conditions and generate code.
    
    Args:
        conditional_edges: List of edges with conditions
        src: Source node name
        node_names: Dictionary mapping node IDs to clean names
        code_lines: List to append code lines to
        eq_field_matches: Set of field names used in equality conditions
        has_node_mappings: Whether node mappings are available
    """
    field = list(eq_field_matches)[0]
    
    # Extract the values for each target
    routes = {}
    for edge in conditional_edges:
        target = node_names.get(edge["target"])
        condition = edge["data"]["condition"]
        
        # Use the mapping function if available
        if has_node_mappings:
            from langflow2langgraph.mapping import convert_edge_condition
            edge_condition = convert_edge_condition(condition)
            # For simple equality conditions, extract the value for routing
            value_match = re.search(f"{field}\\s*==\\s*[\"']([^\"']+)[\"']", condition)
            if value_match:
                value = value_match.group(1)
                routes[value] = target
        else:
            # Default implementation
            value_match = re.search(f"{field}\\s*==\\s*[\"']([^\"']+)[\"']", condition)
            if value_match:
                value = value_match.group(1)
                routes[value] = target
    
    # Generate conditional edges code
    code_lines.append(f"")
    code_lines.append(f"    # Conditional routing based on {field}")
    code_lines.append(f"    graph.add_conditional_edges(")
    code_lines.append(f"        \"{src}\",")
    
    if has_node_mappings and 'edge_condition' in locals():
        # Use the converted condition
        code_lines.append(f"        {edge_condition},")
    else:
        # Default implementation
        code_lines.append(f"        lambda state: state.get(\"{field}\", \"\"),")
    
    code_lines.append(f"        {{")
    
    for value, target in routes.items():
        code_lines.append(f"            \"{value}\": \"{target}\",")
    
    code_lines.append(f"        }}")
    code_lines.append(f"    )")

def handle_complex_conditions(
    conditional_edges: List[Dict[str, Any]], 
    src: str, 
    node_names: Dict[str, str], 
    code_lines: List[str],
    eq_field_matches: Set[str],
    comp_field_matches: Set[str],
    func_field_matches: Set[str],
    has_node_mappings: bool
) -> None:
    """
    Handle complex conditions and generate router function code.
    
    Args:
        conditional_edges: List of edges with conditions
        src: Source node name
        node_names: Dictionary mapping node IDs to clean names
        code_lines: List to append code lines to
        eq_field_matches: Set of field names used in equality conditions
        comp_field_matches: Set of field names used in comparison conditions
        func_field_matches: Set of field names used in function calls
        has_node_mappings: Whether node mappings are available
    """
    # Collect all fields used in conditions
    all_fields = set()
    all_fields.update(eq_field_matches)
    all_fields.update(comp_field_matches)
    all_fields.update(func_field_matches)
    
    # Generate a router function
    router_name = f"{src}_router"
    code_lines.append(f"")
    code_lines.append(f"    # Complex conditional routing from {src}")
    code_lines.append(f"    def {router_name}(state):")
    
    # Add condition checks
    for i, edge in enumerate(conditional_edges):
        target = node_names.get(edge["target"])
        condition = edge["data"]["condition"]
        
        # Use the mapping function if available
        if has_node_mappings:
            from langflow2langgraph.mapping import convert_edge_condition
            condition = convert_edge_condition(condition).replace("lambda state: ", "")
        else:
            # Clean up the condition for Python
            # Replace field references with state.get calls
            for field in all_fields:
                condition = re.sub(f"\\b{field}\\b", f"state.get('{field}')", condition)
        
        if i == 0:
            code_lines.append(f"        if {condition}:")
        else:
            code_lines.append(f"        elif {condition}:")
        
        code_lines.append(f"            return \"{target}\"")
    
    # Default case
    if conditional_edges:
        default_target = node_names.get(conditional_edges[-1]["target"])
        code_lines.append(f"        else:")
        code_lines.append(f"            return \"{default_target}\"")
    
    # Add the router node and edges
    code_lines.append(f"")
    code_lines.append(f"    graph.add_node(\"{router_name}\", {router_name})")
    code_lines.append(f"    graph.add_edge(\"{src}\", \"{router_name}\")")
    
    # Add conditional edges from router to targets
    targets = set(node_names.get(edge["target"]) for edge in conditional_edges)
    for target in targets:
        code_lines.append(f"    graph.add_conditional_edges(")
        code_lines.append(f"        \"{router_name}\",")
        code_lines.append(f"        lambda state: {router_name}(state),")
        code_lines.append(f"        {{\"{target}\": \"{target}\"}}")
        code_lines.append(f"    )")

def generate_entry_finish_points(node_names: Dict[str, str]) -> List[str]:
    """
    Generate code for entry and finish points.
    
    Args:
        node_names: Dictionary mapping node IDs to clean names
        
    Returns:
        List of code lines for entry and finish points
    """
    node_values = list(node_names.values())
    if not node_values:
        return []
    
    lines = [
        "",
        "    # --- Entry and Finish ---",
        f"    graph.add_edge(START, \"{node_values[0]}\")",
        f"    graph.add_edge(\"{node_values[-1]}\", END)"
    ]
    
    return lines
