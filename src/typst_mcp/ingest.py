import msgspec
import msgspec.json
import html2text
from typing import Optional, List, Union, Dict, Any


class OutlineItem(msgspec.Struct):
    id: str
    name: str
    children: List["OutlineItem"]

class DocumentBody(msgspec.Struct):
    kind: str
    content: Union[str, Dict[str, Any]]

class Document(msgspec.Struct):
    route: str
    title: str
    description: Optional[str]
    part: Optional[str]
    outline: List[OutlineItem]
    body: DocumentBody
    children: List["Document"]

class DocumentMetadata(msgspec.Struct):
    route: str
    title: str
    description: Optional[str]
    part: Optional[str]
    document_type: str

class DocumentChunk(msgspec.Struct):
    content: str
    metadata: DocumentMetadata

def decode_json(filepath: str) -> List[Document]:
    with open(filepath, "rb") as f:
        documents: List[Document] = msgspec.json.decode(f.read(), type=List[Document])
    return documents


def extract_relevant_documents(documents: List[Document]) -> List[Document]:
    base_dir: str = "/DOCS-BASE/"
    sub_dirs: List[str] = ["tutorial/", "reference/", "guides/"]
    relevant_documents: List[Document] = []
    for document in documents:
        if document.route.startswith(tuple(f"{base_dir}{subdir}" for subdir in sub_dirs)):
            relevant_documents.append(document)
    return relevant_documents

def is_html(body: DocumentBody) -> bool:
    if body.kind == "html" and isinstance(body.content, str):
        return True
    return False

def extract_text_from_body(body: DocumentBody, html: html2text.HTML2Text) -> str:
    if is_html(body):
        return html.handle(body.content)  # type: ignore
    return str(body.content)

def chunk_symbols_list(document: Document, symbols_data: Dict[str, Any]) -> List[DocumentChunk]:
    chunks = []
    
    if "list" not in symbols_data or not isinstance(symbols_data["list"], list):
        return chunks
    
    symbols_list = symbols_data["list"]
    name = symbols_data.get("name", "symbols")
    title = symbols_data.get("title", "Symbols")
    details = symbols_data.get("details", "")
    
    html = html2text.HTML2Text()
    html.ignore_links = False
    html.body_width = 0
    html.ignore_images = True
    details_text = html.handle(details) if details else ""
    
    for symbol in symbols_list:
        symbol_name = symbol.get("name", "unknown")
        codepoint = symbol.get("codepoint", "")
        math_class = symbol.get("mathClass", "")
        markup_shorthand = symbol.get("markupShorthand", "")
        math_shorthand = symbol.get("mathShorthand", "")
        
        content_parts = [
            f"Symbol: {symbol_name}",
            f"Category: {title}",
            f"Collection: {name}",
        ]
        
        if codepoint:
            try:
                char = chr(codepoint)
                content_parts.append(f"Character: {char} (U+{codepoint:04X})")
            except (ValueError, OverflowError):
                content_parts.append(f"Codepoint: {codepoint}")
        
        if math_class:
            content_parts.append(f"Math class: {math_class}")
        
        if markup_shorthand:
            content_parts.append(f"Markup shorthand: {markup_shorthand}")
        
        if math_shorthand:
            content_parts.append(f"Math shorthand: {math_shorthand}")
        
        if details_text:
            content_parts.append(f"\nAbout {title} symbols:\n{details_text}")
        
        content = "\n".join(content_parts)
        
        metadata = DocumentMetadata(
            route=f"{document.route}#{symbol_name}",
            title=f"{title}: {symbol_name}",
            description=f"Symbol {symbol_name} from {name} collection",
            part=document.part or "Symbols",
            document_type="symbol"
        )
        
        chunk = DocumentChunk(content=content, metadata=metadata)
        chunks.append(chunk)
    
    return chunks

def chunk_documents(documents: List[Document]) -> List[DocumentChunk]:
    document_chunks: List[DocumentChunk] = []

    html = html2text.HTML2Text()
    html.ignore_links = False
    html.body_width = 0
    html.ignore_images = True

    def extract_document_type(route: str) -> str:
        if "/tutorial/" in route:
            return "tutorial"
        elif "/reference/" in route:
            return "reference"
        elif "/guides/" in route:
            return "guides"
        return "other"

    def process_document(document: Document):
        if document.children:
            for child in document.children:
                process_document(child)
        else:
            if document.body.kind == "symbols" and isinstance(document.body.content, dict):
                symbol_chunks = chunk_symbols_list(document, document.body.content)
                document_chunks.extend(symbol_chunks)
            else:
                body_text = extract_text_from_body(document.body, html)
                metadata = DocumentMetadata(
                    route=document.route,
                    title=document.title,
                    description=document.description,
                    part=document.part or "Unknown",
                    document_type=extract_document_type(document.route)
                )
                chunk = DocumentChunk(
                    content=body_text,
                    metadata=metadata
                )
                document_chunks.append(chunk)

    for document in documents:
        process_document(document)

    return document_chunks