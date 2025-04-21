#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow to LangGraph Node Type Mappings
----------------------------------------

This module contains mappings and implementations for converting different
LangFlow node types to their LangGraph equivalents.
"""

from typing import Dict, Any, List, Optional, Callable

# Node type categories
PROMPT_NODES = [
    "PromptTemplate", 
    "ChatPromptTemplate", 
    "FewShotPromptTemplate",
    "PromptNode"
]

LLM_NODES = [
    "LLM", 
    "ChatModel", 
    "OpenAI", 
    "ChatOpenAI", 
    "HuggingFaceHub",
    "LLMNode"
]

CHAIN_NODES = [
    "LLMChain", 
    "SequentialChain", 
    "TransformChain", 
    "RouterChain",
    "ChainNode"
]

MEMORY_NODES = [
    "ConversationBufferMemory", 
    "ConversationBufferWindowMemory", 
    "ConversationSummaryMemory",
    "MemoryNode"
]

AGENT_NODES = [
    "ZeroShotAgent", 
    "ConversationalAgent", 
    "AgentExecutor",
    "AgentNode"
]

TOOL_NODES = [
    "Tool", 
    "BaseTool", 
    "RequestsTool", 
    "PythonFunctionTool",
    "ToolNode"
]

RETRIEVER_NODES = [
    "VectorStoreRetriever", 
    "ContextualCompressionRetriever",
    "RetrieverNode"
]

VECTORSTORE_NODES = [
    "FAISS", 
    "Chroma", 
    "Pinecone",
    "VectorStoreNode"
]

TEXT_SPLITTER_NODES = [
    "CharacterTextSplitter", 
    "RecursiveCharacterTextSplitter", 
    "TokenTextSplitter",
    "TextSplitterNode"
]

DOCUMENT_NODES = [
    "Document", 
    "TextLoader", 
    "PyPDFLoader", 
    "WebBaseLoader",
    "DocumentNode"
]

UTILITY_NODES = [
    "PythonFunction", 
    "StringFormatter", 
    "JsonFormatter",
    "UtilityNode"
]

# Node implementation templates
def generate_prompt_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a prompt node"""
    template = node.get("inputs", {}).get("template", "")
    if not template:
        template = node.get("inputs", {}).get("prompt", "")
    
    code = [
        f"    def {node_name}(state):",
        f"        # Prompt template implementation",
        f"        template = \"\"\"{template}\"\"\"",
        f"        # Format the template with state variables",
        f"        formatted_prompt = template",
        f"        # Extract variables from the template",
        f"        import re",
        f"        variables = re.findall(r'{{([^{{}}]+)}}', template)",
        f"        # Replace variables with values from state",
        f"        for var in variables:",
        f"            var_clean = var.strip()",
        f"            if var_clean in state:",
        f"                formatted_prompt = formatted_prompt.replace('{{{{' + var + '}}}}', str(state[var_clean]))",
        f"        state[\"prompt\"] = formatted_prompt",
        f"        return state"
    ]
    return code

def generate_llm_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for an LLM node"""
    model = node.get("inputs", {}).get("model_name", "")
    temperature = node.get("inputs", {}).get("temperature", 0.7)
    
    code = [
        f"    def {node_name}(state):",
        f"        # LLM implementation",
        f"        # Model: {model}, Temperature: {temperature}",
        f"        if \"prompt\" in state:",
        f"            # In a real implementation, this would call the LLM",
        f"            state[\"llm_response\"] = f\"Response to: {{state['prompt']}}\"",
        f"        elif \"input\" in state:",
        f"            state[\"llm_response\"] = f\"Response to: {{state['input']}}\"",
        f"        else:",
        f"            state[\"llm_response\"] = \"No input provided\"",
        f"        return state"
    ]
    return code

def generate_chain_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a chain node"""
    code = [
        f"    def {node_name}(state):",
        f"        # Chain implementation",
        f"        # This would typically combine multiple components",
        f"        if \"input\" in state:",
        f"            state[\"chain_result\"] = f\"Chain processed: {{state['input']}}\"",
        f"        return state"
    ]
    return code

def generate_memory_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a memory node"""
    memory_type = node.get("class_path", "").split(".")[-1]
    
    code = [
        f"    def {node_name}(state):",
        f"        # Memory implementation ({memory_type})",
        f"        if \"history\" not in state:",
        f"            state[\"history\"] = []",
        f"        if \"input\" in state and \"llm_response\" in state:",
        f"            # Add the current exchange to history",
        f"            state[\"history\"].append((state[\"input\"], state[\"llm_response\"]))",
        f"        return state"
    ]
    return code

def generate_agent_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for an agent node"""
    code = [
        f"    def {node_name}(state):",
        f"        # Agent implementation",
        f"        if \"input\" in state:",
        f"            # In a real implementation, this would use tools and reasoning",
        f"            state[\"agent_result\"] = f\"Agent processed: {{state['input']}}\"",
        f"            state[\"intermediate_steps\"] = [\"Step 1: Thinking\", \"Step 2: Acting\"]",
        f"        return state"
    ]
    return code

