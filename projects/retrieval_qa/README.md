# Retrieval QA Project

This project demonstrates a retrieval-based question answering flow using LangGraph.

## Input Flow

The input flow is a Langflow JSON export that defines a retrieval QA flow with the following components:
- Input node: Receives user question
- Document node: Loads documents
- Text splitter node: Splits documents into chunks
- Embedding node: Generates embeddings for chunks
- Vector store node: Stores embeddings and chunks
- Retriever node: Retrieves relevant chunks
- Context formatter node: Formats retrieved chunks into context
- Prompt node: Formats the question and context into a prompt
- LLM node: Processes the prompt and generates a response
- Output node: Returns the response to the user

## Output Graph

The output graph is a LangGraph Python file that implements the retrieval QA flow. It includes:
- A state schema that defines the input, documents, context, prompt, LLM response, and output
- Node functions that process the state
- Edges that connect the nodes
- Entry and finish points

## Usage

```python
from projects.retrieval_qa.output_graphs.retrieval_qa import create_graph

# Create the graph
graph = create_graph()

# Run the graph with an input
result = graph.invoke({"input": "What is LangGraph?"})

print(result)
```
