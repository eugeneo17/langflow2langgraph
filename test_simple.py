from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class GraphState(TypedDict):
    input: str
    question: str
    response: str
    output: str

def create_simple_graph():
    graph = StateGraph(GraphState)
    
    def input_node(state):
        """Handle input"""
        state["question"] = state["input"]
        return state
    
    def llm_node(state):
        """Generate response"""
        state["response"] = f"AI: {state['question']}"
        return state
    
    def output_node(state):
        """Format output"""
        state["output"] = state["response"]
        return state
    
    graph.add_node("input", input_node)
    graph.add_node("llm", llm_node)
    graph.add_node("output", output_node)
    
    graph.add_edge(START, "input")
    graph.add_edge("input", "llm")
    graph.add_edge("llm", "output")
    graph.add_edge("output", END)
    
    return graph.compile()

if __name__ == "__main__":
    app = create_simple_graph()
    result = app.invoke({"input": "Hello"})
    print(result)