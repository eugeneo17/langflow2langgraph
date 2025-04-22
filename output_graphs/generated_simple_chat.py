from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    input: str
    prompt: str
    llm_response: str
    output: Dict[str, Any]

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    def node_input_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = {"result": state["input"]}
        return state
    graph.add_node("node_input_node", node_input_node)

    def node_prompt_node(state):
        """Process the state by formatting a prompt template."""
        # Prompt template implementation
        template = "You are a helpful assistant. Answer the following question:\n\n{input}"
        # Format the template with state variables
        formatted_prompt = template
        # Format the template with state variables
        if "input" in state:
            formatted_prompt = template.format(input=state["input"])
        state["prompt"] = formatted_prompt
        return state
    graph.add_node("node_prompt_node", node_prompt_node)

    def node_llm_node(state):
        """Process the state using an LLM."""
        # LLM implementation
        # Model: gpt-3.5-turbo-instruct, Temperature: 0.7
        if "prompt" in state:
            # In a real implementation, this would call the LLM
            state["llm_response"] = f"Response to: {state['prompt']}"
        elif "input" in state:
            state["llm_response"] = f"Response to: {state['input']}"
        else:
            state["llm_response"] = "No input provided"
        return state
    graph.add_node("node_llm_node", node_llm_node)

    def node_output_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "llm_response" in state:
            state["output"] = {"result": state["llm_response"]}
        return state
    graph.add_node("node_output_node", node_output_node)

    # --- Edges ---
    graph.add_edge("node_input_node", "node_prompt_node")
    graph.add_edge("node_prompt_node", "node_llm_node")
    graph.add_edge("node_llm_node", "node_output_node")

    # --- Entry and Finish ---
    graph.set_entry_point("node_input_node")
    graph.set_finish_point("node_output_node")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "What is LangGraph?"})
    print(result)
