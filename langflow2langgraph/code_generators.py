#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangGraph Code Generators
------------------------

This module provides specialized code generators for different node types.
"""

from typing import Dict, Any

def generate_llm_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for an LLM node"""
    inputs = node_data.get("inputs", {})
    model_name = inputs.get("model_name", "")
    temperature = inputs.get("temperature", 0.7)

    code = f"""def {node_name}(state):
    \"\"\"Process the state using an LLM.\"\"\"
    # LLM implementation
    # Model: {model_name}, Temperature: {temperature}
    if "prompt" in state:
        # In a real implementation, this would call the LLM
        state["llm_response"] = f"Response to: {{state['prompt']}}"
    elif "input" in state:
        state["llm_response"] = f"Response to: {{state['input']}}"
    else:
        state["llm_response"] = "No input provided"
    return state"""
    return code

def generate_chat_model_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Chat Model node"""
    inputs = node_data.get("inputs", {})
    model_name = inputs.get("model_name", "")
    temperature = inputs.get("temperature", 0.7)
    
    code = f"""def {node_name}(state):
    \"\"\"Process the state using a Chat Model.\"\"\"
    # Chat Model implementation
    # Model: {model_name}, Temperature: {temperature}
    if "messages" in state and isinstance(state["messages"], list):
        # In a real implementation, this would call the Chat Model
        state["chat_response"] = f"Response to messages: {{len(state['messages'])}} messages"
    elif "input" in state:
        # Create a simple message and respond
        state["chat_response"] = f"Response to: {{state['input']}}"
    else:
        state["chat_response"] = "No input provided"
    return state"""
    return code

def generate_chain_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Chain node"""
    chain_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state through a chain.\"\"\"
    # Chain implementation: {chain_type}
    if "input" in state:
        # In a real implementation, this would process through the chain
        state["chain_result"] = f"Chain processed: {{state['input']}}"
    return state"""
    return code

def generate_agent_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for an Agent node"""
    agent_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state using an agent.\"\"\"
    # Agent implementation: {agent_type}
    if "input" in state:
        # In a real implementation, this would use tools and reasoning
        state["agent_result"] = f"Agent processed: {{state['input']}}"
        state["intermediate_steps"] = ["Step 1: Thinking", "Step 2: Acting"]
    return state"""
    return code

def generate_tool_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Tool node"""
    tool_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state using a tool.\"\"\"
    # Tool implementation: {tool_type}
    if "input" in state:
        # In a real implementation, this would execute the tool
        state["tool_result"] = f"Tool executed on: {{state['input']}}"
    return state"""
    return code

def generate_memory_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Memory node"""
    memory_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state using memory.\"\"\"
    # Memory implementation: {memory_type}
    if "history" not in state:
        state["history"] = []
    if "input" in state and "llm_response" in state:
        # Add the current exchange to history
        state["history"].append((state["input"], state["llm_response"]))
    return state"""
    return code

def generate_prompt_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Prompt node"""
    inputs = node_data.get("inputs", {})
    template = inputs.get("template", "")

    code = f"""def {node_name}(state):
    \"\"\"Process the state by formatting a prompt template.\"\"\"
    # Prompt template implementation
    template = \"\"\"{template}\"\"\"
    # Format the template with state variables
    formatted_prompt = template
    # Extract variables from the template
    import re
    variables = re.findall(r'{{([^{{}}]+)}}', template)
    # Replace variables with values from state
    for var in variables:
        var_clean = var.strip()
        if var_clean in state:
            formatted_prompt = formatted_prompt.replace('{{{{' + var + '}}}}', str(state[var_clean]))
    state["prompt"] = formatted_prompt
    return state"""
    return code

def generate_retriever_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Retriever node"""
    retriever_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state by retrieving documents.\"\"\"
    # Retriever implementation: {retriever_type}
    if "input" in state:
        # In a real implementation, this would retrieve documents
        state["documents"] = [
            {{"content": f"Document 1 relevant to {{state['input']}}", "metadata": {{}}}},
            {{"content": f"Document 2 relevant to {{state['input']}}", "metadata": {{}}}}
        ]
    return state"""
    return code

