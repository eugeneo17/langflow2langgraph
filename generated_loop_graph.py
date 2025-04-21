from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

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
        lambda state: state.get('decision') == 'exit_loop',
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