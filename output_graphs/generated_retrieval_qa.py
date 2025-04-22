from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    input: str
    documents: List[Dict[str, Any]]
    context: str
    prompt: str
    llm_response: str
    output: Dict[str, Any]

def create_graph():
    # Define the graph with proper state schema
    graph = StateGraph(GraphState)

    def node_input_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "input" in state:
            state["output"] = {"query": state["input"]}
        return state
    graph.add_node("node_input_node", node_input_node)

    def node_document_node(state):
        """Process the state by loading documents."""
        # Document loader implementation: TextLoader
        if "file_path" in state:
            # In a real implementation, this would load a document
            state["document_content"] = f"Content loaded from {state['file_path']}"
        # For demonstration, we'll use a hardcoded document
        state["documents"] = [
            {"content": "LangGraph is a library for building stateful, multi-actor applications with LLMs, built on top of LangChain.", "metadata": {}},
            {"content": "LangGraph provides a way to implement stateful, multi-actor applications with LLMs. It is built on top of LangChain, and is designed to be used with it.", "metadata": {}}
        ]
        return state
    graph.add_node("node_document_node", node_document_node)

    def node_text_splitter_node(state):
        """Process the state by splitting text into chunks."""
        # Text splitter implementation: CharacterTextSplitter
        # Chunk size: 1000
        if "documents" in state:
            # In a real implementation, this would split the documents
            # For demonstration, we'll just use the documents as is
            state["chunks"] = state["documents"]
        return state
    graph.add_node("node_text_splitter_node", node_text_splitter_node)

    def node_embedding_node(state):
        """Process the state by generating embeddings."""
        # Embedding implementation: OpenAIEmbeddings
        if "chunks" in state:
            # In a real implementation, this would generate embeddings
            # For demonstration, we'll just use dummy embeddings
            state["embeddings"] = [[0.1, 0.2, 0.3]]  # Mock embedding vector
        return state
    graph.add_node("node_embedding_node", node_embedding_node)

    def node_vectorstore_node(state):
        """Process the state by searching a vector store."""
        # VectorStore implementation: Chroma
        if "chunks" in state and "embeddings" in state:
            # In a real implementation, this would create a vector store
            # For demonstration, we'll just use the chunks as is
            state["vectorstore"] = {"chunks": state["chunks"], "embeddings": state["embeddings"]}
        return state
    graph.add_node("node_vectorstore_node", node_vectorstore_node)

    def node_retriever_node(state):
        """Process the state by retrieving documents."""
        # Retriever implementation: VectorStoreRetriever
        if "input" in state and "vectorstore" in state:
            # In a real implementation, this would retrieve documents
            # For demonstration, we'll just use the chunks from the vector store
            state["documents"] = state["vectorstore"]["chunks"]
        return state
    graph.add_node("node_retriever_node", node_retriever_node)

    def node_context_formatter(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "documents" in state:
            # Format the documents into a context string
            context = "\n\n".join([doc["content"] for doc in state["documents"]])
            state["context"] = context
        return state
    graph.add_node("node_context_formatter", node_context_formatter)

    def node_prompt_node(state):
        """Process the state by formatting a prompt template."""
        # Prompt template implementation
        template = "Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\nContext:\n{context}\n\nQuestion: {input}\n\nAnswer:"
        # Format the template with state variables
        formatted_prompt = template
        # Format with state variables
        if "context" in state and "input" in state:
            formatted_prompt = template.format(context=state["context"], input=state["input"])
        state["prompt"] = formatted_prompt
        return state
    graph.add_node("node_prompt_node", node_prompt_node)

    def node_llm_node(state):
        """Process the state using an LLM."""
        # LLM implementation
        # Model: gpt-3.5-turbo-instruct, Temperature: 0.3
        if "prompt" in state:
            # In a real implementation, this would call the LLM
            state["llm_response"] = f"Response to: {state['prompt']}"
        elif "input" in state:
            state["llm_response"] = f"Response to: {state['input']}"
        else:
            state["llm_response"] = "No input provided"
        return state
    graph.add_node("node_llm_node", node_llm_node)

    def node_output_node(state):
        """Process the state with custom logic."""
        # Custom node implementation
        if "llm_response" in state:
            state["output"] = {
                "answer": state["llm_response"],
                "sources": [doc["content"] for doc in state.get("documents", [])]
            }
        return state
    graph.add_node("node_output_node", node_output_node)

    # --- Edges ---
    graph.add_edge("node_input_node", "node_retriever_node")
    graph.add_edge("node_document_node", "node_text_splitter_node")
    graph.add_edge("node_text_splitter_node", "node_vectorstore_node")
    graph.add_edge("node_embedding_node", "node_vectorstore_node")
    graph.add_edge("node_vectorstore_node", "node_retriever_node")
    graph.add_edge("node_retriever_node", "node_context_formatter")
    graph.add_edge("node_context_formatter", "node_prompt_node")
    graph.add_edge("node_input_node", "node_prompt_node")
    graph.add_edge("node_prompt_node", "node_llm_node")
    graph.add_edge("node_llm_node", "node_output_node")

    # --- Entry and Finish ---
    graph.set_entry_point("node_document_node")
    graph.set_finish_point("node_output_node")

    return graph.compile()

if __name__ == "__main__":
    app = create_graph()
    result = app.invoke({"input": "What is LangGraph?"})
    print(result)