def generate_vectorstore_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a VectorStore node"""
    vectorstore_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state by searching a vector store.\"\"\"
    # VectorStore implementation: {vectorstore_type}
    if "input" in state:
        # In a real implementation, this would search the vector store
        state["search_results"] = [
            {{"content": f"Result 1 for {{state['input']}}", "metadata": {{}}}},
            {{"content": f"Result 2 for {{state['input']}}", "metadata": {{}}}}
        ]
    return state"""
    return code

def generate_embedding_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for an Embedding node"""
    embedding_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state by generating embeddings.\"\"\"
    # Embedding implementation: {embedding_type}
    if "input" in state:
        # In a real implementation, this would generate embeddings
        state["embeddings"] = [[0.1, 0.2, 0.3]]  # Mock embedding vector
    return state"""
    return code

def generate_document_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Document node"""
    document_type = node_data.get("class_path", "").split(".")[-1]

    code = f"""def {node_name}(state):
    \"\"\"Process the state by loading documents.\"\"\"
    # Document loader implementation: {document_type}
    if "file_path" in state:
        # In a real implementation, this would load a document
        state["document_content"] = f"Content loaded from {{state['file_path']}}"
    return state"""
    return code

def generate_text_splitter_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a TextSplitter node"""
    splitter_type = node_data.get("class_path", "").split(".")[-1]
    inputs = node_data.get("inputs", {})
    chunk_size = inputs.get("chunk_size", 1000)

    code = f"""def {node_name}(state):
    \"\"\"Process the state by splitting text into chunks.\"\"\"
    # Text splitter implementation: {splitter_type}
    # Chunk size: {chunk_size}
    if "input" in state and isinstance(state["input"], str):
        # Simple splitting by paragraphs for demonstration
        paragraphs = state["input"].split("\\n\\n")
        state["chunks"] = [p for p in paragraphs if p.strip()]
    return state"""
    return code

def generate_utility_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Utility node"""
    utility_type = node_data.get("class_path", "").split(".")[-1]

    # Special case for PythonFunction
    if utility_type == "PythonFunction":
        inputs = node_data.get("inputs", {})
        code_str = inputs.get("code", "")
        if code_str:
            # Extract the function definition and body
            return code_str

    code = f"""def {node_name}(state):
    \"\"\"Process the state using a utility function.\"\"\"
    # Utility implementation: {utility_type}
    if "input" in state:
        state["processed_input"] = state["input"].upper()
    return state"""
    return code

def generate_custom_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Custom node"""
    inputs = node_data.get("inputs", {})
    code_str = inputs.get("code", "")

    if code_str:
        # If custom code is provided, use it
        return code_str

    # Generate specific implementations based on node type
    node_id = node_data.get("id", "")
    
    if "chatinput" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Handle chat input from user.\"\"\"
        if "input" in state:
            state["messages"] = [state["input"]]
            state["question"] = state["input"]
        return state"""
    elif "chatoutput" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Format chat output for user.\"\"\"
        if "response" in state:
            state["output"] = state["response"]
        elif "messages" in state and state["messages"]:
            state["output"] = state["messages"][-1]
        return state"""
    elif "prompt" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Build prompt from context and question.\"\"\"
        context = state.get("context", "")
        question = state.get("question", "")
        prompt = f"Context: {{context}}\\n\\nQuestion: {{question}}"
        state["prompt"] = prompt
        return state"""
    elif "languagemodel" in node_id.lower() or "llm" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Process with language model.\"\"\"
        prompt = state.get("prompt", state.get("input", ""))
        # Simulate LLM response
        state["response"] = f"AI Response: {{prompt}}"
        return state"""
    elif "embedding" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Generate embeddings for text.\"\"\"
        text = state.get("input", "")
        # Simulate embedding generation
        state["embeddings"] = f"embeddings_for_{{text}}"
        return state"""
    elif "localdb" in node_id.lower() or "database" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Query local database/vector store.\"\"\"
        query = state.get("question", state.get("input", ""))
        # Simulate database query
        state["documents"] = [f"doc1_for_{{query}}", f"doc2_for_{{query}}"]
        return state"""
    elif "parser" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Parse and structure documents.\"\"\"
        documents = state.get("documents", [])
        # Simulate parsing
        state["context"] = " ".join(documents) if documents else ""
        return state"""
    elif "confluence" in node_id.lower():
        code = f"""def {node_name}(state):
        \"\"\"Fetch data from Confluence.\"\"\"
        # Simulate Confluence data fetch
        state["raw_data"] = "confluence_data_content"
        return state"""
    else:
        code = f"""def {node_name}(state):
        \"\"\"Custom node processing.\"\"\"
        if "input" in state:
            state["output"] = f"Processed: {{state['input']}}"
        return state"""
    return code

def generate_output_parser_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for an Output Parser node"""
    parser_type = node_data.get("class_path", "").split(".")[-1]
    
    code = f"""def {node_name}(state):
    \"\"\"Process the state by parsing structured output.\"\"\"
    # Output Parser implementation: {parser_type}
    if "input" in state:
        # In a real implementation, this would parse the input
        try:
            # Mock parsing - in reality this would use the specific parser logic
            if "json" in "{parser_type}".lower():
                import json
                # Try to parse as JSON if it looks like JSON
                if state["input"].strip().startswith('{{') and state["input"].strip().endswith('}}'):
                    state["parsed_output"] = json.loads(state["input"])
                else:
                    # Mock JSON structure
                    state["parsed_output"] = {{
                        "result": state["input"],
                        "status": "success"
                    }}
            elif "pydantic" in "{parser_type}".lower():
                # Mock Pydantic parsing
                state["parsed_output"] = {{
                    "content": state["input"],
                    "metadata": {{}}
                }}
            elif "regex" in "{parser_type}".lower():
                # Mock regex parsing
                state["parsed_output"] = {{
                    "matched": True,
                    "extracted": state["input"]
                }}
            else:
                # Generic structured output
                state["parsed_output"] = {{
                    "output": state["input"]
                }}
        except Exception as e:
            state["parsed_output"] = {{
                "error": str(e),
                "original_input": state["input"]
            }}
    return state"""
    return code

