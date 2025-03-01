import streamlit as st
import os
import json
import faiss
import re 
import requests
from streamlit_lottie import st_lottie
from indexing import index_documents, semantic_search, read_document_chunk, metadata  
from answer_generation import generate_answer

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def main():
    global documents_path, index, metadata
    print("Starting Streamlit UI")
    
    st.set_page_config(page_title="Local GenAI Search", page_icon="🔍", layout="wide")
    
    st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        font-weight: bold;
        color: #1E90FF;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 12px;
        border: none;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('<p class="big-font">Local GenAI Search 🔍</p>', unsafe_allow_html=True)
        st.write("Explore your documents with the power of AI!")
    with col2:
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json"
        lottie_json = load_lottieurl(lottie_url)
        st_lottie(lottie_json, height=150, key="coding")

    # Input for documents path
    documents_path = st.text_input("📁 Enter the path to your documents folder:", "")
    if documents_path:
        documents_path = os.path.abspath(documents_path)
    

    if not os.path.exists("document_index.faiss"):
        st.warning("⚠️ Documents are not indexed. Please run the indexing process first.")
        if st.button("🚀 Index Documents"):
            if documents_path:
                with st.spinner("Indexing documents... This may take a while."):
                    print(f"Indexing documents in {documents_path}")
                    index_documents(documents_path)
                st.success("✅ Indexing complete!")
                st.rerun()
            else:
                st.error("Please enter a valid documents folder path.")
    else:
        if len(metadata) == 0:
            print("Loading FAISS index and metadata")
            try:
                index = faiss.read_index("document_index.faiss")
                with open("metadata.json", "r") as f:
                    metadata = json.load(f)
                print(f"Loaded index with {index.ntotal} vectors and {len(metadata)} metadata entries")
            except Exception as e:
                st.error(f"Failed to load index: {e}")
                st.warning("Please re-index your documents.")
    
    st.markdown("---")
    st.markdown("## Ask a Question")
    question = st.text_input("🤔 What would you like to know about your documents?", "")

    if st.button("🔍 Search and Answer"):
        if question:
            with st.spinner("Searching and generating answer..."):
                print(f"User asked: '{question}'")
                
                # Perform semantic search
                search_results = semantic_search(question)
                
                context = "\n\n".join([f"{i}: {result['content']}" for i, result in enumerate(search_results)])
                
                # Generate answer
                answer = generate_answer(question, context)
                
                st.markdown("### 🤖 AI Answer:")
                st.markdown(answer)
                
                # Display referenced documents
                st.markdown("### 📚 Referenced Documents:")
                referenced_ids = set()
                for match in re.finditer(r'\[(\d+)\]', answer):
                    try:
                        doc_id = int(match.group(1))
                        if doc_id < len(search_results):
                            referenced_ids.add(doc_id)
                    except ValueError:
                        continue

                print(f"Displaying {len(referenced_ids)} referenced documents")
                for doc_id in referenced_ids:
                    doc = search_results[doc_id]
                    with st.expander(f"📄 Document {doc_id} - {os.path.basename(doc['path'])}"):
                        st.write(doc['content'])
                        st.write(f"Source: {doc['path']}")
                        if os.path.exists(doc['path']):
                            with open(doc['path'], 'rb') as f:
                                st.download_button("⬇️ Download file", f, file_name=os.path.basename(doc['path']))
                        else:
                            st.warning(f"⚠️ File not found: {doc['path']}")
        else:
            st.warning("⚠️ Please enter a question before clicking 'Search and Answer'.")

if __name__ == "__main__":
    main()
    print("Application finished")