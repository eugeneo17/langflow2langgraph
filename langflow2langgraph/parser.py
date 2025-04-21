#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow JSON Parser
-------------------

This module handles parsing LangFlow JSON configurations and extracting nodes and edges.
"""

import json
import re
from typing import Dict, Tuple, List, Any, Optional
from pathlib import Path

class LangFlowParsingError(Exception):
    """Exception raised for errors during LangFlow JSON parsing."""
    pass

def load_langflow_json(json_path: str) -> Dict:
    """
    Load and validate a LangFlow JSON configuration file.
    
    Args:
        json_path: Path to the JSON file
        
    Returns:
        Dict containing the parsed JSON data
        
    Raises:
        LangFlowParsingError: If the file cannot be loaded or parsed
    """
    try:
        json_path = Path(json_path)
        if not json_path.exists():
            raise LangFlowParsingError(f"File not found: {json_path}")
            
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Basic validation
        if not isinstance(data, dict):
            raise LangFlowParsingError("Invalid JSON format: root must be an object")
            
        if "nodes" not in data:
            raise LangFlowParsingError("Invalid LangFlow JSON: 'nodes' field is required")
            
        return data
        
    except json.JSONDecodeError as e:
        raise LangFlowParsingError(f"Invalid JSON syntax: {str(e)}")
    except Exception as e:
        raise LangFlowParsingError(f"Error loading LangFlow JSON: {str(e)}")

def extract_nodes_and_edges(data: Dict) -> Tuple[Dict, List, Dict]:
    """
    Extract and validate nodes, edges, and state fields from LangFlow JSON.
    
    Args:
        data: Parsed LangFlow JSON data
        
    Returns:
        Tuple of (nodes, edges, state_fields)
        
    Raises:
        LangFlowParsingError: If the nodes or edges are invalid
    """
    try:
        nodes = {node["id"]: node for node in data.get("nodes", [])}
        edges = data.get("edges", [])
        
        # Validate node references in edges
        for edge in edges:
            if edge["source"] not in nodes:
                raise LangFlowParsingError(f"Invalid edge: source node '{edge['source']}' not found")
            if edge["target"] not in nodes:
                raise LangFlowParsingError(f"Invalid edge: target node '{edge['target']}' not found")
        
        # Extract state fields from node functions and edge conditions
        state_fields = extract_state_fields(nodes, edges)
                
        return nodes, edges, state_fields
        
    except KeyError as e:
        raise LangFlowParsingError(f"Invalid node/edge structure: {str(e)}")
    except Exception as e:
        raise LangFlowParsingError(f"Error extracting nodes and edges: {str(e)}")

def extract_state_fields(nodes: Dict, edges: List) -> Dict[str, str]:
    """
    Extract state fields from node functions and edge conditions with improved type inference.
    
    Args:
        nodes: Dictionary of nodes
        edges: List of edges
        
    Returns:
        Dictionary mapping field names to their types
    """
    state_fields = {
        "input": "str",  # Always include input
        "output": "dict"  # Always include output
    }
    
    # Extract fields from Python functions
    for node_id, node in nodes.items():
        # Extract from Python function code
        if "inputs" in node and "code" in node["inputs"]:
            code = node["inputs"]["code"]
            # Look for state assignments like state["field_name"] = value
            field_assignments = re.findall(r'state\[\"([^\"]+)\"\]\s*=\s*(.+?)(?:\n|$)', code)
            field_assignments.extend(re.findall(r"state\['([^']+)'\]\s*=\s*(.+?)(?:\n|$)", code))
            
            # Look for state accesses like if "field_name" in state:
            field_accesses = re.findall(r'if\s+\"([^\"]+)\"\s+in\s+state', code)
            field_accesses.extend(re.findall(r"if\s+'([^']+)'\s+in\s+state", code))
            
            # Look for return values like return {"decision": value}
            return_fields = re.findall(r'return\s+{\s*\"([^\"]+)\"\s*:\s*(.+?)(?:}|,)', code)
            return_fields.extend(re.findall(r"return\s+{\s*'([^']+)'\s*:\s*(.+?)(?:}|,)", code))
            
            # Process field assignments to infer types
            for field, value in field_assignments:
                if field in state_fields:
                    continue
                
                # Infer type from assignment value
                if re.search(r'\[\]|list\(\)|\[.+\]', value):
                    state_fields[field] = "list"
                elif re.search(r'{}|dict\(\)|{.+}', value):
                    state_fields[field] = "dict"
                elif re.search(r'True|False', value):
                    state_fields[field] = "bool"
                elif re.search(r'^\d+$', value.strip()):
                    state_fields[field] = "int"
                elif re.search(r'^\d+\.\d+$', value.strip()):
                    state_fields[field] = "float"
                else:
                    state_fields[field] = "str"
            
            # Process return values to infer types
            for field, value in return_fields:
                if field in state_fields:
                    continue
                
                # Infer type from return value
                if re.search(r'\[\]|list\(\)|\[.+\]', value):
                    state_fields[field] = "list"
                elif re.search(r'{}|dict\(\)|{.+}', value):
                    state_fields[field] = "dict"
                elif re.search(r'True|False', value):
                    state_fields[field] = "bool"
                elif re.search(r'^\d+$', value.strip()):
                    state_fields[field] = "int"
                elif re.search(r'^\d+\.\d+$', value.strip()):
                    state_fields[field] = "float"
                else:
                    state_fields[field] = "str"
            
            # Add remaining fields from accesses
            all_accesses = set(field_accesses)
            for field in all_accesses:
                if field not in state_fields:
                    # Try to infer type from usage patterns
                    if f"{field}.append" in code or f"{field}.extend" in code or f"{field}[" in code and not re.search(r'{0}\[\''.format(field), code):
                        state_fields[field] = "list"
                    elif f"{field}.get(" in code or f"{field}[" in code and re.search(r'{0}\[\''.format(field), code):
                        state_fields[field] = "dict"
                    elif f"{field} is True" in code or f"{field} is False" in code or f"not {field}" in code:
                        state_fields[field] = "bool"
                    elif f"{field} + " in code or f"{field} - " in code or f"{field} * " in code or f"{field} / " in code:
                        state_fields[field] = "float"
                    elif f"{field} += " in code or f"{field} -= " in code or f"len({field})" in code:
                        state_fields[field] = "int"
                    else:
                        state_fields[field] = "str"
        
        # Extract from node metadata and inputs
        class_path = node.get("class_path", "")
        if "LLM" in class_path:
            # LLM nodes typically produce a response
            state_fields["llm_response"] = "str"
        
        # Check for specific node types based on class_path
        if "TextSplitter" in class_path or "Splitter" in class_path:
            state_fields["chunks"] = "list"
        elif "Retriever" in class_path or "VectorStore" in class_path:
            state_fields["documents"] = "list"
        elif "Memory" in class_path:
            state_fields["history"] = "list"
        elif "Chain" in class_path:
            state_fields["chain_result"] = "str"
        elif "Tool" in class_path:
            state_fields["tool_result"] = "str"
        elif "Agent" in class_path:
            state_fields["agent_result"] = "str"
            state_fields["intermediate_steps"] = "list"
    
    # Extract fields from edge conditions
    for edge in edges:
        if "data" in edge and "condition" in edge["data"]:
            condition = edge["data"]["condition"]
            # Extract field name from conditions like "field == 'value'"
            try:
                field_matches = re.findall(r'(\w+)\s*==\s*[\'"]([^\'"]*)[\'"]', condition)
                for field, value in field_matches:
                    if field not in state_fields:
                        # Try to infer type from the condition value
                        if value.lower() in ["true", "false"]:
                            state_fields[field] = "bool"
                        elif value.isdigit():
                            state_fields[field] = "int"
                        elif re.match(r'^\d+\.\d+$', value):
                            state_fields[field] = "float"
                        else:
                            state_fields[field] = "str"
            except Exception as e:
                # If regex fails, try a simpler approach
                if "==" in condition:
                    parts = condition.split("==")
                    if len(parts) >= 2:
                        field = parts[0].strip()
                        if field and field.isalnum() and field not in state_fields:
                            state_fields[field] = "str"
    
    return state_fields
