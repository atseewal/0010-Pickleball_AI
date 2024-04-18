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

#### Download and install Microsoft C++ Build Tools

If you have an issue installing the requirements, specifically failing to build wheels for chorma-hnswlib, download and install Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Try installing way more than you think you need. If clicking the **Launch** button in the Visual Studio Installer displays **File not found** or similar in the command prompt window, you probably didn't install all of the components. I had success with MSVC v143 - VS 2022 C++ x64/x86 build tools (latest), Windows 11 SDK (10.0.22621.0), C++ CMake tools for Windows, Testing tools core features - Build Tools, C++ AddressSanitizer, C++ Build Tools core features, C++ 2022 Redistributable Update, and C++ core desktop features installed.

*This step never works right for me, I end up installing and uninstalling things for hours.*

### Vector Database

TBD