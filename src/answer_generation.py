import ollama
import re

def generate_answer(query, context):
    print(f"Generating answer for query: '{query}'")
    prompt = f"""Answer the user's question using the documents given in the context. In the context are documents that should contain an answer. Please always reference the document ID (in square brackets, for example [0],[1]) of the document that was used to make a claim. Use as many citations and documents as it is necessary to answer the question.

Context:
{context}

Question: {query}

Answer:"""

    print("Sending prompt to Ollama")
    response = ollama.generate(model='llama3.1', prompt=prompt)
    print("Received response from Ollama")
    return response['response']