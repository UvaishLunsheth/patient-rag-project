from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import ChatOpenAI
from datetime import date

today = date.today().strftime("%Y-%m-%d")

# -----------------------------
# Import Analytics Functions
# -----------------------------
# Make sure your analytics.py file is in the same folder!
from analytics import (
    get_total_patients,
    get_total_revenue, 
    get_total_outstanding, 
    get_highest_outstanding_patient,
    get_latest_payment,
    get_days_since_patient_payment,
    get_village_wise_revenue,        
    get_average_revenue_per_patient,
    get_patient_daily_charges,
    get_highest_daily_charge_patient,
    get_least_daily_charge_patient
)

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Configuration
# -----------------------------
CHROMA_PATH = "chroma_db_v2"

# -----------------------------
# Load Embedding Model
# -----------------------------
print("Loading Embedding Model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"local_files_only": True}
)

# -----------------------------
# Load Vector Database
# -----------------------------
print("Loading Patient Database...")

vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 10}
)

# -----------------------------
# Load OpenAI (GPT-4o-mini)
# -----------------------------
print("Loading OpenAI...")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

print("\n" + "=" * 60)
print(" Hybrid Physiotherapy Patient Assistant Ready ")
print("=" * 60)
print("Type 'exit' to quit.\n")

# -----------------------------
# Chat Loop & Router
# -----------------------------
while True:

    query = input("Ask a question: ").strip()

    print("You typed:", query)

    if query.lower() == "exit":
        print("Goodbye!")
        break
        
    query_lower = query.lower()

    # ==========================================
    # THE ROUTER
    # ==========================================
    
    # Route 1: Analytics (Math/Aggregations)
    if "total revenue" in query_lower or "overall revenue" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_total_revenue())

    elif "how many patients" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_total_patients())    

    elif "total outstanding" in query_lower or "total amount yet to be paid" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_total_outstanding())

    elif "highest outstanding" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_highest_outstanding_patient())

   # Only route GLOBAL last payment questions to Pandas
    elif "who made the last payment" in query_lower or "last payment overall" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_latest_payment())

    # Route for calculating days since a patient's payment
    elif "how many days" in query_lower and "payment" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        # We pass the query into the function so it can find the name!
        print("Answer:\n" + get_days_since_patient_payment(query))    
    # --------------------------
    
    # Route for Village-wise Revenue
    elif any(phrase in query_lower for phrase in ["village wise", "revenue by village", "village revenue"]):
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_village_wise_revenue())

    # Route for Average Revenue Per Patient
    elif "average revenue" in query_lower or "revenue per patient" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_average_revenue_per_patient())

    #  Route for HIGHEST Per Day Charge (Must go first!)
    elif any(phrase in query_lower for phrase in ["highest per day charge", "most per day charge", "highest daily charge"]):
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_highest_daily_charge_patient())

    #  Route for LOWEST Per Day Charge
    elif any(phrase in query_lower for phrase in ["least per day charge", "lowest per day charge", "least daily charge"]):
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_least_daily_charge_patient())

    #  Route for General Per Day Charges (List everyone)
    elif "per day charge" in query_lower or "daily charge" in query_lower or "charge of all patients" in query_lower:
        print("\n[System: Routed to Pandas Analytics]")
        print("Answer:\n" + get_patient_daily_charges())

    # Route 2: RAG (Semantic Search / Text)
    else:
        print("\n[System: Routed to ChromaDB RAG]")


        
        # -----------------------------
        # Retrieve Relevant Patients
        # -----------------------------
        docs = retriever.invoke(query)

        if not docs:
            print("\nNo matching records found.\n")
            continue

        # -----------------------------
        # Build Context
        # -----------------------------
        context = "\n\n".join(
            [doc.page_content for doc in docs]
        )

        # -----------------------------
        # Prompt
        # -----------------------------
        prompt = f"""
Today's current date is: {today}        
You are a physiotherapy clinic assistant.

Your job is to answer questions ONLY from the patient records provided.

Rules:

1. Use ONLY the information from the context.
2. Never make up information.
3. Never guess.
4. If information is unavailable, say:
   "I could not find that information in the dataset."
5. For financial questions:
   Use the values exactly as shown.
6. For patient conditions:
   Report the condition and condition category.
7. If multiple patients match the question,
   list all matching patients.

PATIENT RECORDS:

{context}

QUESTION:
{query}

ANSWER:
"""

        # -----------------------------
        # Generate Response
        # -----------------------------
        try:
            response = llm.invoke(prompt)
            print("\nAnswer:")
            print(response.content)
        except Exception as e:
            print(f"\n[Error]: OpenAI API failed. Details: {e}")

    print("\n" + "=" * 60 + "\n")