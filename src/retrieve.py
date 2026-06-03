from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

CHROMA_PATH = "chroma_db_v2"

print("Loading Embedding Model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Loading Vector Database...")

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

collection = vectorstore.get()

print(f"\nDocuments in DB: {len(collection['documents'])}")

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 5}
)

query = "Who has pending the payments and what are the amounts?"  # Example query to test retrieval

print(f"\nSearching for:\n{query}\n")

results = retriever.invoke(query)

for idx, doc in enumerate(results, start=1):

    print("=" * 60)
    print(f"Result {idx}")
    print("=" * 60)

    print("Metadata:")
    print(doc.metadata)

    print("\nContent:")
    print(doc.page_content)

    print("\n")