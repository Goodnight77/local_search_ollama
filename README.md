# Local GenAI Search with Ollama

## Project Overview

This project implements a local GenAI search engine leveraging Ollama for model execution.  It indexes documents, allowing for efficient semantic search using a vector database (Faiss).  The system includes a user interface (UI) for interacting with the search functionality.

## Features

* **Local Indexing:** Indexes documents locally for privacy and control.
* **Semantic Search:** Performs semantic searches based on the meaning of queries, not just keywords.
* **Ollama Integration:** Uses Ollama for managing and running the language model.
* **Faiss Vector Database:** Employs Faiss for efficient similarity search of embeddings.
* **User Interface:** Provides a user-friendly interface for querying and viewing results.
* **Text Preprocessing:** Includes functionality for cleaning and preparing text for indexing.

## Getting started 

### Prerequisites

- Python 3.8 or higher
- Streamlit
- Ollama (for AI model integration)
- FAISS (for vector indexing)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Goodnight77/local_search_ollama.git
   cd local-genai-search
2. **Install the required dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Set up Ollama**:
   Ensure that Ollama is installed and running on your machine. You can download it from [here](https://ollama.com/).




## Usage
1. **Run the streamlit app**:
   ```bash
   streamlit run main.py

2. **Index your documents**:
   Enter the path to your documents folder in the input field.
   Click on the "🚀 Index Documents" button to start the indexing process.

3. **Ask Question**:
   Once the documents are indexed, you can enter your question in the input field and click on the "🔍 Search and Answer"  button.
   The app will perform a semantic search, generate an AI-based answer, and display the referenced documents.

## File Structure

- `main.py`: The entry point of the application.
- `ui.py`: Contains the Streamlit UI and main logic.
- `indexing.py`: Handles document indexing and semantic search.
- `handlers.py`: Contains functions to read different types of documents (PDF, DOCX, PPTX, TXT).
- `text_processing.py`: Handles text chunking and embedding.
- `answer_generation.py`: Generates AI-based answers using Ollama.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.

## License

This project is licensed under the Apache License 2.0.  See the LICENSE file for details.

