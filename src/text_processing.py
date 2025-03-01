import ollama 
import numpy as np 

def chunk_text(text , chunk_size= 500 , overlap= 50):
  print(f"chunking text of length {len(text)} with chunk size {chunk_size} and overlap {overlap}")
  words= text.split()
  chunks= []
  for i in range(0 , len(words), chunk_size - overlap):
    chunk= ' '.join(words[i:i+chunk_size])
    chunks.append(chunk)
  print(f"created {len(chunks)} chunks")
  return chunks

def embed_text(text): 
  response = ollama.embeddings(model= 'nomic-embed-text', prompt = text)
  return response['embedding']