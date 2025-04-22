# Agent Project

This project demonstrates an agent-based flow using LangGraph.

## Input Flow

The input flow is a Langflow JSON export that defines an agent flow with the following components:
- Input node: Receives user input
- Agent node: Processes the input and decides on actions
- Tool nodes: Execute actions
- Output node: Returns the response to the user

## Output Graph

The output graph is a LangGraph Python file that implements the agent flow. It includes:
- A state schema that defines the input, agent state, tool outputs, and final output
- Node functions that process the state
- Edges that connect the nodes
- Entry and finish points

## Usage

```python
from projects.agent.output_graphs.agent_example import create_graph

# Create the graph
graph = create_graph()

# Run the graph with an input
result = graph.invoke({"input": "What's the weather in New York?"})

print(result)
```
