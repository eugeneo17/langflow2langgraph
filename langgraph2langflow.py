# LangFlow to LangGraph Converter (Simplified Prototype)

import json
from typing import Dict

# --- Step 1: Load LangFlow JSON ---
def load_langflow_json(path: str) -> Dict:
    with open(path, 'r') as f:
        return json.load(f)

# --- Step 2: Extract Node Definitions ---
def extract_nodes_and_edges(data: Dict):
    nodes = {node["id"]: node for node in data.get("nodes", [])}
    edges = data.get("edges", [])
    return nodes, edges

# --- Step 3: Create LangGraph Python Code ---
def generate_langgraph_code(nodes: Dict, edges: list) -> str:
    code_lines = [
        "from langgraph.graph import StateGraph",
        "",
        "graph = StateGraph()",
        "",
        "# --- Node Functions ---"
    ]

    node_names = {}

    for node_id, node in nodes.items():
        class_path = node.get("class_path", "")
        label = node.get("data", {}).get("label", f"Node_{node_id}")
        node_names[node_id] = label

        if class_path.endswith("PythonFunction") and "code" in node.get("inputs", {}):
            func_code = node["inputs"]["code"]
            code_lines.append(func_code)
            code_lines.append(f"graph.add_node(\"{label}\", {func_code.split('def ')[1].split('(')[0]})")
        else:
            # Stub: just add dummy function for now
            code_lines.append(f"def {label.lower()}(state):")
            code_lines.append(f"    # TODO: implement logic from class {class_path}")
            code_lines.append(f"    return state")
            code_lines.append(f"graph.add_node(\"{label}\", {label.lower()})")
        code_lines.append("")

    code_lines.append("# --- Edges ---")
    for edge in edges:
        src = node_names.get(edge["source"], edge["source"])
        tgt = node_names.get(edge["target"], edge["target"])
        code_lines.append(f"graph.add_edge(\"{src}\", \"{tgt}\")")

    code_lines.append("\n# --- Entry and Finish ---")
    if node_names:
        first = list(node_names.values())[0]
        last = list(node_names.values())[-1]
        code_lines.append(f"graph.set_entry_point(\"{first}\")")
        code_lines.append(f"graph.set_finish_point(\"{last}\")")

    return "\n".join(code_lines)

# --- Step 4: Main Function ---
def convert_langflow_to_langgraph(json_path: str):
    data = load_langflow_json(json_path)
    nodes, edges = extract_nodes_and_edges(data)
    langgraph_code = generate_langgraph_code(nodes, edges)
    return langgraph_code

# Example usage (uncomment to run manually):
# code_output = convert_langflow_to_langgraph("path_to_your_langflow_export.json")
# print(code_output)
if __name__ == "__main__":
    result = convert_langflow_to_langgraph("my_flow.json")
    print(result)
