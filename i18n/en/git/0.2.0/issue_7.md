# EMBEDDINGS AND FAISS FOR ENHANCED CONTEXTUAL MANAGEMENT [#7]

## Objective
Integrate an embeddings and vector management module using FAISS to improve the chat agent’s ability to handle and enrich context. This will enable the agent to store, retrieve, and use vectorized representations of data, allowing for smarter and more context-aware responses.

## Proposed Solution

### 1. Integration of the Embeddings Module
- Develop a module to generate text embeddings using pre-trained models  
- Make the module configurable (model selection, dimensionality, etc.)  
- Create an interface similar to `gemini_client` to abstract complexity  

### 2. Implementation of Vector Management with FAISS
- Use FAISS for storage and management of embeddings  
- Implement key functionalities:
  - Add new embeddings to the vector store  
  - Search for the most relevant embeddings by similarity  
  - Delete obsolete or irrelevant embeddings  
- Consider persistence strategies and metadata handling  

### 3. Improved Context Handling
- Modify the chat agent to query the vector database  
- Enrich the current context with retrieved relevant information  
- Update the `ContextManager` to incorporate retrieved data  

### 4. Performance Optimization
- Ensure vector search remains efficient even with large datasets  
- Implement batching or caching mechanisms as needed  
- Consider FAISS index strategies based on data volume  

## Proposed Structure

```
src/
  embeddings/
    embeddings_client.py   # Client for generating embeddings
    vector_store.py        # FAISS index management
    utils.py               # Auxiliary functions
  models/
    vector_data.py         # Models for metadata and results
  context/
    context_enrichment.py  # Logic for context enrichment
```

## Configuration Schema Modifications

```yaml
# New sections to be added in AbioConfig
embeddings:
  provider: "openai"  # Alternatives: "gemini", "huggingface"
  model: "text-embedding-3-small"
  dimensions: 1536
  
vector_store:
  type: "faiss"
  index_type: "IndexFlatL2"  # Alternatives: "IndexIVFFlat", "IndexHNSW"
  path: "./data/vector_store"
  metadata_db: "./data/metadata.db"
  top_k: 5  # Default number of results to retrieve
```

## Workflow

1. User sends a query  
2. An embedding is generated for the query  
3. Similar vectors are searched in the FAISS store  
4. Associated metadata (original text) is retrieved  
5. Current context is enriched with the retrieved information  
6. A response is generated using the enriched context  

## Expected Benefits

- Significant improvement in the quality and relevance of responses  
- Ability to incorporate specific knowledge into conversations  
- Modular and reusable system for vectorization and retrieval  
- Greater scalability for handling large volumes of information  

## Next Steps

1. Implement the embeddings client with multi-provider support  
2. Develop the FAISS-based vector management module  
3. Integrate vector retrieval into the conversation flow  
4. Write unit and integration tests  
5. Evaluate performance and response quality  

## References

- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)  
- [HuggingFace Transformers](https://huggingface.co/docs/transformers/index)  
- [OpenAI Embeddings API](https://platform.openai.com/docs/guides/embeddings)  

## Priority
High 

## Progress Journal

### April 2025 — Implementation Updates

#### 1. Refined Architecture: Removed `vector_store.py`, Introduced `faiss` Module

- **Decision:**  
  The initial plan proposed a `vector_store.py` inside `embeddings/`. After further analysis, I decided to move all FAISS-related logic to a dedicated `faiss/` package for better separation of concerns and future extensibility.
- **Action:**  
  - **Removed:** `src/embeddings/vector_store.py` (no longer needed).
  - **Created:** `src/faiss/faiss_manager.py` as the main entry point for FAISS index management.
  - **Created:** `src/faiss/__init__.py` (empty for now, enables package import).
- **Rationale:**  
  This change clarifies the boundaries between embedding generation (handled in `embeddings/`) and vector index management (handled in `faiss/`). It also aligns with the project’s modular design.

#### 2. FAISS Manager Module

- **Implemented:**  
  - [`FAISSManager`](src/faiss/faiss_manager.py):  
    - Handles index creation, addition of embeddings, similarity search, and index reset.
    - Keeps a mapping between embeddings and their original texts for retrieval.
    - Provides methods for adding, searching, and clearing the index.
- **Benefits:**  
  - Encapsulates all FAISS logic in one place.
  - Simplifies future enhancements (e.g., persistence, metadata, advanced index types).

#### 3. Embeddings Generator

- **Status:**  
  - [`EmbeddingsGenerator`](src/embeddings/embeddings_generator.py) is implemented and provides text-to-vector transformation using SentenceTransformers.
  - Supports preprocessing and segmentation of long texts.

#### 4. Integration Plan

- Next steps involve integrating `FAISSManager` with the context management flow, so that relevant context can be retrieved and injected into the chat session dynamically.

---

### Summary of Changes

- **Removed:** `src/embeddings/vector_store.py`
- **Added:** `src/faiss/faiss_manager.py` and `src/faiss/__init__.py`
- **Updated:** Architecture documentation and references to use the new `faiss` module.

---

## Next Steps

1. Integrate `FAISSManager` into the context enrichment workflow.
2. Add persistence and metadata support to the FAISS module if needed.
3. Update configuration models to reflect the new structure.
4. Write unit tests for the new FAISS module.
