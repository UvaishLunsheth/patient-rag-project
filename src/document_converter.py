import pandas as pd
from langchain_core.documents import Document

def create_patient_documents(df):
    documents = []
    
    # Group the dataframe by Patient_ID to process one patient at a time
    grouped_patients = df.groupby("Patient_ID")
    
    for patient_id, patient_data in grouped_patients:
        # Sort by Date to ensure the last row has the most recent status updates
        patient_data = patient_data.sort_values("Date")
        latest_record = patient_data.iloc[-1]
        
        # Calculate aggregations across all visits for this specific patient
        total_visits = patient_data["Visit_Status"].eq("Visit").sum()
        total_amount_received = patient_data["Amount Received (₹)"].sum()
        total_revenue = patient_data["True_Revenue"].sum()
        outstanding_amount = total_revenue - total_amount_received
        
        # --- Extract Payment History Log ---
        # Filter only the rows where an actual payment was made
        payments_df = patient_data[patient_data["Amount Received (₹)"] > 0]
        
        if not payments_df.empty:
            payment_lines = []
            for _, row in payments_df.iterrows():
                # Extract just the YYYY-MM-DD part of the date
                date_str = str(row['Date']).split()[0]
                amount = row['Amount Received (₹)']
                payment_lines.append(f"- {date_str}: ₹{amount:,.0f}")
            payment_history_str = "\n".join(payment_lines)
        else:
            payment_history_str = "- No payments recorded yet."
        
        # Format the text block to be highly retrieval-friendly
        text = f"""Patient ID: {latest_record['Patient_ID']}
Patient Name: {latest_record['Patient_Name']}

Village: {latest_record['Village']}

Condition: {latest_record['Patient Condition']}
Condition Category: {latest_record['Patient Condition Category']}

Exercise Start Date: {latest_record['Exercise Start Date']}

Total Visits Conducted: {total_visits}

Financial Summary:
- Total Revenue Generated: ₹{total_revenue:,.0f}
- Total Amount Received: ₹{total_amount_received:,.0f}
- Outstanding Amount: ₹{outstanding_amount:,.0f}
- Payment Status: {latest_record['Payment_Status']}

Latest Visit Status: {latest_record['Visit_Status']}

Payment History Log:
{payment_history_str}"""

        # Create the LangChain Document and attach filterable metadata
        doc = Document(
            page_content=text.strip(),
            metadata={
                "patient_id": latest_record["Patient_ID"],
                "patient_name": latest_record["Patient_Name"],
                "condition_category": latest_record["Patient Condition Category"],
                "village": latest_record["Village"]
            }
        )
        documents.append(doc)
        
    return documents

# Test block to verify it works before plugging it into the database script
if __name__ == "__main__":
    print("Loading Excel data...")
    df = pd.read_excel("data/Visit_Charges_data.xlsx")
    
    docs = create_patient_documents(df)
    
    print(f"\nTotal Documents Generated: {len(docs)}")
    print("\n" + "="*50)
    print("First Patient Document Preview:")
    print("="*50 + "\n")
    print(docs[0].page_content)
    print("\n" + "="*50)