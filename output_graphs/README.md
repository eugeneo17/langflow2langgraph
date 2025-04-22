# Output Graphs

This directory contains LangGraph Python files that have been converted from Langflow JSON exports.

## File Structure

- `simple_chat.py` - A simple chat example with an LLM
- `retrieval_qa.py` - A retrieval-based QA example with document loading and vector search
- `agent_graph.py` - An agent-based example with tools
- `loop_graph.py` - An example demonstrating loop constructs
- `conditional_graph.py` - An example demonstrating conditional routing

## Using the Graphs

Each graph file contains a `create_graph()` function that returns a compiled LangGraph. You can import and use these graphs in your Python code:

```python
from output_graphs.simple_chat import create_graph

# Create the graph
graph = create_graph()

# Run the graph with an input
result = graph.invoke({"input": "Hello, world!"})

print(result)
```

## Testing

To test all the graphs:

```bash
python test_all_graphs.py
```

This will run each graph with a simple input and display the results.
