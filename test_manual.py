#!/usr/bin/env python
# -*- coding: utf-8 -*-

from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

class LoopGraphState(TypedDict):
    input: str
    current_index: int
    max_items: int
    results: List[Any]
    decision: str
    llm_response: str
    output: Dict[str, Any]

def create_loop_graph():
    # Define the graph with proper state schema
    graph = StateGraph(LoopGraphState)

    # --- Node Functions ---
    def inputprocessor(state):
        """Process the input and initialize the loop state."""
        # Initialize loop variables
        state["current_index"] = 0
        state["max_items"] = 3  # Process 3 items
        state["results"] = []
        return state
    graph.add_node("inputprocessor", inputprocessor)

    def check_loop_condition(state):
        """Check if we should continue looping or exit."""
        if "current_index" in state and "max_items" in state:
            if state["current_index"] < state["max_items"]:
                return {"decision": "continue_loop"}
            else:
                return {"decision": "exit_loop"}
        return {"decision": "exit_loop"}
    graph.add_node("loopcontroller", check_loop_condition)

    def itemprocessor(state):
        """Process the state using an LLM."""
        # LLM implementation
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
        """Update the loop state after processing an item."""
        if "llm_response" in state and "current_index" in state and "results" in state:
            state["results"].append(state["llm_response"])
            state["current_index"] += 1
        return state
    graph.add_node("loopupdater", update_loop_state)

    def format_results(state):
        """Format the final results."""
        if "results" in state:
            state["output"] = {"processed_items": state["results"]}
        return state
    graph.add_node("outputformatter", format_results)

    # --- Edges ---
    graph.add_edge("inputprocessor", "loopcontroller")

    # Conditional routing based on decision
    graph.add_conditional_edges(
        "loopcontroller",
        lambda state: state.get('decision'),
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

class ConditionalGraphState(TypedDict):
    input: str
    condition: str
    llm_response: str
    output: Dict[str, Any]

def create_conditional_graph():
    # Define the graph with proper state schema
    graph = StateGraph(ConditionalGraphState)

    # --- Node Functions ---
    def inputprocessor(state):
        """Process the input and determine the condition."""
        # Check the input to determine which path to take
        if "input" in state:
            input_text = state["input"]
            if "?" in input_text:
                state["condition"] = "question"
            elif len(input_text) < 20:
                state["condition"] = "short"
            else:
                state["condition"] = "long"
        else:
            state["condition"] = "default"
        return state
    graph.add_node("inputprocessor", inputprocessor)

    def process_question(state):
        """Process a question input."""
        if "input" in state:
            state["output"] = {
                "response": f"Answer to question: {state['input']}",
                "type": "question"
            }
        return state
    graph.add_node("questionprocessor", process_question)

    def process_short_input(state):
        """Process a short input."""
        if "input" in state:
            state["output"] = {
                "response": f"Short response to: {state['input']}",
                "type": "short"
            }
        return state
    graph.add_node("shortprocessor", process_short_input)

    def process_long_input(state):
        """Process a long input using an LLM."""
        # LLM implementation
        if "prompt" in state:
            # In a real implementation, this would call the LLM
            state["llm_response"] = f"Response to: {state['prompt']}"
        elif "input" in state:
            state["llm_response"] = f"Response to: {state['input']}"
        else:
            state["llm_response"] = "No input provided"

        state["output"] = {
            "response": state["llm_response"],
            "type": "long"
        }
        return state
    graph.add_node("longprocessor", process_long_input)

    def default_processor(state):
        """Process input with a default handler."""
        state["output"] = {
            "response": "Default response",
            "type": "default"
        }
        return state
    graph.add_node("defaultprocessor", default_processor)

    # --- Edges ---
    # Conditional routing based on condition
    graph.add_conditional_edges(
        "inputprocessor",
        lambda state: state.get('condition'),
        {
            "question": "questionprocessor",
            "short": "shortprocessor",
            "long": "longprocessor",
            "default": "defaultprocessor"
        }
    )

    # --- Entry and Finish ---
    graph.set_entry_point("inputprocessor")
    # Multiple finish points
    graph.set_finish_point("questionprocessor")
    graph.set_finish_point("shortprocessor")
    graph.set_finish_point("longprocessor")
    graph.set_finish_point("defaultprocessor")

    return graph.compile()

def test_loop_graph():
    # Create the graph
    app = create_loop_graph()

    # Test with a comma-separated list
    test_input = {
        "input": "apple,banana,cherry,date"
    }

    print("Input:", test_input)
    print("\nProcessing...\n")

    try:
        # Run the graph
        result = app.invoke(test_input)
        print("Output:", result)
        print("\nStatus: Success ✅")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nStatus: Failed ❌")

def test_conditional_graph():
    # Create the graph
    app = create_conditional_graph()

    # Test with different inputs
    test_inputs = [
        {"input": "What is the capital of France?"},  # Question
        {"input": "Hello"},  # Short
        {"input": "This is a much longer input that should trigger the long input processor with LLM"}  # Long
    ]

    for i, test_input in enumerate(test_inputs):
        print(f"\nTest {i+1}:")
        print("Input:", test_input)
        print("\nProcessing...\n")

        try:
            # Run the graph
            result = app.invoke(test_input)
            print("Output:", result)
            print("\nStatus: Success ✅")
        except Exception as e:
            print(f"Error: {str(e)}")
            print("\nStatus: Failed ❌")

if __name__ == "__main__":
    print("=== Testing Loop Graph ===\n")
    test_loop_graph()

    print("\n=== Testing Conditional Graph ===\n")
    test_conditional_graph()
