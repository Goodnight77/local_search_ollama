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


## Installation

This project uses `pip` and `virtualenv`.  Ensure you have Python 3.7+ installed.  Create a virtual environment and install the required packages:

```bash
python -m venv myenv
source myenv/Scripts/activate  # On Windows: myenv\Scripts\activate.bat
pip install -r req.txt
```

## Usage

1. **Indexing:**  Index your documents using the `indexing.py` script. You'll need to provide the path to your documents.  Further parameters may be available; consult `indexing.py` for details.  An example might look like:

   ```bash
   python indexing.py --documents_path /path/to/your/documents
   ```

2. **Querying:** Use the main script `main.py` to query the index.  The UI will be launched, allowing you to enter your search terms.

   ```bash
   python main.py
   ```

3. **Answer Generation:** The `answer_generation.py` script handles generating answers from the retrieved documents.

## License

This project is licensed under the Apache License 2.0.  See the LICENSE file for details.
