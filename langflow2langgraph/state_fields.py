#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow State Fields
-------------------

This module defines the state fields for different node categories.
"""

from langflow2langgraph.node_categories import NodeCategory

# State field mappings for different node categories
CATEGORY_STATE_FIELDS = {
    NodeCategory.LLM: {
        "input": "str",
        "llm_response": "str",
    },
    NodeCategory.CHAT_MODEL: {
        "input": "str",
        "messages": "list",
        "chat_response": "str",
    },
    NodeCategory.CHAIN: {
        "input": "str",
        "chain_result": "str",
    },
    NodeCategory.AGENT: {
        "input": "str",
        "agent_result": "str",
        "intermediate_steps": "list",
        "tools": "list",
    },
    NodeCategory.TOOL: {
        "input": "str",
        "tool_result": "str",
    },
    NodeCategory.MEMORY: {
        "input": "str",
        "history": "list",
        "memory_result": "str",
        "chat_history": "list",
    },
    NodeCategory.PROMPT: {
        "input": "str",
        "prompt": "str",
        "template": "str",
        "variables": "dict",
    },
    NodeCategory.RETRIEVER: {
        "input": "str",
        "query": "str",
        "documents": "list",
    },
    NodeCategory.VECTORSTORE: {
        "input": "str",
        "search_results": "list",
        "documents": "list",
        "query": "str",
    },
    NodeCategory.EMBEDDING: {
        "input": "str",
        "embeddings": "list",
        "texts": "list",
    },
    NodeCategory.DOCUMENT: {
        "file_path": "str",
        "document_content": "str",
        "documents": "list",
    },
    NodeCategory.TEXT_SPLITTER: {
        "input": "str",
        "chunks": "list",
        "documents": "list",
    },
    NodeCategory.UTILITY: {
        "input": "str",
        "processed_input": "str",
        "result": "str",
    },
    NodeCategory.CUSTOM: {
        "input": "str",
        "output": "str",
    },
    NodeCategory.OUTPUT_PARSER: {
        "input": "str",
        "parsed_output": "dict",
        "format_instructions": "str",
    },
    NodeCategory.ROUTER: {
        "input": "str",
        "destination": "str",
        "route": "str",
    },
    NodeCategory.DOCUMENT_TRANSFORMER: {
        "documents": "list",
        "transformed_documents": "list",
    },
}
