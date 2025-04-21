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
            # Process the input
            if "input" in state:
                state["processed_input"] = state["input"].upper()
            return state
    graph.add_node("inputprocessor", process_input)

    def llmnode(state):
        # TODO: implement logic from class langflow.LLMNode
        # For testing purposes, add a mock LLM response
        if "processed_input" in state:
            state["llm_response"] = f"Processed: {state['processed_input']}"
        return state
    graph.add_node("llmnode", llmnode)

    def format_output(state):
            # Format the output
            if "llm_response" in state:
                state["output"] = f"Result: {state['llm_response']}"
            return state
    graph.add_node("outputformatter", format_output)

    # --- Edges ---
    graph.add_edge("inputprocessor", "llmnode")
    graph.add_edge("llmnode", "outputformatter")

    # --- Entry and Finish ---
    graph.set_entry_point("inputprocessor")
    graph.set_finish_point("outputformatter")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "Test input"})
    print(result)