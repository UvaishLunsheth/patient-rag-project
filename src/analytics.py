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

def get_village_wise_revenue():
    df = pd.read_excel(DATA_PATH)
    # Group by Village and sum the revenue
    village_rev = df.groupby("Village")["True_Revenue"].sum().reset_index()
    
    # Sort from highest revenue to lowest
    village_rev = village_rev.sort_values("True_Revenue", ascending=False)
    
    result = "Here is the revenue breakdown by village:\n"
    for _, row in village_rev.iterrows():
        result += f"- {row['Village']}: ₹{row['True_Revenue']:,.0f}\n"
    return result.strip()

def get_average_revenue_per_patient():
    df = pd.read_excel(DATA_PATH)
    total_rev = df["True_Revenue"].sum()
    total_patients = df["Patient_ID"].nunique()
    
    avg_rev = total_rev / total_patients if total_patients > 0 else 0
    return f"The average revenue generated per patient is ₹{avg_rev:,.0f}."

def get_patient_daily_charges():
    df = pd.read_excel(DATA_PATH)
    
    # Group by patient and calculate their per-visit charge
    result = "Here is the effective per-day charge for each patient:\n"
    
    grouped = df.groupby("Patient_Name")
    for name, group in grouped:
        total_revenue = group["True_Revenue"].sum()
        total_visits = group[group["Visit_Status"] == "Visit"].shape[0]
        
        # Avoid division by zero if a patient hasn't had any visits yet
        if total_visits > 0:
            daily_charge = total_revenue / total_visits
            result += f"- {name}: ₹{daily_charge:,.0f} per day\n"
        else:
            result += f"- {name}: No visits recorded yet\n"
            
    return result.strip()

def get_highest_daily_charge_patient():
    df = pd.read_excel(DATA_PATH)
    
    patient_charges = {}
    grouped = df.groupby("Patient_Name")
    
    # Calculate everyone's daily charge
    for name, group in grouped:
        total_revenue = group["True_Revenue"].sum()
        total_visits = group[group["Visit_Status"] == "Visit"].shape[0]
        
        if total_visits > 0:
            patient_charges[name] = total_revenue / total_visits
            
    if not patient_charges:
        return "No visits have been recorded yet."
        
    # Find the maximum charge
    max_charge = max(patient_charges.values())
    
    # Find all patients who pay this max amount (handles ties)
    top_patients = [name for name, charge in patient_charges.items() if charge == max_charge]
    
    patients_str = " and ".join(top_patients)
    return f"The highest per-day charge is ₹{max_charge:,.0f}, paid by: {patients_str}."

def get_least_daily_charge_patient():
    df = pd.read_excel(DATA_PATH)
    
    patient_charges = {}
    grouped = df.groupby("Patient_Name")
    
    # Calculate everyone's daily charge
    for name, group in grouped:
        total_revenue = group["True_Revenue"].sum()
        total_visits = group[group["Visit_Status"] == "Visit"].shape[0]
        
        if total_visits > 0:
            patient_charges[name] = total_revenue / total_visits
            
    if not patient_charges:
        return "No visits have been recorded yet."
        
    # Find the MINIMUM charge instead of maximum
    min_charge = min(patient_charges.values())
    
    # Find all patients who pay this minimum amount (handles ties)
    bottom_patients = [name for name, charge in patient_charges.items() if charge == min_charge]
    
    patients_str = " and ".join(bottom_patients)
    return f"The lowest per-day charge is ₹{min_charge:,.0f}, paid by: {patients_str}."

# Quick test block
if __name__ == "__main__":
    print(get_total_revenue())
    print(get_total_outstanding())
    print(get_highest_outstanding_patient())
    print(get_total_patients())
    print(get_latest_payment())
    print(get_village_wise_revenue())
    print(get_average_revenue_per_patient())
    print(get_patient_daily_charges())
    print(get_highest_daily_charge_patient())
    print(get_least_daily_charge_patient())