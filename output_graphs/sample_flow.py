from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    input: str
    output: Dict[str, Any]
    processed_text: List[Any]
    llm_response: str
    final_output: str
    error: str

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    def process_input(state):
            if "input" in state:
                state["processed_text"] = state["input"].strip().lower()
            return state
    graph.add_node("textinput", process_input)

    def llmprocessor(state):
        """Process the state using an LLM."""
        # LLM implementation
        # Model: , Temperature: 0.7
        if "prompt" in state:
            # In a real implementation, this would call the LLM
            state["llm_response"] = f"Response to: {state['prompt']}"
        elif "input" in state:
            state["llm_response"] = f"Response to: {state['input']}"
        else:
            state["llm_response"] = "No input provided"
        return state
    graph.add_node("llmprocessor", llmprocessor)

    def format_output(state):
        if "llm_response" in state:
            state["final_output"] = {
                "summary": state["llm_response"],
                "timestamp": state.get("timestamp", "")
            }
        return state
    graph.add_node("outputformatter", format_output)

    def validate_response(state):
        if "final_output" not in state:
            state["error"] = "Missing final output"
            return state
        if not isinstance(state["final_output"], dict):
            state["error"] = "Invalid output format"
        return state
    graph.add_node("responsevalidator", validate_response)

    # --- Edges ---
    graph.add_edge("textinput", "llmprocessor")
    graph.add_edge("llmprocessor", "outputformatter")
    graph.add_edge("outputformatter", "responsevalidator")

    # --- Entry and Finish ---
    graph.set_entry_point("textinput")
    graph.set_finish_point("responsevalidator")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "Test input"})
    print(result)
