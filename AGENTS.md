# PROJECT DESCRIPTION

This repo contains the code for an open-source MCP Server for the Typst markup language.
The general process of the server is as follows:

1. Takes the Typst documentation from `data/docs.json` (structured JSON format)
2. Parses the JSON to extract documents with their metadata (route, title, description, part, outline)
3. Chunks documents semantically using the outline structure (sections/subsections)
4. Uses an embedding model to generate vectors for each chunk
5. Saves all vectors in a Chroma Database along with rich metadata
6. A user can then make a query which hits a FastAPI endpoint which will use RAG

# Key Technologies Used

- Python 3.10
- uv package manager
- FastAPI
- Chroma DB
- torch
- SentenceTransformer
- Snowflake Artic Embed Model

# Documentation Data Structure

## Source: `data/docs.json`

- **Format**: Hierarchical JSON with 187 documents (~628K characters of HTML content)
- **Total markdown files**: 301 files with ~80K lines (for reference, but JSON is primary source)

## JSON Structure

Each document entry contains:

- `route`: Path in docs hierarchy (e.g., `/DOCS-BASE/reference/foundations/int/`)
- `title`: Document title (e.g., "Integer", "Array")
- `description`: Brief summary of the document
- `part`: Category (e.g., "Language", "Foundations", "Functions")
- `outline`: Hierarchical table of contents with section IDs
- `body`: HTML content with semantic markup
- `children`: Nested child documents

## Chunking Strategy

### Implementation Approach:

1. **Parse JSON hierarchy**: Traverse the nested document structure
2. **Extract metadata**: Capture route, title, part, description for each doc
3. **Semantic chunking**:
   - Use `outline` field to identify logical sections
   - Split large documents by sections/subsections
   - Keep smaller documents as single chunks
4. **HTML to text**: Convert HTML content while preserving structure
5. **Store in ChromaDB**: Include metadata with each chunk:
   ```python
   {
     "text": chunk_content,
     "metadata": {
       "route": "/DOCS-BASE/reference/foundations/int/",
       "title": "Integer",
       "part": "Foundations",
       "section_id": "definitions-signum",
       "section_name": "Signum",
       "doc_type": "reference"  # tutorial, reference, guide, changelog
     }
   }
   ```

### Benefits for Users:

- **Precise citations**: "Found in Reference > Foundations > Integer > Signum"
- **Direct links**: Can link to exact section in Typst docs
- **Filtered search**: Query by doc type (reference vs tutorial)
- **Better context**: Understand where information comes from
- **Accurate results**: Semantically coherent chunks improve retrieval
