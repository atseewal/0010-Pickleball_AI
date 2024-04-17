# 0010-Pickleball_AI
AI bot to help parse the rules of Pickleball.

## Project Goals

1. Create a retrieval augmented generation (RAG) bot that can answer questions about pickleball
2. Use the official rules of pickleball as a source to answer the questions

## Implementation

Planned implementation using standard RAG methodology. Documents are loaded to a vector database. A chain is executed to find documents similar to the input question, use that as additional context, and answer the question.

### Project Setup

* Clone the project from the git repository.

* Create a virtual environment using pip.

```bash
pip install requirements.txt
```

* Run `download_documents.ps1` to download the required data.

```bash
. '.\download_documents.ps1'
```

### Vector Database

TBD