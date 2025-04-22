# Simple Chat Project

This project demonstrates a simple chat flow using LangGraph.

## Input Flow

The input flow is a Langflow JSON export that defines a simple chat flow with the following components:
- Input node: Receives user input
- Prompt node: Formats the input into a prompt
- LLM node: Processes the prompt and generates a response
- Output node: Returns the response to the user

## Output Graph

The output graph is a LangGraph Python file that implements the simple chat flow. It includes:
- A state schema that defines the input, prompt, LLM response, and output
- Node functions that process the state
- Edges that connect the nodes
- Entry and finish points

## Usage

```python
from projects.simple_chat.output_graphs.simple_chat import create_graph

# Create the graph
graph = create_graph()

# Run the graph with an input
result = graph.invoke({"input": "Hello, world!"})

print(result)
```
