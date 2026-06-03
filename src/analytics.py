import pandas as pd

# Load the dataset once
DATA_PATH = "data/Visit_Charges_data.xlsx"


def get_total_revenue():
    df = pd.read_excel(DATA_PATH)
    total = df["True_Revenue"].sum()
    return f"The total revenue generated across all patients is ₹{total:,.0f}."

def get_total_patients():
    df = pd.read_excel(DATA_PATH)
    total_patients = df["Patient_ID"].nunique()
    return f"There are {total_patients} unique patients in the dataset."

def get_total_outstanding():
    df = pd.read_excel(DATA_PATH)
    total_rev = df["True_Revenue"].sum()
    total_received = df["Amount Received (₹)"].sum()
    outstanding = total_rev - total_received
    return f"The total outstanding amount across all patients is ₹{outstanding:,.0f}."

def get_highest_outstanding_patient():
    df = pd.read_excel(DATA_PATH)
    # Group by patient to get their total revenue and received amounts
    patient_totals = df.groupby("Patient_Name").agg({
        "True_Revenue": "sum",
        "Amount Received (₹)": "sum"
    })
    patient_totals["Outstanding"] = patient_totals["True_Revenue"] - patient_totals["Amount Received (₹)"]
    
    # Find the patient with the max outstanding
    top_patient = patient_totals.sort_values("Outstanding", ascending=False).iloc[0]
    patient_name = top_patient.name
    amount = top_patient["Outstanding"]
    
    return f"The patient with the highest outstanding amount is {patient_name} with ₹{amount:,.0f}."
def get_latest_payment():
    df = pd.read_excel(DATA_PATH)
    
    # 1. Filter for rows where an actual payment was made
    payments_df = df[df["Amount Received (₹)"] > 0]
    
    if payments_df.empty:
        return "No payments have been recorded yet."
        
    # 2. Sort the dates in descending order (newest first)
    latest_payment = payments_df.sort_values("Date", ascending=False).iloc[0]
    
    # 3. Extract the details
    patient_name = latest_payment["Patient_Name"]
    amount = latest_payment["Amount Received (₹)"]
    date_str = str(latest_payment["Date"]).split()[0]
    
    return f"The most recent payment was made by {patient_name} on {date_str} for the amount of ₹{amount:,.0f}."

import pandas as pd
from datetime import datetime

def get_days_since_patient_payment(query):
    df = pd.read_excel(DATA_PATH)
    
    # 1. Grab a list of all patient names in your dataset
    patients = df["Patient_Name"].dropna().unique()
    
    # 2. Search the user's question to see which patient they are asking about
    target_patient = None
    for patient in patients:
        if str(patient).lower() in query.lower():
            target_patient = patient
            break
            
    if not target_patient:
        return "I couldn't identify the patient's name in your question. Please include their exact name!"
        
    # 3. Filter the data to find that specific patient's payments
    patient_df = df[df["Patient_Name"] == target_patient]
    payments_df = patient_df[patient_df["Amount Received (₹)"] > 0]
    
    if payments_df.empty:
        return f"No payments have been recorded for {target_patient} yet."
        
    # 4. Do the exact calendar math
    latest_date = pd.to_datetime(payments_df["Date"].max())
    today = pd.Timestamp.today()
    
    days_passed = (today - latest_date).days
    clean_date = latest_date.strftime('%Y-%m-%d')
    
    return f"It has been {days_passed} days since {target_patient}'s last payment, which was made on {clean_date}."

# Quick test block
if __name__ == "__main__":
    print(get_total_revenue())
    print(get_total_outstanding())
    print(get_highest_outstanding_patient())
    print(get_total_patients())
    print(get_latest_payment())