from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    input: str
    output: Dict[str, Any]

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    def node_input_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_input_node", node_input_node)

    def node_llm_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_llm_node", node_llm_node)

    def node_search_tool(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_search_tool", node_search_tool)

    def node_calculator_tool(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_calculator_tool", node_calculator_tool)

    def node_tools_combiner(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_tools_combiner", node_tools_combiner)

    def node_agent_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_agent_node", node_agent_node)

    def node_agent_executor(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_agent_executor", node_agent_executor)

    def node_output_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = f"Custom processing: {state['input']}"
        return state
    graph.add_node("node_output_node", node_output_node)

    # --- Edges ---
    graph.add_edge("node_input_node", "node_agent_executor")
    graph.add_edge("node_llm_node", "node_agent_node")
    graph.add_edge("node_search_tool", "node_tools_combiner")
    graph.add_edge("node_calculator_tool", "node_tools_combiner")
    graph.add_edge("node_tools_combiner", "node_agent_node")
    graph.add_edge("node_agent_node", "node_agent_executor")
    graph.add_edge("node_agent_executor", "node_output_node")

    # --- Entry and Finish ---
    graph.set_entry_point("node_input_node")
    graph.set_finish_point("node_output_node")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "Test input"})
    print(result)
