import chromadb

def create_chroma_client():
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="typst-mcp")

# TODO
