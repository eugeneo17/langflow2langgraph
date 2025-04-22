# Loop Flow Project

This project demonstrates a loop flow using LangGraph.

## Input Flow

The input flow is a Langflow JSON export that defines a loop flow with the following components:
- Input processor node: Processes the input and prepares items for iteration
- Loop controller node: Checks loop conditions
- Item processor node: Processes each item
- Loop updater node: Updates the loop state
- Output formatter node: Formats the final output

## Output Graph

The output graph is a LangGraph Python file that implements the loop flow. It includes:
- A state schema that defines the input, items, current index, results, and output
- Node functions that process the state
- Conditional edges that control the loop
- Entry and finish points

## Usage

```python
from projects.loop.output_graphs.loop_flow import create_graph

# Create the graph
graph = create_graph()

# Run the graph with a comma-separated list
result = graph.invoke({"input": "item1,item2,item3"})

print(result)
```
