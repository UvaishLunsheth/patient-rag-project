

```markdown
# Physiotherapy Hybrid AI Assistant (RAG + Analytics)

An intelligent conversational agent built for a physiotherapy clinic. This project implements a **Hybrid AI Architecture** that combines a Large Language Model (LLM) with a custom Keyword Router, delegating complex financial math to **Pandas** and semantic patient inquiries to a **ChromaDB RAG** (Retrieval-Augmented Generation) pipeline.

## 🚀 Project Overview

Standard RAG pipelines struggle with aggregate math (e.g., calculating total clinic revenue) because they are limited by retrieval windows and LLM hallucination. This project solves that by acting as a "Traffic Cop":
1. **Analytics Route (Pandas):** Global queries (total revenue, outstanding balances, average daily charges) are intercepted and calculated with 100% accuracy using Pandas.
2. **Semantic Route (ChromaDB RAG):** Patient-specific queries (conditions, payment history, visit counts) fall through to the vector database, where the LLM reads optimized text summaries to answer contextually.

## ✨ Key Features
* **Custom Hybrid Router:** intelligently routes user questions to either the Pandas math engine or the vector database.
* **RAG-Optimized Document Engineering:** Converts raw Excel rows into highly structured, patient-level text summaries (including calculated daily charges and chronological payment histories) to maximize retrieval accuracy.
* **Anti-Hallucination Guardrails:** Strict prompt engineering ensures the AI refuses to answer if information is not present in the dataset.
* **Exact Financial Aggregations:** Handles edge cases like highest/lowest payers and exact day-counts since a patient's last payment using Python's `datetime` and Pandas.

## 🛠️ Tech Stack
* **Language:** Python
* **Data Processing & Analytics:** Pandas, OpenPyXL
* **AI & Orchestration:** LangChain, OpenAI (`gpt-4o-mini`)
* **Embeddings:** HuggingFace (`sentence-transformers/all-MiniLM-L6-v2`)
* **Vector Database:** ChromaDB

## 📁 Project Structure
```text
patient-rag-project/
├── dashboard/               # UI and dashboard components
├── data/                    # Raw and processed patient datasets
├── src/                     # Core application source code
│   ├── analytics.py         # Analytics and metric tracking
│   ├── chatbot.py           # Chatbot logic and LLM integration
│   ├── document_converter.py# File format conversions (e.g., PDF/Word to text)
│   ├── loader.py            # Data ingestion scripts
│   ├── retrieve.py          # Semantic search and RAG retrieval logic
│   └── vectordb.py          # Vector database (ChromaDB) management
├── .env                     # Environment variables (Ignored by Git)
├── .gitignore               # Ignored files and directories
├── requirements.txt         # Python package dependencies
└── README.md                # Project documentation
```

## ⚙️ Setup and Installation

**1. Clone the repository:**

```bash
git clone [https://github.com/yourusername/physio-hybrid-assistant.git](https://github.com/yourusername/physio-hybrid-assistant.git)
cd physio-hybrid-assistant

```

**2. Install dependencies:**

```bash
pip install -r requirements.txt

```

**3. Set up your environment variables:**
Create a `.env` file in the root directory and add your OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here


```

**4. Build the Vector Database:**
Run the ingestion script to process the Excel data and build the Chroma collection:

```bash
python src/vectordb.py

```

## 💻 Usage

Start the interactive hybrid assistant by running:

```bash
python src/chatbot.py

```

### Example Prompts to Try:

**Testing the Pandas Analytics Route:**

* *"What is the total outstanding amount across all patients?"*
* *"Which patient has the highest per day charge?"*
* *"How many neurological patients are there?"*
* *"How many days since the last payment made by the Monikaben?"*


**Testing the ChromaDB RAG Route:**

* *"What condition does ChanduBhai have?"*
* *"Who has pending payments?"*
* *"When was the last payment made by Monikaben?"*
* *"which patient has most visits?"*
* *"what is Total Amount received by the Monikaben?"*
* *"How many patients are there"*

```

***



```