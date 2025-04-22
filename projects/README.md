# LangGraph Projects

This directory contains various LangGraph projects, each demonstrating different aspects of LangGraph functionality.

## Project Structure

Each project follows the same structure:

```
project_name/
├── input_flows/       # Langflow JSON exports
├── output_graphs/     # Generated LangGraph Python files
└── README.md          # Project documentation
```

## Available Projects

- [Simple Chat](./simple_chat/): A simple chat flow
- [Retrieval QA](./retrieval_qa/): A retrieval-based question answering flow
- [Agent](./agent/): An agent-based flow
- [Conditional](./conditional/): A conditional routing flow
- [Loop](./loop/): A loop flow

## Adding New Projects

To add a new project:

1. Create a new directory with the project name
2. Create input_flows and output_graphs subdirectories
3. Add your Langflow JSON export to the input_flows directory
4. Generate the LangGraph Python file using the converter
5. Add a README.md file with project documentation

## Testing Projects

Each project can be tested individually by importing its create_graph function and invoking it with appropriate input.

Example:

```python
from projects.simple_chat.output_graphs.simple_chat import create_graph

# Create the graph
graph = create_graph()

# Run the graph with an input
result = graph.invoke({"input": "Hello, world!"})

print(result)
```
