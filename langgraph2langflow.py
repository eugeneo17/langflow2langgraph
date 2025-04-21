# LangFlow to LangGraph Converter (Simplified Prototype)

import json
import os
import re
from typing import Dict, Tuple, List, Any
from pathlib import Path

# Import node mappings if available, otherwise use a fallback
try:
    from langflow2langgraph.node_mappings import generate_node_code, get_node_type
    HAS_NODE_MAPPINGS = True
except ImportError:
    HAS_NODE_MAPPINGS = False

# Import validator if available
try:
    from langflow2langgraph.validator import validate_code, fix_common_issues
    HAS_VALIDATOR = True
except ImportError:
    HAS_VALIDATOR = False

class LangGraphConversionError(Exception):
    """Custom exception for conversion errors"""
    pass

# --- Step 1: Load LangFlow JSON ---
def load_langflow_json(path: str) -> Dict:
    """Load and validate LangFlow JSON file"""
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"JSON file not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Basic validation
        if not isinstance(data, dict):
            raise ValueError("Invalid JSON format: root must be an object")
        if "nodes" not in data or "edges" not in data:
            raise ValueError("Invalid JSON format: missing 'nodes' or 'edges'")

        return data
    except json.JSONDecodeError as e:
        raise LangGraphConversionError(f"Invalid JSON syntax: {str(e)}")
    except Exception as e:
        raise LangGraphConversionError(f"Error loading JSON: {str(e)}")

# --- Step 2: Extract Node Definitions ---
def extract_nodes_and_edges(data: Dict) -> Tuple[Dict, list]:
    """Extract and validate nodes and edges"""
    try:
        nodes = {node["id"]: node for node in data.get("nodes", [])}
        edges = data.get("edges", [])

        # Validate node references in edges
        for edge in edges:
            if edge["source"] not in nodes:
                raise ValueError(f"Invalid edge: source node '{edge['source']}' not found")
            if edge["target"] not in nodes:
                raise ValueError(f"Invalid edge: target node '{edge['target']}' not found")

        # Extract state fields from node functions
        state_fields = extract_state_fields(nodes, edges)

        return nodes, edges, state_fields
    except KeyError as e:
        raise LangGraphConversionError(f"Invalid node/edge structure: {str(e)}")

def extract_state_fields(nodes: Dict, edges: list) -> Dict:
    """Extract state fields from node functions and edge conditions with improved type inference"""
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
            field_assignments = re.findall(r'state\["([^"]+)"\]\s*=\s*(.+?)(?:\n|$)', code)
            field_assignments.extend(re.findall(r"state\['([^']+)'\]\s*=\s*(.+?)(?:\n|$)", code))

            # Look for state accesses like if "field_name" in state:
            field_accesses = re.findall(r'if\s+"([^"]+)"\s+in\s+state', code)
            field_accesses.extend(re.findall(r"if\s+'([^']+)'\s+in\s+state", code))

            # Look for return values like return {"decision": value}
            return_fields = re.findall(r'return\s+{\s*"([^"]+)"\s*:\s*(.+?)(?:}|,)', code)
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
            field_matches = re.findall(r'(\w+)\s*==\s*["\']([^"\']*)["\'](.*)', condition)
            for field, value, _ in field_matches:
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

    return state_fields

