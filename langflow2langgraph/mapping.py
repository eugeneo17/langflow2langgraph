#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow to LangGraph Mappings
-----------------------------

This module provides mappings between Langflow components and their LangGraph equivalents.
"""

from typing import Dict, Any
from langflow2langgraph.node_categories import NodeCategory, LANGFLOW_CLASS_TO_CATEGORY
from langflow2langgraph.state_fields import CATEGORY_STATE_FIELDS
from langflow2langgraph.code_generators import (
    generate_llm_node_code,
    generate_chain_node_code,
    generate_agent_node_code,
    generate_tool_node_code,
    generate_memory_node_code,
    generate_prompt_node_code,
    generate_retriever_node_code,
    generate_vectorstore_node_code,
    generate_embedding_node_code,
    generate_document_node_code,
    generate_text_splitter_node_code,
    generate_utility_node_code,
    generate_custom_node_code,
    generate_chat_model_node_code,
    generate_output_parser_node_code,
    generate_router_node_code,
    generate_document_transformer_node_code
)

# Mapping of node categories to code generation functions
CATEGORY_CODE_GENERATORS = {
    NodeCategory.LLM: generate_llm_node_code,
    NodeCategory.CHAT_MODEL: generate_chat_model_node_code,
    NodeCategory.CHAIN: generate_chain_node_code,
    NodeCategory.AGENT: generate_agent_node_code,
    NodeCategory.TOOL: generate_tool_node_code,
    NodeCategory.MEMORY: generate_memory_node_code,
    NodeCategory.PROMPT: generate_prompt_node_code,
    NodeCategory.RETRIEVER: generate_retriever_node_code,
    NodeCategory.VECTORSTORE: generate_vectorstore_node_code,
    NodeCategory.EMBEDDING: generate_embedding_node_code,
    NodeCategory.DOCUMENT: generate_document_node_code,
    NodeCategory.TEXT_SPLITTER: generate_text_splitter_node_code,
    NodeCategory.UTILITY: generate_utility_node_code,
    NodeCategory.CUSTOM: generate_custom_node_code,
    NodeCategory.OUTPUT_PARSER: generate_output_parser_node_code,
    NodeCategory.ROUTER: generate_router_node_code,
    NodeCategory.DOCUMENT_TRANSFORMER: generate_document_transformer_node_code,
}

def get_node_category(class_path: str) -> str:
    """
    Determine the category of a node based on its class path.
    
    Args:
        class_path: The class path of the node
        
    Returns:
        The node category
    """
    # Try exact match first
    if class_path in LANGFLOW_CLASS_TO_CATEGORY:
        return LANGFLOW_CLASS_TO_CATEGORY[class_path]
        
    # Try partial match
    for path, category in LANGFLOW_CLASS_TO_CATEGORY.items():
        if class_path.startswith(path) or path in class_path:
            return category
    
    # Infer from class name
    class_name = class_path.split(".")[-1].lower()
    
    # Check for chat models first (more specific than general LLMs)
    if any(keyword in class_name for keyword in ["chatmodel", "chatgpt", "chatvertexai", "chatanthropic", "chatcohere", "chatollama", "chatpalm"]):
        return NodeCategory.CHAT_MODEL
    # Then check for LLMs
    elif any(keyword in class_name for keyword in ["llm", "openai", "anthropic", "cohere", "huggingface", "vertexai", "palm", "ollama", "bedrock"]):
        return NodeCategory.LLM
    # Check for output parsers
    elif any(keyword in class_name for keyword in ["parser", "outputparser", "jsonoutput", "pydanticoutput", "regexparser", "structuredoutput"]):
        return NodeCategory.OUTPUT_PARSER
    # Check for routers
    elif any(keyword in class_name for keyword in ["router", "multiprompt", "llmrouter"]):
        return NodeCategory.ROUTER
    # Check for document transformers
    elif any(keyword in class_name for keyword in ["documentcompressor", "embeddings_filter", "embeddings_redundant", "llmchainfilter"]):
        return NodeCategory.DOCUMENT_TRANSFORMER
    # Check for other categories
    elif any(keyword in class_name for keyword in ["chain"]):
        return NodeCategory.CHAIN
    elif any(keyword in class_name for keyword in ["agent", "executor"]):
        return NodeCategory.AGENT
    elif any(keyword in class_name for keyword in ["tool"]):
        return NodeCategory.TOOL
    elif any(keyword in class_name for keyword in ["memory", "chatmessagehistory"]):
        return NodeCategory.MEMORY
    elif any(keyword in class_name for keyword in ["prompt", "template", "exampleselector", "messageprompt"]):
        return NodeCategory.PROMPT
    elif any(keyword in class_name for keyword in ["retriever", "contextualcompression", "multiquery", "selfquery", "timeweighted", "webresearch", "ensemble", "parentdocument"]):
        return NodeCategory.RETRIEVER
    elif any(keyword in class_name for keyword in ["vectorstore", "faiss", "chroma", "pinecone", "qdrant", "redis", "weaviate", "milvus", "elasticsearch", "pgvector", "supabase", "mongodb"]):
        return NodeCategory.VECTORSTORE
    elif any(keyword in class_name for keyword in ["embedding", "embeddings", "sentencetransformer", "tensorflowhubeembeddings"]):
        return NodeCategory.EMBEDDING
    elif any(keyword in class_name for keyword in ["document", "loader", "textloader", "pdfloader", "csvloader", "jsonloader", "excelloader", "webbaseloader", "youtubeloader", "directoryloader", "emailloader", "imageloader", "blobloader"]):
        return NodeCategory.DOCUMENT
    elif any(keyword in class_name for keyword in ["splitter", "textsplitter", "charactertextsplitter", "recursivetextsplitter", "tokentextsplitter", "markdowntextsplitter", "htmltextsplitter", "pythoncodetextsplitter", "latextextsplitter"]):
        return NodeCategory.TEXT_SPLITTER
    elif any(keyword in class_name for keyword in ["python", "function", "apiwrapper", "serpapi", "wikipedia", "tavily", "googlesearch", "bingsearch", "searx", "arxiv", "openweathermap", "sqldatabase", "wolframalpha", "zapier", "graphql"]):
        return NodeCategory.UTILITY
    
    # Default to custom
    return NodeCategory.CUSTOM

def get_state_fields_for_node(node_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Get state fields for a specific node.
    
    Args:
        node_data: The node data
        
    Returns:
        Dictionary of state fields for the node
    """
    category = get_node_category(node_data.get("class_path", ""))
    return CATEGORY_STATE_FIELDS.get(category, {})

