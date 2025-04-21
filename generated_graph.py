from langgraph.graph import StateGraph
from typing import TypedDict, Annotated

# Define the state schema
class GraphState(TypedDict):
    input: str
    processed_input: str
    llm_response: str
    output: str

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    # --- Node Functions ---
    def process_input(state):
            if "input" in state:
                state["processed_text"] = state["input"].strip().lower()
            return state
    graph.add_node("textinput", process_input)

    def llmprocessor(state):
        # TODO: implement logic from class langflow.LLMNode
        # For testing purposes, add a mock LLM response
        if "processed_input" in state:
            state["llm_response"] = f"Processed: {state['processed_input']}"
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