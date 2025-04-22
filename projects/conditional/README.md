# Conditional Flow Project

This project demonstrates a conditional routing flow using LangGraph.

## Input Flow

The input flow is a Langflow JSON export that defines a conditional flow with the following components:
- Input analyzer node: Analyzes the input for sentiment and question detection
- Response router node: Routes the input based on analysis
- Question handler node: Processes questions
- Positive handler node: Processes positive sentiment
- Negative handler node: Processes negative sentiment
- Neutral handler node: Processes neutral sentiment
- Output formatter node: Formats the response

## Output Graph

The output graph is a LangGraph Python file that implements the conditional flow. It includes:
- A state schema that defines the input, analysis results, routing decision, and output
- Node functions that process the state
- Conditional edges that route the flow based on the analysis
- Entry and finish points

## Usage

```python
from projects.conditional.output_graphs.conditional_flow import create_graph

# Create the graph
graph = create_graph()

# Run the graph with different inputs
result1 = graph.invoke({"input": "What is LangGraph?"})  # Question
result2 = graph.invoke({"input": "I love LangGraph!"})   # Positive
result3 = graph.invoke({"input": "I hate errors."})      # Negative
result4 = graph.invoke({"input": "LangGraph is a tool."}) # Neutral

print(result1)
print(result2)
print(result3)
print(result4)
```