def generate_tool_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a tool node"""
    tool_name = node.get("data", {}).get("label", node_name)
    
    code = [
        f"    def {node_name}(state):",
        f"        # Tool implementation: {tool_name}",
        f"        if \"input\" in state:",
        f"            state[\"tool_result\"] = f\"Tool {tool_name} executed on: {{state['input']}}\"",
        f"        return state"
    ]
    return code

def generate_retriever_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a retriever node"""
    code = [
        f"    def {node_name}(state):",
        f"        # Retriever implementation",
        f"        if \"input\" in state:",
        f"            # In a real implementation, this would retrieve documents",
        f"            state[\"documents\"] = [",
        f"                {{\"content\": f\"Document 1 relevant to {{state['input']}}\", \"metadata\": {{}}}},",
        f"                {{\"content\": f\"Document 2 relevant to {{state['input']}}\", \"metadata\": {{}}}}",
        f"            ]",
        f"        return state"
    ]
    return code

def generate_vectorstore_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a vector store node"""
    code = [
        f"    def {node_name}(state):",
        f"        # Vector store implementation",
        f"        if \"input\" in state:",
        f"            # In a real implementation, this would search a vector store",
        f"            state[\"search_results\"] = [",
        f"                {{\"content\": f\"Result 1 for {{state['input']}}\", \"metadata\": {{}}}},",
        f"                {{\"content\": f\"Result 2 for {{state['input']}}\", \"metadata\": {{}}}}",
        f"            ]",
        f"        return state"
    ]
    return code

def generate_text_splitter_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a text splitter node"""
    chunk_size = node.get("inputs", {}).get("chunk_size", 1000)
    
    code = [
        f"    def {node_name}(state):",
        f"        # Text splitter implementation (chunk_size: {chunk_size})",
        f"        if \"input\" in state and isinstance(state[\"input\"], str):",
        f"            # Simple splitting by paragraphs for demonstration",
        f"            paragraphs = state[\"input\"].split(\"\\n\\n\")",
        f"            state[\"chunks\"] = [p for p in paragraphs if p.strip()]",
        f"        return state"
    ]
    return code

def generate_document_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a document node"""
    code = [
        f"    def {node_name}(state):",
        f"        # Document loader implementation",
        f"        if \"file_path\" in state:",
        f"            # In a real implementation, this would load a document",
        f"            state[\"document_content\"] = f\"Content loaded from {{state['file_path']}}\"",
        f"        return state"
    ]
    return code

def generate_utility_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a utility node"""
    code = [
        f"    def {node_name}(state):",
        f"        # Utility function implementation",
        f"        if \"input\" in state:",
        f"            state[\"processed_input\"] = state[\"input\"].upper()",
        f"        return state"
    ]
    return code

# Node type to implementation mapping
NODE_TYPE_IMPLEMENTATIONS: Dict[str, Callable] = {
    "prompt": generate_prompt_node_code,
    "llm": generate_llm_node_code,
    "chain": generate_chain_node_code,
    "memory": generate_memory_node_code,
    "agent": generate_agent_node_code,
    "tool": generate_tool_node_code,
    "retriever": generate_retriever_node_code,
    "vectorstore": generate_vectorstore_node_code,
    "text_splitter": generate_text_splitter_node_code,
    "document": generate_document_node_code,
    "utility": generate_utility_node_code
}

def get_node_type(class_path: str) -> str:
    """Determine the node type from the class path"""
    if not class_path:
        return "utility"
        
    class_name = class_path.split(".")[-1]
    
    if any(node_type in class_name for node_type in PROMPT_NODES):
        return "prompt"
    elif any(node_type in class_name for node_type in LLM_NODES):
        return "llm"
    elif any(node_type in class_name for node_type in CHAIN_NODES):
        return "chain"
    elif any(node_type in class_name for node_type in MEMORY_NODES):
        return "memory"
    elif any(node_type in class_name for node_type in AGENT_NODES):
        return "agent"
    elif any(node_type in class_name for node_type in TOOL_NODES):
        return "tool"
    elif any(node_type in class_name for node_type in RETRIEVER_NODES):
        return "retriever"
    elif any(node_type in class_name for node_type in VECTORSTORE_NODES):
        return "vectorstore"
    elif any(node_type in class_name for node_type in TEXT_SPLITTER_NODES):
        return "text_splitter"
    elif any(node_type in class_name for node_type in DOCUMENT_NODES):
        return "document"
    elif any(node_type in class_name for node_type in UTILITY_NODES):
        return "utility"
    
    # Default to utility for unknown node types
    return "utility"

def generate_node_code(node: Dict[str, Any], node_name: str) -> List[str]:
    """Generate code for a node based on its type"""
    class_path = node.get("class_path", "")
    node_type = get_node_type(class_path)
    
    if node_type in NODE_TYPE_IMPLEMENTATIONS:
        return NODE_TYPE_IMPLEMENTATIONS[node_type](node, node_name)
    
    # Fallback for unknown node types
    return [
        f"    def {node_name}(state):",
        f"        # Unknown node type implementation for {class_path}",
        f"        # TODO: Implement specific logic for this node type",
        f"        return state"
    ]
