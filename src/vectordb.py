from loader import load_data
from document_converter import create_patient_documents

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
import shutil

# -----------------------------
# Configuration
# -----------------------------
DATA_PATH = "data/Visit_Charges_data.xlsx"

# New Vector Database Folder
CHROMA_PATH = "chroma_db_v2"


# -----------------------------
# Load Dataset
# -----------------------------
print("Loading Dataset...")

df = load_data(DATA_PATH)


# -----------------------------
# Create Patient Documents
# -----------------------------
print("\nCreating Patient Documents...")

documents = create_patient_documents(df)

print(f"\nDocuments Created: {len(documents)}")


# -----------------------------
# Preview First Document
# -----------------------------
print("\nPreview of First Patient Document:")
print("=" * 60)

print(documents[0].page_content)

print("=" * 60)


# -----------------------------
# Load Embedding Model
# -----------------------------
print("\nLoading Embedding Model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# -----------------------------
# Create ChromaDB
# -----------------------------
print("\nCreating ChromaDB V2...")

if os.path.exists(CHROMA_PATH):
    print("Deleting existing ChromaDB...")
    shutil.rmtree(CHROMA_PATH)

print("\nCreating ChromaDB V2...")

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embedding_model,
    persist_directory=CHROMA_PATH
)

print("\nVector Database V2 Created Successfully!")
print(f"Stored in: {CHROMA_PATH}")

collection = vectorstore.get()

print(len(collection["documents"]))
print(collection["documents"][0])
