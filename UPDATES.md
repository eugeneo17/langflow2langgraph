# LangFlow to LangGraph Converter Updates

## Recent Updates

### Project-Based Organization (July 2023)

We've added a new project-based organization structure to make it easier to manage multiple projects:

1. **Project-Based Structure**:
   - Created a `projects` directory with subdirectories for each project
   - Each project has its own `input_flows` and `output_graphs` directories
   - Added README.md files for each project with documentation

2. **New Scripts**:
   - Added `batch_convert_projects.py` for batch conversion of project-based structure
   - Added `test_all_projects.py` for testing all project graphs
   - Added `fix_indentation.py` for fixing indentation issues in generated code

3. **Improved Documentation**:
   - Updated README.md with information about the project-based structure
   - Added examples of how to use the project-based structure

### Modularization and Improvements (June 2023)

We've made several improvements to the LangFlow to LangGraph converter:

1. **Modular Code Structure**:
   - Split the mapping.py file into multiple specialized modules:
     - `mapping.py` - Main mapping logic
     - `node_categories.py` - Node category definitions
     - `state_fields.py` - State field definitions
     - `code_generators.py` - Code generators for different node types

2. **Improved Code Generation**:
   - Fixed indentation issues in generated code
   - Added proper docstrings to generated functions
   - Improved handling of conditional routing
   - Enhanced loop construct support

3. **Better Validation**:
   - Enhanced validator.py to handle docstrings and indentation better
   - Added more robust error handling

4. **New Examples**:
   - Added examples for loop flows and conditional flows
   - Created manual test file to demonstrate correct implementation

5. **New Features**:
   - Support for a wide range of node types:
     - LLM nodes
     - Chat Model nodes
     - Chain nodes
     - Agent nodes
     - Tool nodes
     - Memory nodes
     - Prompt nodes
     - Retriever nodes
     - VectorStore nodes
     - Embedding nodes
     - Document nodes
     - Text Splitter nodes
     - Utility nodes
     - Custom nodes
     - Output Parser nodes
     - Router nodes
     - Document Transformer nodes

## Updated Project Structure

```
langflow2langgraph/
├── langflow2langgraph/
│   ├── __init__.py
│   ├── converter.py       # Main converter logic
│   ├── mapping.py         # Mappings between Langflow and LangGraph
│   ├── node_categories.py # Node category definitions
│   ├── state_fields.py    # State field definitions
│   ├── code_generators.py # Code generators for different node types
│   ├── validator.py       # Code validation and fixing
│   ├── code_generator.py  # LangGraph code generation
│   └── cli.py             # Command-line interface
├── input_flows/          # Langflow JSON exports (flat structure)
│   ├── simple_chat.json   # Simple chat example
│   ├── retrieval_qa.json  # Retrieval QA example
│   ├── agent_example.json # Agent example
│   ├── loop_flow.json     # Loop example
│   └── conditional_flow.json # Conditional routing example
├── output_graphs/        # Generated LangGraph Python files (flat structure)
│   ├── simple_chat.py     # Simple chat example
│   ├── retrieval_qa.py    # Retrieval QA example
│   ├── agent_graph.py     # Agent example
│   ├── loop_graph.py      # Loop example
│   └── conditional_graph.py # Conditional routing example
├── projects/             # Project-based structure
│   ├── simple_chat/      # Simple chat project
│   │   ├── input_flows/  # Langflow JSON exports
│   │   ├── output_graphs/ # Generated LangGraph Python files
│   │   └── README.md     # Project documentation
│   ├── retrieval_qa/     # Retrieval QA project
│   ├── agent/            # Agent project
│   ├── conditional/      # Conditional routing project
│   ├── loop/             # Loop project
│   └── README.md         # Projects documentation
├── tests/
│   └── test_converter.py
├── batch_convert.py      # Batch conversion script (flat structure)
├── batch_convert_projects.py # Batch conversion script (project-based structure)
├── test_all_graphs.py    # Test all converted graphs (flat structure)
├── test_all_projects.py  # Test all project graphs (project-based structure)
├── fix_indentation.py    # Fix indentation issues in generated code
├── setup.py
├── README.md
├── UPDATES.md           # Recent updates and changes
└── requirements.txt
```

## Testing

### Testing Flat Structure

You can test all the graphs in the flat structure:

```bash
python test_all_graphs.py
```

This will test all the graphs in the `output_graphs` directory.

### Testing Project-Based Structure

You can test all the graphs in the project-based structure:

```bash
python test_all_projects.py
```

This will test all the graphs in the `projects` directory.

### Testing Individual Projects

You can test individual projects by importing their create_graph function:

```python
from projects.simple_chat.output_graphs.simple_chat import create_graph

# Create the graph
graph = create_graph()

# Run the graph with an input
result = graph.invoke({"input": "Hello, world!"})

print(result)
```

## Conversion

### Converting Flat Structure

To convert all the flows in the flat structure:

```bash
python batch_convert.py
```

This will convert all the JSON files in the `input_flows` directory to Python files in the `output_graphs` directory.

### Converting Project-Based Structure

To convert all the flows in the project-based structure:

```bash
python batch_convert_projects.py
```

This will convert all the JSON files in the `projects/*/input_flows` directories to Python files in the `projects/*/output_graphs` directories.

### Converting Individual Files

To convert an individual file:

```bash
python -m langflow2langgraph.cli input_flows/simple_chat.json output_graphs/simple_chat.py
```

Or using the Python API:

```python
from langflow2langgraph import convert_langflow_to_langgraph

convert_langflow_to_langgraph(
    input_file="input_flows/simple_chat.json",
    output_file="output_graphs/simple_chat.py",
    validate=True
)
```
