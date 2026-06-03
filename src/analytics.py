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

def get_patient_holidays(query):
    df = pd.read_excel(DATA_PATH)
    
    # 1. Grab a list of all patient names
    patients = df["Patient_Name"].dropna().unique()
    
    # 2. Search the user's question for the patient's name
    target_patient = None
    for patient in patients:
        if str(patient).lower() in query.lower():
            target_patient = patient
            break
            
    if not target_patient:
        return "I couldn't identify the patient's name in your question. Please include their exact name!"
        
    # 3. Filter for that specific patient
    patient_df = df[df["Patient_Name"] == target_patient]
    
    # 4. Filter for holidays/cancellations in the Remarks column
    # We check for both spelling variations just to be safe!
    holiday_mask = patient_df["Remarks"].isin(["Cancelled By Therapist", "Cancelled by Patient", "cancelled by therapist", "Cancelled By Patient","Cancelled by Therapist"])
    holidays_df = patient_df[holiday_mask]
    
    total_holidays = len(holidays_df)
    
    if total_holidays == 0:
        return f"Great news! No holidays or cancellations have been recorded for {target_patient}."
        
    # 5. Extract the dates and the specific reason
    holiday_lines = []
    for _, row in holidays_df.iterrows():
        date_str = str(row["Date"]).split()[0]
        reason = row["Remarks"]
        holiday_lines.append(f"- {date_str}: {reason}")
        
    holidays_list_str = "\n".join(holiday_lines)
    
    return f"{target_patient} has had a total of {total_holidays} holidays/cancellations:\n{holidays_list_str}"


    



def get_sundays_passed_since_start(query):

    df = pd.read_excel(DATA_PATH)

    

    # 1. Grab a list of all patient names

    patients = df["Patient_Name"].dropna().unique()

    

    # 2. Search the user's question for the patient's name

    target_patient = None

    for patient in patients:

        if str(patient).lower() in query.lower():

            target_patient = patient

            break

            

    if not target_patient:

        return "I couldn't identify the patient's name in your question. Please include their exact name!"

        

    # 3. Filter for that specific patient

    patient_df = df[df["Patient_Name"] == target_patient]

    

    if patient_df.empty:

        return f"No records found for {target_patient}."

        

    # 4. Get their exact Exercise Start Date (assuming it's in the 'Exercise Start Date' column)

    # We take the first available start date for them

    start_date_val = patient_df["Exercise Start Date"].dropna().iloc[0]

    start_date = pd.to_datetime(start_date_val)

    today = pd.Timestamp.today()

    

    # 5. Generate a calendar range and count the Sundays (Sunday is day 6 in Pandas: Monday=0, Sunday=6)

    days_between = pd.date_range(start=start_date, end=today)

    sundays_passed = (days_between.dayofweek == 6).sum()

    

    clean_date = start_date.strftime('%Y-%m-%d')

    return f"A total of {sundays_passed} Sunday(s) have passed since {target_patient} started their exercise on {clean_date}."





def get_sunday_visits():

    df = pd.read_excel(DATA_PATH)

    

    # 1. Filter rows where the Remarks column contains "Sunday visit conducted"

    # We use na=False to prevent errors on empty remark cells, and case=False to catch spelling variations

    sunday_visits_df = df[df["Remarks"].astype(str).str.contains("Sunday visit conducted", case=False, na=False)]

    

    if sunday_visits_df.empty:

        return "No Sunday visits have been recorded for any patient yet."

        

    # 2. Count the unique patients

    unique_patients_count = sunday_visits_df["Patient_Name"].nunique()

    

    # 3. Build the detailed output

    result = f"A total of {unique_patients_count} patient(s) had visits conducted on a Sunday.\nHere are the details:\n"

    

    # Group by patient to list their specific Sunday dates

    grouped = sunday_visits_df.groupby("Patient_Name")

    for patient_name, group in grouped:

        # Extract just the YYYY-MM-DD from the dates

        dates = [str(d).split()[0] for d in group["Date"].tolist()]

        result += f"- {patient_name}: {len(dates)} Sunday visit(s) on {', '.join(dates)}\n"

        

    return result.strip()


def get_village_with_most_patients():
    df = pd.read_excel(DATA_PATH)
    
    # Group by village and count UNIQUE patients
    village_counts = df.groupby("Village")["Patient_ID"].nunique()
    
    if village_counts.empty:
        return "No patient data available."
        
    # Find the absolute highest number of patients
    max_patients = village_counts.max()
    
    # Find all villages that share this exact maximum number (handles ties perfectly!)
    top_villages = village_counts[village_counts == max_patients].index.tolist()
    
    # Format the output cleanly depending on if there is a tie
    if len(top_villages) == 1:
        return f"The village with the most patients is {top_villages[0]}, which has {max_patients} patient(s)."
    else:
        villages_str = " and ".join(top_villages)
        return f"There is a tie! The villages with the most patients are {villages_str}, each having {max_patients} patient(s)."

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