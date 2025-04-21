from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    input: str
    output: Dict[str, Any]
    input_length: str
    has_question: str
    sentiment: List[Any]
    route: str
    llm_response: str

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    def analyze_input(state):
            if "input" in state:
                text = state["input"].lower()
                state["input_length"] = len(text)
                state["has_question"] = "?" in text
                state["sentiment"] = "positive" if any(word in text for word in ["good", "great", "excellent", "happy"]) else "negative" if any(word in text for word in ["bad", "terrible", "sad", "unhappy"]) else "neutral"
            return state
    graph.add_node("inputanalyzer", analyze_input)

    def route_response(state):
            if "sentiment" in state and "has_question" in state:
                if state["has_question"]:
                    return {"route": "question_handler"}
                elif state["sentiment"] == "positive":
                    return {"route": "positive_handler"}
                elif state["sentiment"] == "negative":
                    return {"route": "negative_handler"}
                else:
                    return {"route": "neutral_handler"}
            return {"route": "neutral_handler"}
    graph.add_node("responserouter", route_response)

    def questionhandler(state):
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
    graph.add_node("questionhandler", questionhandler)

    def positivehandler(state):
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
    graph.add_node("positivehandler", positivehandler)

    def negativehandler(state):
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
    graph.add_node("negativehandler", negativehandler)

    def neutralhandler(state):
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
    graph.add_node("neutralhandler", neutralhandler)

    def format_output(state):
            if "llm_response" in state:
                state["output"] = {
                    "response": state["llm_response"],
                    "metadata": {
                        "sentiment": state.get("sentiment", "unknown"),
                        "was_question": state.get("has_question", False),
                        "length": state.get("input_length", 0)
                    }
                }
            return state
    graph.add_node("outputformatter", format_output)

    # --- Edges ---
    graph.add_edge("inputanalyzer", "responserouter")

    # Conditional routing based on route
    graph.add_conditional_edges(
        "responserouter",
        lambda state: state.get('route') == 'neutral_handler',
        {
            "question_handler": "questionhandler",
            "positive_handler": "positivehandler",
            "negative_handler": "negativehandler",
            "neutral_handler": "neutralhandler",
        }
    )
    graph.add_edge("questionhandler", "outputformatter")
    graph.add_edge("positivehandler", "outputformatter")
    graph.add_edge("negativehandler", "outputformatter")
    graph.add_edge("neutralhandler", "outputformatter")

    # --- Entry and Finish ---
    graph.set_entry_point("inputanalyzer")
    graph.set_finish_point("outputformatter")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "Test input"})
    print(result)