def generate_node_code(node_name: str, node_data: Dict[str, Any]) -> str:
    """
    Generate code for a node based on its category.
    
    Args:
        node_name: The name of the node
        node_data: The node data
        
    Returns:
        Generated code for the node
    """
    category = get_node_category(node_data.get("class_path", ""))
    generator = CATEGORY_CODE_GENERATORS.get(category)
    
    if generator:
        return generator(node_name, node_data)
    else:
        # Fallback to custom node
        return generate_custom_node_code(node_name, node_data)

# Mapping of Langflow edge conditions to LangGraph conditional edge implementations
def convert_edge_condition(condition: str) -> str:
    """
    Convert a Langflow edge condition to a LangGraph conditional edge implementation.
    
    Args:
        condition: The edge condition from Langflow
        
    Returns:
        LangGraph conditional edge implementation
    """
    import re
    
    # Simple equality condition
    if "==" in condition:
        # Check if it's a string comparison
        string_match = re.search(r'(\w+)\s*==\s*[\'"]([^\'"]*)[\'"]', condition)
        if string_match:
            field = string_match.group(1).strip()
            value = string_match.group(2).strip()
            return f"lambda state: state.get('{field}') == '{value}'"
        
        # Check if it's a numeric or boolean comparison
        numeric_match = re.search(r'(\w+)\s*==\s*([\d\.]+|True|False)', condition)
        if numeric_match:
            field = numeric_match.group(1).strip()
            value = numeric_match.group(2).strip()
            # Convert to appropriate type
            if value == 'True':
                return f"lambda state: state.get('{field}') == True"
            elif value == 'False':
                return f"lambda state: state.get('{field}') == False"
            elif '.' in value:
                return f"lambda state: state.get('{field}') == {value}"
            else:
                return f"lambda state: state.get('{field}') == {value}"
        
        # Default equality handling
        field, value = condition.split("==", 1)
        field = field.strip()
        value = value.strip().strip("'\"")
        return f"lambda state: state.get('{field}') == '{value}'"
    
    # Inequality condition
    elif "!=" in condition:
        field, value = condition.split("!=", 1)
        field = field.strip()
        value = value.strip().strip("'\"")
        if value in ['True', 'False']:
            return f"lambda state: state.get('{field}') != {value}"
        else:
            return f"lambda state: state.get('{field}') != '{value}'"
    
    # Greater than condition
    elif ">" in condition and not ">=" in condition:
        field, value = condition.split(">", 1)
        field = field.strip()
        value = value.strip()
        return f"lambda state: state.get('{field}') > {value}"
    
    # Less than condition
    elif "<" in condition and not "<=" in condition:
        field, value = condition.split("<", 1)
        field = field.strip()
        value = value.strip()
        return f"lambda state: state.get('{field}') < {value}"
    
    # Greater than or equal condition
    elif ">=" in condition:
        field, value = condition.split(">=", 1)
        field = field.strip()
        value = value.strip()
        return f"lambda state: state.get('{field}') >= {value}"
    
    # Less than or equal condition
    elif "<=" in condition:
        field, value = condition.split("<=", 1)
        field = field.strip()
        value = value.strip()
        return f"lambda state: state.get('{field}') <= {value}"
    
    # Contains condition (in)
    elif " in " in condition:
        # Check if it's checking if a value is in a field
        in_match = re.search(r'[\'"](.+?)[\'"](\s+in\s+)(\w+)', condition)
        if in_match:
            value = in_match.group(1).strip()
            field = in_match.group(3).strip()
            return f"lambda state: '{value}' in state.get('{field}', '')"
        # Check if it's checking if a field is in a list of values
        in_list_match = re.search(r'(\w+)(\s+in\s+)\[(.*?)\]', condition)
        if in_list_match:
            field = in_list_match.group(1).strip()
            values = [v.strip().strip("'\"")
                     for v in in_list_match.group(3).split(',')]
            values_str = ", ".join([f"'{v}'" for v in values])
            return f"lambda state: state.get('{field}') in [{values_str}]"
    
    # Logical AND
    elif " and " in condition:
        parts = condition.split(" and ")
        converted_parts = [convert_edge_condition(part.strip()) for part in parts]
        lambda_parts = [part.replace("lambda state: ", "") for part in converted_parts]
        return f"lambda state: {' and '.join(lambda_parts)}"
    
    # Logical OR
    elif " or " in condition:
        parts = condition.split(" or ")
        converted_parts = [convert_edge_condition(part.strip()) for part in parts]
        lambda_parts = [part.replace("lambda state: ", "") for part in converted_parts]
        return f"lambda state: {' or '.join(lambda_parts)}"
    
    # Logical NOT
    elif condition.strip().startswith("not "):
        inner_condition = condition.strip()[4:].strip()
        converted = convert_edge_condition(inner_condition)
        inner_lambda = converted.replace("lambda state: ", "")
        return f"lambda state: not ({inner_lambda})"
    
    # Default to a simple equality check if we can't parse the condition
    return f"lambda state: {condition}"
