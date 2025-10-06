# typst-mcp

> [!WARNING]
> Early alpha - some features are incomplete or unstable

A Model Context Protocol (MCP) server that gives LLMs semantic search over the official Typst documentation.

## How it works

- Chunks the entire Typst documentation (5.5MB) into semantic segments with metadata
- Generates embeddings using a local embedding model
- Stores vectors in a database for similarity searching
- Exposes MCP tools for LLM queries

## Installation

### Docker

```bash
# Coming soon...
```

### uv (Python)

```bash
# Coming soon...
```

## Tools

The server exposes the following tools:

- `search_typst_docs` - Semantic search across Typst documenation
- `get_function_signature` - Retrieve function signature and parameters
- `find_examples` - Get code examples for certain features
- `get_syntax_reference` - Look up markup syntax rules

## Roadmap

- [ ] Documentation parsing and chunking
- [ ] Vector database storage with metadata indexing
- [ ] Generate embeddings for documentation chunks
- [ ] Retrieval system with similarity search
- [ ] All MCP tool endpoints
- [ ] Unit and integration tests
- [ ] Benchmark query latency and accuracy
- [ ] Query result caching layer
- [ ] Support custom embedding models
- [ ] CLI for server configuration
