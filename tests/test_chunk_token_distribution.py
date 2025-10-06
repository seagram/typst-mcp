import statistics
import tiktoken
from pathlib import Path
from typst_mcp.ingest import decode_json, extract_relevant_documents, chunk_documents

def main():
    encoding = tiktoken.get_encoding("cl100k_base")
    
    project_root = Path(__file__).parent.parent
    docs_path = project_root / "data" / "docs.json"
    
    documents = decode_json(str(docs_path))
    print(f"Loaded {len(documents)} documents")
    
    relevant_docs = extract_relevant_documents(documents)
    print(f"Found {len(relevant_docs)} relevant documents")
    
    chunks = chunk_documents(relevant_docs)
    print(f"Created {len(chunks)} chunks")
    
    chunk_token_lengths = [len(encoding.encode(chunk.content)) for chunk in chunks]
    chunk_char_lengths = [len(chunk.content) for chunk in chunks]
    
    print(f"\nTotal chunks: {len(chunks)}")
    print(f"Total tokens: {sum(chunk_token_lengths):,}")
    print(f"Total characters: {sum(chunk_char_lengths):,}")
    print(f"Average token/char ratio: {sum(chunk_token_lengths) / sum(chunk_char_lengths):.3f}")
    print("\nToken Statistics:")
    print(f"    Average length: {statistics.mean(chunk_token_lengths):.2f} tokens")
    print(f"    Median length: {statistics.median(chunk_token_lengths):.2f} tokens")
    print(f"    Shortest chunk: {min(chunk_token_lengths):,} tokens")
    print(f"    Longest chunk: {max(chunk_token_lengths):,} tokens")
    print(f"    Standard deviation: {statistics.stdev(chunk_token_lengths):.2f}")
    
    sorted_lengths = sorted(chunk_token_lengths)
    p25 = sorted_lengths[len(sorted_lengths) // 4]
    p75 = sorted_lengths[3 * len(sorted_lengths) // 4]
    p90 = sorted_lengths[9 * len(sorted_lengths) // 10]
    p95 = sorted_lengths[19 * len(sorted_lengths) // 20]
    
    print("\nPercentile Distribution:")
    print(f"  25th percentile: {p25:,} tokens")
    print(f"  75th percentile: {p75:,} tokens")
    print(f"  90th percentile: {p90:,} tokens")
    print(f"  95th percentile: {p95:,} tokens")
    
    print("\n Statistics by Document Type:")
    type_stats = {}
    for i, chunk in enumerate(chunks):
        doc_type = chunk.metadata.document_type
        if doc_type not in type_stats:
            type_stats[doc_type] = []
        type_stats[doc_type].append(chunk_token_lengths[i])
    
    for doc_type, lengths in sorted(type_stats.items()):
        print(f"\n  {doc_type.upper()}:")
        print(f"    Count: {len(lengths)}")
        print(f"    Total tokens: {sum(lengths):,}")
        print(f"    Average: {statistics.mean(lengths):.2f} tokens")
        print(f"    Min: {min(lengths):,} tokens")
        print(f"    Max: {max(lengths):,} tokens")
    
    print("\n Statistics by Part (Top 10 by count):")
    part_stats = {}
    for i, chunk in enumerate(chunks):
        part = chunk.metadata.part
        if part not in part_stats:
            part_stats[part] = []
        part_stats[part].append(chunk_token_lengths[i])
    
    sorted_parts = sorted(part_stats.items(), key=lambda x: len(x[1]), reverse=True)
    for part, lengths in sorted_parts[:10]:
        print(f"\n  {part}:")
        print(f"    Count: {len(lengths)}")
        print(f"    Average: {statistics.mean(lengths):.2f} tokens")
    
    print("\n Token Distribution (bins):")
    bins = {
        "0-500": 0,
        "500-2K": 0,
        "2K-5K": 0,
        "5K-10K": 0,
        "10K-20K": 0,
        "20K+": 0
    }
    
    for length in chunk_token_lengths:
        if length < 500:
            bins["0-500"] += 1
        elif length < 2000:
            bins["500-2K"] += 1
        elif length < 5000:
            bins["2K-5K"] += 1
        elif length < 10000:
            bins["5K-10K"] += 1
        elif length < 20000:
            bins["10K-20K"] += 1
        else:
            bins["20K+"] += 1
    
    for bin_name, count in bins.items():
        percentage = (count / len(chunks)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {bin_name:10s}: {count:4d} ({percentage:5.1f}%) {bar}")
    
    shortest_idx = chunk_token_lengths.index(min(chunk_token_lengths))
    longest_idx = chunk_token_lengths.index(max(chunk_token_lengths))
    
    print("\n Shortest Chunk:")
    print(f"  Title: {chunks[shortest_idx].metadata.title}")
    print(f"  Route: {chunks[shortest_idx].metadata.route}")
    print(f"  Type: {chunks[shortest_idx].metadata.document_type}")
    print(f"  Length: {chunk_token_lengths[shortest_idx]:,} tokens ({chunk_char_lengths[shortest_idx]:,} chars)")
    
    print("\n Longest Chunk:")
    print(f"  Title: {chunks[longest_idx].metadata.title}")
    print(f"  Route: {chunks[longest_idx].metadata.route}")
    print(f"  Type: {chunks[longest_idx].metadata.document_type}")
    print(f"  Length: {chunk_token_lengths[longest_idx]:,} tokens ({chunk_char_lengths[longest_idx]:,} chars)")

    return chunks


if __name__ == "__main__":
    chunks = main()