def generate_router_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Router node"""
    router_type = node_data.get("class_path", "").split(".")[-1]
    
    code = f"""def {node_name}(state):
    \"\"\"Process the state by determining routing paths.\"\"\"
    # Router implementation: {router_type}
    if "input" in state:
        # In a real implementation, this would determine the route based on input
        # For demonstration, we'll use a simple length-based routing
        input_text = state["input"]
        
        # Simple routing logic based on input characteristics
        if "?" in input_text:
            state["route"] = "question_route"
        elif len(input_text) < 20:
            state["route"] = "short_input_route"
        elif any(keyword in input_text.lower() for keyword in ["help", "support", "assist"]):
            state["route"] = "help_route"
        else:
            state["route"] = "default_route"
            
        state["destination"] = state["route"]
    return state"""
    return code

def generate_document_transformer_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """Generate LangGraph code for a Document Transformer node"""
    transformer_type = node_data.get("class_path", "").split(".")[-1]
    
    code = f"""def {node_name}(state):
    \"\"\"Process the state by transforming documents.\"\"\"
    # Document Transformer implementation: {transformer_type}
    if "documents" in state and isinstance(state["documents"], list):
        # In a real implementation, this would transform the documents
        # For demonstration, we'll create a simple transformation
        transformed_docs = []
        for i, doc in enumerate(state["documents"]):
            # Create a transformed version of each document
            if isinstance(doc, dict):
                # If it's already a dict with content
                transformed = {{
                    "content": f"Transformed: {{doc.get('content', 'No content')}}",
                    "metadata": doc.get("metadata", {{}}) | {{"transformed": True, "transformer": "{transformer_type}"}}
                }}
            elif isinstance(doc, str):
                # If it's just a string
                transformed = {{
                    "content": f"Transformed: {{doc}}",
                    "metadata": {{"transformed": True, "transformer": "{transformer_type}"}}
                }}
            else:
                # Try to handle other formats
                transformed = {{
                    "content": f"Transformed document {{i}}",
                    "metadata": {{"transformed": True, "transformer": "{transformer_type}"}}
                }}
            transformed_docs.append(transformed)
        
        state["transformed_documents"] = transformed_docs
    return state"""
    return code