# --- Step 3: Create LangGraph Python Code ---
def generate_langgraph_code(nodes: Dict, edges: list, state_fields: Dict) -> str:
    """Generate LangGraph code with improved formatting and validation"""
    try:
        code_lines = [
            "from langgraph.graph import StateGraph",
            "from typing import TypedDict, Annotated, List, Dict, Any",
            "",
            "# Define the state schema",
            "class GraphState(TypedDict):"
        ]

        # Add state fields with their types
        for field, field_type in state_fields.items():
            if field_type == "list":
                code_lines.append(f"    {field}: List[Any]")
            elif field_type == "dict":
                code_lines.append(f"    {field}: Dict[str, Any]")
            elif field_type == "int":
                code_lines.append(f"    {field}: int")
            elif field_type == "bool":
                code_lines.append(f"    {field}: bool")
            else:  # Default to string
                code_lines.append(f"    {field}: str")

        code_lines.extend([
            "",
            "def create_graph():",
            "    # Define the graph with proper state schema",
            "    graph = StateGraph(GraphState)",
            "",
            "    # --- Node Functions ---"
        ])

        node_names = {}

        for node_id, node in nodes.items():
            class_path = node.get("class_path", "")
            label = node.get("data", {}).get("label", f"Node_{node_id}")
            # Clean label for Python function name
            clean_label = ''.join(c if c.isalnum() else '_' for c in label).lower()
            if clean_label[0].isdigit():
                clean_label = 'f_' + clean_label

            node_names[node_id] = clean_label

            if class_path.endswith("PythonFunction") and "code" in node.get("inputs", {}):
                func_code = node["inputs"]["code"].strip()
                # Fix indentation in the function code
                func_lines = func_code.split('\n')
                fixed_func_lines = []
                for line in func_lines:
                    if line.startswith('def '):
                        fixed_func_lines.append(f"    {line}")
                    else:
                        fixed_func_lines.append(f"        {line}")
                fixed_func_code = '\n'.join(fixed_func_lines)
                code_lines.append(fixed_func_code)
                func_name = func_code.split('def ')[1].split('(')[0].strip()
                code_lines.append(f"    graph.add_node(\"{clean_label}\", {func_name})")
            else:
                # Use node mappings if available
                if HAS_NODE_MAPPINGS:
                    # Import is done at runtime to avoid circular imports
                    from langflow2langgraph.node_mappings import generate_node_code
                    node_code_lines = generate_node_code(node, clean_label)
                    code_lines.extend(node_code_lines)
                    code_lines.append(f"    graph.add_node(\"{clean_label}\", {clean_label})")
                else:
                    # Fallback to basic implementation
                    if "LLM" in class_path:
                        # Find the most likely input fields for this LLM node
                        input_fields = [field for field in state_fields.keys()
                                      if field != "output" and field != "llm_response"]

                        # Prioritize fields based on naming patterns
                        primary_input_field = "input"  # Default
                        secondary_input_fields = []

                        # First priority: fields with input-related names
                        for field in input_fields:
                            if field == "input":
                                continue  # Skip the default input field
                            if field.endswith("_input") or "text" in field or "content" in field or "message" in field or "query" in field:
                                primary_input_field = field
                                break

                        # Second priority: processed_input or similar
                        if primary_input_field == "input" and "processed_input" in input_fields:
                            primary_input_field = "processed_input"

                        # Collect other potential input fields
                        for field in input_fields:
                            if field != primary_input_field and field != "input":
                                secondary_input_fields.append(field)

                        # Get prompt template if available
                        prompt_template = node.get("inputs", {}).get("prompt_template", "")

                        # If no prompt template, create a default one
                        if not prompt_template:
                            prompt_template = f"Process this: {{{{{primary_input_field}}}}}"

                        # Extract template variables
                        template_vars = re.findall(r'{([^{}]+)}', prompt_template)

                        # Generate the LLM function
                        code_lines.append(f"    def {clean_label}(state):")
                        code_lines.append(f"        # TODO: implement logic from class {class_path}")
                        code_lines.append(f"        # For testing purposes, add a mock LLM response")

                        # Check if primary input is available
                        code_lines.append(f"        if \"{primary_input_field}\" in state:")

                        # Format the prompt template
                        if template_vars:
                            # Handle template variables
                            code_lines.append(f"            # Format prompt template with variables")
                            code_lines.append(f"            prompt = f\"{prompt_template}\"")

                            # Generate mock response based on the template
                            code_lines.append(f"            state[\"llm_response\"] = f\"Response to: {{prompt}}\"")
                        else:
                            # Simple response using primary input
                            code_lines.append(f"            state[\"llm_response\"] = f\"Processed: {{state['{primary_input_field}']}}\"")

                        # Add fallbacks for other potential inputs
                        if secondary_input_fields:
                            for field in secondary_input_fields[:2]:  # Limit to 2 fallbacks for simplicity
                                code_lines.append(f"        elif \"{field}\" in state:")
                                code_lines.append(f"            state[\"llm_response\"] = f\"Processed: {{state['{field}']}}\"")

                        # Default case
                        code_lines.append(f"        else:")
                        code_lines.append(f"            state[\"llm_response\"] = \"No input provided\"")

                        code_lines.append(f"        return state")
                        code_lines.append(f"    graph.add_node(\"{clean_label}\", {clean_label})")
                    else:
                        code_lines.extend([
                            f"    def {clean_label}(state):",
                            f"        # TODO: implement logic from class {class_path}",
                            f"        return state",
                            f"    graph.add_node(\"{clean_label}\", {clean_label})"
                        ])
            code_lines.append("")

        # Group edges by source to identify conditional branches
        edges_by_source = {}
        for edge in edges:
            source = edge["source"]
            if source not in edges_by_source:
                edges_by_source[source] = []
            edges_by_source[source].append(edge)

        code_lines.append("    # --- Edges ---")

        # Process edges, looking for conditional branches
        for source, source_edges in edges_by_source.items():
            src = node_names.get(source)

            # Check if these edges have conditions
            conditional_edges = [e for e in source_edges if "data" in e and "condition" in e["data"]]

            if len(conditional_edges) > 0 and len(conditional_edges) == len(source_edges):
                # All edges from this source have conditions - use conditional_edges
                # First, identify the condition fields
                conditions = [e["data"]["condition"] for e in conditional_edges]

                # Try to identify common patterns in conditions
                eq_field_matches = set()
                for condition in conditions:
                    matches = re.findall(r'(\w+)\s*==\s*["\']', condition)
                    eq_field_matches.update(matches)

                # Check for other comparison operators
                comp_field_matches = set()
                for condition in conditions:
                    matches = re.findall(r'(\w+)\s*(?:>|<|>=|<=|!=)\s*', condition)
                    comp_field_matches.update(matches)

                # Check for function calls like len(field) or field.startswith
                func_field_matches = set()
                for condition in conditions:
                    matches = re.findall(r'(\w+)\.(\w+)\(', condition)  # method calls
                    for field, _ in matches:
                        func_field_matches.add(field)
                    matches = re.findall(r'(\w+)\s*\(\s*(\w+)', condition)  # function calls
                    for func, field in matches:
                        if func != 'len':
                            continue
                        func_field_matches.add(field)

                # Check for logical operators
                has_logical_ops = any(re.search(r'\s+(?:and|or|not)\s+', condition) for condition in conditions)

                # Determine the best approach for handling these conditions
                if len(eq_field_matches) == 1 and not comp_field_matches and not func_field_matches and not has_logical_ops:
                    # Simple equality conditions on a single field - use conditional_edges
                    field = list(eq_field_matches)[0]

                    # Extract the values for each target
                    routes = {}
                    for edge in conditional_edges:
                        target = node_names.get(edge["target"])
                        condition = edge["data"]["condition"]
                        value_match = re.search(f"{field}\\s*==\\s*[\"']([^\"']+)[\"']", condition)
                        if value_match:
                            value = value_match.group(1)
                            routes[value] = target

                    # Generate conditional edges code
                    code_lines.append(f"")
                    code_lines.append(f"    # Conditional routing based on {field}")
                    code_lines.append(f"    graph.add_conditional_edges(")
                    code_lines.append(f"        \"{src}\",")
                    code_lines.append(f"        lambda state: state.get(\"{field}\", \"\"),")
                    code_lines.append(f"        {{")

                    for value, target in routes.items():
                        code_lines.append(f"            \"{value}\": \"{target}\",")

                    code_lines.append(f"        }}")
                    code_lines.append(f"    )")
                elif len(eq_field_matches) > 0 or len(comp_field_matches) > 0 or len(func_field_matches) > 0:
                    # More complex conditions - use a router function
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
                else:
                    # Fallback to regular edges with comments
                    for edge in source_edges:
                        src = node_names.get(edge["source"])
                        tgt = node_names.get(edge["target"])
                        condition = edge["data"].get("condition", "")
                        code_lines.append(f"    # Condition: {condition}")
                        code_lines.append(f"    graph.add_edge(\"{src}\", \"{tgt}\")")
            else:
                # Regular edges
                for edge in source_edges:
                    src = node_names.get(edge["source"])
                    tgt = node_names.get(edge["target"])
                    code_lines.append(f"    graph.add_edge(\"{src}\", \"{tgt}\")")

        code_lines.extend([
            "",
            "    # --- Entry and Finish ---",
            f"    graph.set_entry_point(\"{list(node_names.values())[0]}\")",
            f"    graph.set_finish_point(\"{list(node_names.values())[-1]}\")",
            "",
            "    return graph.compile()",
            "",
            "if __name__ == \"__main__\":",
            "    app = create_graph()",
            "    result = app.invoke({\"input\": \"Test input\"})",
            "    print(result)"
        ])

        return "\n".join(code_lines)
    except Exception as e:
        raise LangGraphConversionError(f"Error generating code: {str(e)}")

# --- Step 4: Main Function ---
def convert_langflow_to_langgraph(json_path: str, output_path: str = None, validate: bool = True) -> str:
    """Convert LangFlow JSON to LangGraph code with error handling and validation"""
    try:
        data = load_langflow_json(json_path)
        nodes, edges, state_fields = extract_nodes_and_edges(data)
        langgraph_code = generate_langgraph_code(nodes, edges, state_fields)

        # Validate and fix code if validator is available
        if validate and HAS_VALIDATOR:
            # Import is done at runtime to avoid circular imports
            from langflow2langgraph.validator import validate_code, fix_common_issues

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

if __name__ == "__main__":
    try:
        # Use a default example file if none provided
        example_path = "examples/sample_flow.json"
        output_path = "generated_graph.py"

        result = convert_langflow_to_langgraph(example_path, output_path)
        print(f"Successfully converted {example_path} to {output_path}")
        print("\nGenerated code:")
        print("-" * 40)
        print(result)

    except LangGraphConversionError as e:
        print(f"Error: {str(e)}")
        exit(1)
