#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LangFlow Node Categories
----------------------

This module defines the categories of nodes in LangFlow and their mappings.
"""

# Node Categories
class NodeCategory:
    LLM = "llm"
    CHAIN = "chain"
    AGENT = "agent"
    TOOL = "tool"
    MEMORY = "memory"
    PROMPT = "prompt"
    RETRIEVER = "retriever"
    VECTORSTORE = "vectorstore"
    EMBEDDING = "embedding"
    DOCUMENT = "document"
    TEXT_SPLITTER = "text_splitter"
    UTILITY = "utility"
    CUSTOM = "custom"
    OUTPUT_PARSER = "output_parser"
    ROUTER = "router"
    CHAT_MODEL = "chat_model"
    DOCUMENT_TRANSFORMER = "document_transformer"

# Mapping of Langflow class paths to node categories
LANGFLOW_CLASS_TO_CATEGORY = {
    # LLM Nodes
    "langflow.interface.llms.base": NodeCategory.LLM,
    "langflow.interface.llms.chatmodels": NodeCategory.CHAT_MODEL,
    "langchain.llms.openai.OpenAI": NodeCategory.LLM,
    "langchain.llms.openai.AzureOpenAI": NodeCategory.LLM,
    "langchain.chat_models.openai.ChatOpenAI": NodeCategory.CHAT_MODEL,
    "langchain.chat_models.openai.AzureChatOpenAI": NodeCategory.CHAT_MODEL,
    "langchain.llms.huggingface_hub.HuggingFaceHub": NodeCategory.LLM,
    "langchain.llms.huggingface_pipeline.HuggingFacePipeline": NodeCategory.LLM,
    "langchain.llms.huggingface_endpoint.HuggingFaceEndpoint": NodeCategory.LLM,
    "langchain.llms.anthropic.ChatAnthropic": NodeCategory.CHAT_MODEL,
    "langchain.chat_models.anthropic.ChatAnthropic": NodeCategory.CHAT_MODEL,
    "langchain.llms.cohere.Cohere": NodeCategory.LLM,
    "langchain.chat_models.cohere.ChatCohere": NodeCategory.CHAT_MODEL,
    "langchain.llms.ollama.Ollama": NodeCategory.LLM,
    "langchain.chat_models.ollama.ChatOllama": NodeCategory.CHAT_MODEL,
    "langchain.llms.vertexai.VertexAI": NodeCategory.LLM,
    "langchain.chat_models.vertexai.ChatVertexAI": NodeCategory.CHAT_MODEL,
    "langchain.llms.google_palm.GooglePalm": NodeCategory.LLM,
    "langchain.chat_models.google_palm.ChatGooglePalm": NodeCategory.CHAT_MODEL,

    # Chain Nodes
    "langflow.interface.chains.base": NodeCategory.CHAIN,
    "langchain.chains.llm.LLMChain": NodeCategory.CHAIN,
    "langchain.chains.conversation.ConversationChain": NodeCategory.CHAIN,
    "langchain.chains.qa_with_sources.QAWithSourcesChain": NodeCategory.CHAIN,
    "langchain.chains.retrieval_qa.base.RetrievalQA": NodeCategory.CHAIN,
    "langchain.chains.router.base.RouterChain": NodeCategory.ROUTER,
    "langchain.chains.router.multi_prompt.MultiPromptChain": NodeCategory.ROUTER,
    "langchain.chains.router.llm_router.LLMRouterChain": NodeCategory.ROUTER,
    "langchain.chains.sequential.SequentialChain": NodeCategory.CHAIN,
    "langchain.chains.transform.TransformChain": NodeCategory.CHAIN,
    "langchain.chains.summarize.SummarizeChain": NodeCategory.CHAIN,
    "langchain.chains.mapreduce.MapReduceChain": NodeCategory.CHAIN,
    "langchain.chains.combine_documents.base.BaseCombineDocumentsChain": NodeCategory.CHAIN,
    "langchain.chains.combine_documents.stuff.StuffDocumentsChain": NodeCategory.CHAIN,
    "langchain.chains.combine_documents.map_reduce.MapReduceDocumentsChain": NodeCategory.CHAIN,
    "langchain.chains.combine_documents.refine.RefineDocumentsChain": NodeCategory.CHAIN,
    "langchain.chains.graph_qa.base.GraphQAChain": NodeCategory.CHAIN,
    "langchain.chains.openai_functions.base.create_openai_fn_chain": NodeCategory.CHAIN,
    "langchain.chains.openai_functions.base.create_structured_output_chain": NodeCategory.CHAIN,

    # Agent Nodes
    "langflow.interface.agents.base": NodeCategory.AGENT,
    "langchain.agents.agent.AgentExecutor": NodeCategory.AGENT,
    "langchain.agents.conversational.base.ConversationalAgent": NodeCategory.AGENT,
    "langchain.agents.mrkl.base.ZeroShotAgent": NodeCategory.AGENT,
    "langchain.agents.react.base.ReActAgent": NodeCategory.AGENT,
    "langchain.agents.self_ask_with_search.base.SelfAskWithSearchAgent": NodeCategory.AGENT,
    "langchain.agents.openai_functions_agent.base.OpenAIFunctionsAgent": NodeCategory.AGENT,
    "langchain.agents.openai_functions_multi_agent.base.OpenAIMultiFunctionsAgent": NodeCategory.AGENT,
    "langchain.agents.structured_chat.base.StructuredChatAgent": NodeCategory.AGENT,
    "langchain.agents.agent_toolkits.sql.base.create_sql_agent": NodeCategory.AGENT,
    "langchain.agents.agent_toolkits.json.base.create_json_agent": NodeCategory.AGENT,
    "langchain.agents.agent_toolkits.csv.base.create_csv_agent": NodeCategory.AGENT,
    "langchain.agents.agent_toolkits.vectorstore.base.create_vectorstore_agent": NodeCategory.AGENT,

    # Tool Nodes
    "langflow.interface.tools.base": NodeCategory.TOOL,
    "langchain.tools.base.BaseTool": NodeCategory.TOOL,
    "langchain.tools.python.tool.PythonREPLTool": NodeCategory.TOOL,
    "langchain.tools.requests.tool.RequestsTool": NodeCategory.TOOL,
    "langchain.tools.search.tool.SearchTool": NodeCategory.TOOL,
    "langchain.tools.shell.tool.ShellTool": NodeCategory.TOOL,
    "langchain.tools.bing_search.tool.BingSearchTool": NodeCategory.TOOL,
    "langchain.tools.google_search.tool.GoogleSearchTool": NodeCategory.TOOL,
    "langchain.tools.searx_search.tool.SearxSearchTool": NodeCategory.TOOL,
    "langchain.tools.tavily_search.TavilySearchResults": NodeCategory.TOOL,
    "langchain.tools.arxiv.tool.ArxivQueryRun": NodeCategory.TOOL,
    "langchain.tools.wikipedia.tool.WikipediaQueryRun": NodeCategory.TOOL,
    "langchain.tools.sql_database.tool.QuerySQLDataBaseTool": NodeCategory.TOOL,
    "langchain.tools.openapi.utils.api_models.APIOperation": NodeCategory.TOOL,
    "langchain.tools.json.tool.JsonSpec": NodeCategory.TOOL,
    "langchain.tools.file_management.file.ReadFileTool": NodeCategory.TOOL,
    "langchain.tools.file_management.file.WriteFileTool": NodeCategory.TOOL,
    "langchain.tools.file_management.file.ListDirectoryTool": NodeCategory.TOOL,
    "langchain.tools.human.tool.HumanInputRun": NodeCategory.TOOL,
    
    # Output Parser Nodes
    "langchain.output_parsers.regex.RegexParser": NodeCategory.OUTPUT_PARSER,
    "langchain.output_parsers.pydantic.PydanticOutputParser": NodeCategory.OUTPUT_PARSER,
    "langchain.output_parsers.json.JsonOutputParser": NodeCategory.OUTPUT_PARSER,
    "langchain.output_parsers.structured.StructuredOutputParser": NodeCategory.OUTPUT_PARSER,
    "langchain.output_parsers.format_instructions.StructuredOutputParser": NodeCategory.OUTPUT_PARSER,
    "langchain.output_parsers.openai_functions.JsonOutputFunctionsParser": NodeCategory.OUTPUT_PARSER,
    "langchain.output_parsers.openai_functions.PydanticOutputFunctionsParser": NodeCategory.OUTPUT_PARSER,

    # Memory Nodes
    "langflow.interface.memory.base": NodeCategory.MEMORY,
    "langchain.memory.buffer.ConversationBufferMemory": NodeCategory.MEMORY,
    "langchain.memory.buffer_window.ConversationBufferWindowMemory": NodeCategory.MEMORY,
    "langchain.memory.summary.ConversationSummaryMemory": NodeCategory.MEMORY,
    "langchain.memory.summary_buffer.ConversationSummaryBufferMemory": NodeCategory.MEMORY,
    "langchain.memory.chat_message_histories.in_memory.ChatMessageHistory": NodeCategory.MEMORY,
    "langchain.memory.chat_message_histories.redis.RedisChatMessageHistory": NodeCategory.MEMORY,
    "langchain.memory.chat_message_histories.file.FileChatMessageHistory": NodeCategory.MEMORY,
    "langchain.memory.chat_message_histories.postgres.PostgresChatMessageHistory": NodeCategory.MEMORY,
    "langchain.memory.entity.entity_memory.EntityMemory": NodeCategory.MEMORY,
    "langchain.memory.token_buffer.ConversationTokenBufferMemory": NodeCategory.MEMORY,
    "langchain.memory.combined.CombinedMemory": NodeCategory.MEMORY,
    "langchain.memory.vector_store.VectorStoreRetrieverMemory": NodeCategory.MEMORY,

    # Prompt Nodes
    "langflow.interface.prompts.base": NodeCategory.PROMPT,
    "langchain.prompts.prompt.PromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.chat.ChatPromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.chat.HumanMessagePromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.chat.AIMessagePromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.chat.SystemMessagePromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.few_shot.FewShotPromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.pipeline.PipelinePromptTemplate": NodeCategory.PROMPT,
    "langchain.prompts.example_selector.base.BaseExampleSelector": NodeCategory.PROMPT,
    "langchain.prompts.example_selector.semantic_similarity.SemanticSimilarityExampleSelector": NodeCategory.PROMPT,
    "langchain.prompts.example_selector.length_based.LengthBasedExampleSelector": NodeCategory.PROMPT,
    "langchain.prompts.example_selector.ngram_overlap.NGramOverlapExampleSelector": NodeCategory.PROMPT,
    "langchain.prompts.example_selector.mmr.MaxMarginalRelevanceExampleSelector": NodeCategory.PROMPT,

    # Retriever Nodes
    "langflow.interface.retrievers.base": NodeCategory.RETRIEVER,
    "langchain.retrievers.contextual_compression.ContextualCompressionRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.document_compressors.base.DocumentCompressorRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.document_compressors.base.BaseDocumentCompressor": NodeCategory.DOCUMENT_TRANSFORMER,
    "langchain.retrievers.document_compressors.embeddings_filter.EmbeddingsFilter": NodeCategory.DOCUMENT_TRANSFORMER,
    "langchain.retrievers.document_compressors.embeddings_redundant.EmbeddingsRedundantFilter": NodeCategory.DOCUMENT_TRANSFORMER,
    "langchain.retrievers.document_compressors.llm_filter.LLMChainFilter": NodeCategory.DOCUMENT_TRANSFORMER,
    "langchain.retrievers.multi_query.MultiQueryRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.self_query.base.SelfQueryRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.time_weighted.TimeWeightedVectorStoreRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.web_research.WebResearchRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.ensemble.EnsembleRetriever": NodeCategory.RETRIEVER,
    "langchain.retrievers.parent_document.ParentDocumentRetriever": NodeCategory.RETRIEVER,
    
    # VectorStore Nodes
    "langflow.interface.vectorstores.base": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.chroma.Chroma": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.faiss.FAISS": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.pinecone.Pinecone": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.qdrant.Qdrant": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.redis.Redis": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.weaviate.Weaviate": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.milvus.Milvus": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.elasticsearch.ElasticsearchStore": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.pgvector.PGVector": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.supabase.SupabaseVectorStore": NodeCategory.VECTORSTORE,
    "langchain.vectorstores.mongodb_atlas.MongoDBAtlasVectorSearch": NodeCategory.VECTORSTORE,

    # Embedding Nodes
    "langflow.interface.embeddings.base": NodeCategory.EMBEDDING,
    "langchain.embeddings.openai.OpenAIEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.huggingface.HuggingFaceEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.cohere.CohereEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.vertexai.VertexAIEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.google_palm.GooglePalmEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.ollama.OllamaEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.bedrock.BedrockEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.sentence_transformer.SentenceTransformerEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.tensorflow_hub.TensorflowHubEmbeddings": NodeCategory.EMBEDDING,
    "langchain.embeddings.fake.FakeEmbeddings": NodeCategory.EMBEDDING,
    
    # Document Nodes
    "langflow.interface.document_loaders.base": NodeCategory.DOCUMENT,
    "langchain.document_loaders.text.TextLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.pdf.PyPDFLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.csv_loader.CSVLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.json_loader.JSONLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.excel.UnstructuredExcelLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.web_base.WebBaseLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.youtube.YoutubeLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.directory.DirectoryLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.email.UnstructuredEmailLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.image.UnstructuredImageLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.image_captions.ImageCaptionLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.parsers.pdf.PyPDFParser": NodeCategory.DOCUMENT,
    "langchain.document_loaders.blob_loaders.file_system.FileSystemBlobLoader": NodeCategory.DOCUMENT,
    "langchain.document_loaders.blob_loaders.youtube.YoutubeAudioLoader": NodeCategory.DOCUMENT,
    
    # Text Splitter Nodes
    "langflow.interface.text_splitters.base": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.CharacterTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.RecursiveCharacterTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.TokenTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.SentenceTransformersTokenTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.MarkdownTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.HTMLTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.PythonCodeTextSplitter": NodeCategory.TEXT_SPLITTER,
    "langchain.text_splitter.LatexTextSplitter": NodeCategory.TEXT_SPLITTER,

    # Utility Nodes
    "langflow.interface.utilities.base": NodeCategory.UTILITY,
    "langchain.utilities.python.PythonREPL": NodeCategory.UTILITY,
    "langchain.utilities.serpapi.SerpAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.wikipedia.WikipediaAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.tavily_search.TavilySearchAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.google_search.GoogleSearchAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.bing_search.BingSearchAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.searx_search.SearxSearchWrapper": NodeCategory.UTILITY,
    "langchain.utilities.arxiv.ArxivAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.openweathermap.OpenWeatherMapAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.sql_database.SQLDatabase": NodeCategory.UTILITY,
    "langchain.utilities.wolfram_alpha.WolframAlphaAPIWrapper": NodeCategory.UTILITY,
    "langchain.utilities.zapier.ZapierNLAWrapper": NodeCategory.UTILITY,
    "langchain.utilities.graphql.GraphQLAPIWrapper": NodeCategory.UTILITY,
    
    # Custom Nodes
    "langflow.custom.base": NodeCategory.CUSTOM,
    "langflow.custom.utilities.PythonFunction": NodeCategory.UTILITY,
    "langflow.custom.nodes.CustomNode": NodeCategory.CUSTOM,
    "langflow.custom.nodes.InputNode": NodeCategory.CUSTOM,
    "langflow.custom.nodes.OutputNode": NodeCategory.CUSTOM,
}
