# Input Flows

This directory contains Langflow JSON export files that can be converted to LangGraph Python files.

## File Structure

- `simple_chat.json` - A simple chat example with an LLM
- `retrieval_qa.json` - A retrieval-based QA example with document loading and vector search
- `agent_example.json` - An agent-based example with tools
- `loop_flow.json` - An example demonstrating loop constructs
- `conditional_flow.json` - An example demonstrating conditional routing

## Adding New Flows

To add a new flow:

1. Export your flow from Langflow as a JSON file
2. Place the JSON file in this directory
3. Run the batch conversion script:

```bash
python batch_convert.py
```

This will convert all JSON files in this directory to LangGraph Python files in the `output_graphs` directory.

## Testing

To test all the converted graphs:

```bash
python test_all_graphs.py
```

This will run each graph with a simple input and display the results.
