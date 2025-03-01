import os
import faiss
import numpy as np
import json
from handlers import read_pdf, read_docx, read_pptx, read_txt
from text_processing import chunk_text, embed_text

dimension = 768  # Dimension for 'nomic-embed-text' model
index = faiss.IndexFlatIP(dimension)
metadata = []

def index_documents(directory):
    print(f"Indexing documents in directory: {directory}")
    global metadata
    documents = []
    metadata = []  # Reset metadata
    
    # Convert to absolute path
    abs_directory = os.path.abspath(directory)
    
    for root, _, files in os.walk(abs_directory):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"Processing file: {file_path}")
            content = ""
            
            if file.lower().endswith('.pdf'):
                content = read_pdf(file_path)
            elif file.lower().endswith('.docx'):
                content = read_docx(file_path)
            elif file.lower().endswith('.pptx'):
                content = read_pptx(file_path)
            elif file.lower().endswith('.txt'):
                content = read_txt(file_path)
            
            if content:
                chunks = chunk_text(content)
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    # Store both absolute and relative paths
                    rel_path = os.path.relpath(file_path, abs_directory)
                    metadata.append({
                        "abs_path": file_path,
                        "rel_path": rel_path,
                        "chunk_id": i,
                        "base_dir": abs_directory
                    })
    
    print(f"Encoding {len(documents)} document chunks")
    embeddings = [embed_text(doc) for doc in documents]
    print(f"Adding embeddings to FAISS index")
    index.add(np.array(embeddings))
    
    # Save index and metadata
    print("Saving FAISS index and metadata")
    faiss.write_index(index, "document_index.faiss")
    with open("metadata.json", "w") as f:
        json.dump(metadata, f)
    
    print(f"Indexed {len(documents)} document chunks.")

def semantic_search(query, k=10):
    print(f"Performing semantic search for query: '{query}', k={k}")
    query_vector = embed_text(query)
    distances, indices = index.search(np.array([query_vector]), k)
    
    results = []
    for i, idx in enumerate(indices[0]):
        meta = metadata[idx]
        content = read_document_chunk(meta["abs_path"], meta["chunk_id"])
        results.append({
            "id": int(idx),
            "path": meta["abs_path"],
            "content": content,
            "score": float(distances[0][i])
        })
    
    print(f"Found {len(results)} search results")
    return results

def read_document_chunk(file_path, chunk_id):
    print(f"Reading document chunk: {file_path}, chunk_id: {chunk_id}")
    content = ""
    
    # Find the metadata entry for this file
    matching_meta = None
    for meta in metadata:
        if meta["abs_path"] == file_path or meta["rel_path"] == os.path.basename(file_path):
            matching_meta = meta
            break
    
    if matching_meta:
        # Try both absolute path and reconstructed path
        try_paths = [
            matching_meta["abs_path"],
            os.path.join(matching_meta["base_dir"], matching_meta["rel_path"])
        ]
        
        for try_path in try_paths:
            if os.path.exists(try_path):
                file_path = try_path
                break
        else:
            print(f"File not found: {file_path}")
            return f"[Content not available for {os.path.basename(file_path)}]"
    
    if file_path.endswith('.pdf'):
        content = read_pdf(file_path)
    elif file_path.endswith('.docx'):
        content = read_docx(file_path)
    elif file_path.endswith('.pptx'):
        content = read_pptx(file_path)
    elif file_path.endswith('.txt'):
        content = read_txt(file_path)
    
    chunks = chunk_text(content)
    return chunks[chunk_id] if chunk_id < len(chunks) else ""