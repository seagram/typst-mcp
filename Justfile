test:
    PYTHONPATH=src uv run python tests/test_chunk_token_distribution.py

ingest:
    uv run python -m typst_mcp.ingest
