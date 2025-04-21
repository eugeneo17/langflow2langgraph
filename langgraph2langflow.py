# LangFlow to LangGraph Converter (Simplified Prototype)

import json
import os
from typing import Dict, Tuple
from pathlib import Path

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

        return nodes, edges
    except KeyError as e:
        raise LangGraphConversionError(f"Invalid node/edge structure: {str(e)}")

# --- Step 3: Create LangGraph Python Code ---
def generate_langgraph_code(nodes: Dict, edges: list) -> str:
    """Generate LangGraph code with improved formatting and validation"""
    try:
        code_lines = [
            "from langgraph.graph import StateGraph",
            "from typing import TypedDict, Annotated",
            "",
            "# Define the state schema",
            "class GraphState(TypedDict):",
            "    input: str",
            "    processed_input: str",
            "    llm_response: str",
            "    output: str",
            "",
            "def create_graph():",
            "    # Define the graph with proper state schema",
            "    graph = StateGraph(GraphState)",
            "",
            "    # --- Node Functions ---"
        ]

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
                # Handle different node types appropriately
                if "LLM" in class_path:
                    code_lines.extend([
                        f"    def {clean_label}(state):",
                        f"        # TODO: implement logic from class {class_path}",
                        f"        # For testing purposes, add a mock LLM response",
                        f"        if \"processed_input\" in state:",
                        f"            state[\"llm_response\"] = f\"Processed: {{state['processed_input']}}\"",
                        f"        return state",
                        f"    graph.add_node(\"{clean_label}\", {clean_label})"
                    ])
                else:
                    code_lines.extend([
                        f"    def {clean_label}(state):",
                        f"        # TODO: implement logic from class {class_path}",
                        f"        return state",
                        f"    graph.add_node(\"{clean_label}\", {clean_label})"
                    ])
            code_lines.append("")

        code_lines.append("    # --- Edges ---")
        for edge in edges:
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
def convert_langflow_to_langgraph(json_path: str, output_path: str = None) -> str:
    """Convert LangFlow JSON to LangGraph code with error handling"""
    try:
        data = load_langflow_json(json_path)
        nodes, edges = extract_nodes_and_edges(data)
        langgraph_code = generate_langgraph_code(nodes, edges)

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
