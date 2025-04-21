from langgraph.graph import StateGraph
from typing import TypedDict, Annotated, List, Dict, Any

# Define the state schema
class GraphState(TypedDict):
    input: str
    output: Dict[str, Any]
    items: List[Any]
    current_index: int
    results: List[Any]
    decision: str
    llm_response: str

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    def process_input(state):
        if "input" in state:
            state["items"] = state["input"].split(",")
            state["current_index"] = 0
            state["results"] = []
        return state

    graph.add_node("inputprocessor", process_input)

    def check_loop_condition(state):
        if "items" in state and "current_index" in state:
            if state["current_index"] < len(state["items"]):
                return {"decision": "continue_loop"}
            else:
                return {"decision": "exit_loop"}
        return {"decision": "exit_loop"}

    graph.add_node("loopcontroller", check_loop_condition)

    def itemprocessor(state):
        # TODO: implement logic from class langflow.LLMNode
        # For testing purposes, add a mock LLM response
        if "items" in state and "current_index" in state:
            current_item = state["items"][state["current_index"]]
            state["llm_response"] = f"Processed item {state['current_index']}: {current_item}"
        return state

    graph.add_node("itemprocessor", itemprocessor)

    def update_loop_state(state):
        if "llm_response" in state and "current_index" in state and "results" in state:
            state["results"].append(state["llm_response"])
            state["current_index"] += 1
        return state

    graph.add_node("loopupdater", update_loop_state)

    def format_results(state):
        if "results" in state:
            state["output"] = {"processed_items": state["results"]}
        return state

    graph.add_node("outputformatter", format_results)

    # --- Edges ---
    graph.add_edge("inputprocessor", "loopcontroller")

    # Conditional routing based on decision
    graph.add_conditional_edges(
        "loopcontroller",
        lambda state: state.get("decision", ""),
        {
            "continue_loop": "itemprocessor",
            "exit_loop": "outputformatter",
        }
    )

    graph.add_edge("itemprocessor", "loopupdater")
    graph.add_edge("loopupdater", "loopcontroller")

    # --- Entry and Finish ---
    graph.set_entry_point("inputprocessor")
    graph.set_finish_point("outputformatter")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "Test input"})
    print(result)