import pandas as pd
import csv
import re
import tkinter as tk
from tkinter import messagebox

def is_valid_id(id_value):
    """Check if the ID is exactly four digits."""
    return re.match(r"^\d{4}$", id_value) is not None

def is_new_id(id_value, csv_filename):
    """Check if the ID is new or exists in the given CSV file."""
    try:
        with open(csv_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if id_value in row:
                    return False  # ID exists in the CSV file
        return True  # ID is new
    except FileNotFoundError:
        print("CSV file not found.")
        return False  # Assume ID is not new if the file is not found

def is_valid_company_name(name):
    """Check if the company name is valid. Adjust the criteria as needed."""
    # Example validation: Non-empty and up to 100 characters. Adjust as needed.
    return isinstance(name, str) and 0 < len(name) <= 100

def is_valid_transport_value(value):
    """Check if the transport value is a decimal or integer."""
    # Assuming transport values can be integers or decimals with optional 3 decimal places
    return re.match(r"^\d+(\.\d{1,3})?$", value) is not None

def is_valid_energy_value(value):
    """Check if the energy value is a decimal or integer up to 6 digits and 3 decimal places."""
    return re.match(r"^\d{1,6}(\.\d{1,3})?$", value) is not None

def store_emissions_data(data):
    """
    Store emissions data in a CSV file with validations.

    Args:
        data (dict): Dictionary containing company's emissions data.
    """
    try:
        # Validation for the ID
        if not is_valid_id(data.get("ID", "")):
            messagebox.showerror("Error", "ID must be exactly four digits.")
            return False

        # Validation for new ID
        if not is_new_id(data.get("ID", ""), "emissions_data.csv"):
            messagebox.showerror("Error", "ID exists in the database. Please enter a new ID.")
            return False

        # Validate company name
        if not is_valid_company_name(data.get("Name", "")):
            messagebox.showerror("Error", "Invalid company name. Ensure it is not empty and does not exceed 100 characters.")
            return False

        # Validate transportation fields
        transportation_fields = ["Car", "Bus", "Train", "Bicycle", "Walking"]
        for field in transportation_fields:
            if not is_valid_transport_value(str(data.get(field, ""))):
                messagebox.showerror("Error", f"Invalid value for {field}. Must be a decimal or integer.")
                return False

        # Validation for energy fields
        energy_fields = ["Electricity", "Natural Gas", "Fuel Oil", "Propane", "Coal"]
        for field in energy_fields:
            if not is_valid_energy_value(str(data.get(field, ""))):
                messagebox.showerror("Error", f"{field} must be a decimal or integer up to 6 digits and 3 decimal places. No alphabetic characters allowed.")
                return False

        # Calculate emissions for all energy fields
        emissions_data = {"ID": data["ID"], "Name": data["Name"]}
        for field in energy_fields:
            emissions_data[field] = float(data.get(field, 0)) * 12 * get_conversion_factor(field)

        # Calculate emissions for transportation fields
        for field in transportation_fields:
            emissions_data[field] = float(data.get(field, 0)) * 12 * get_conversion_factor(field)

        # Write the calculated emissions to the CSV file
        with open("emissions_data.csv", mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=emissions_data.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(emissions_data)

        from pdf_report import generate_and_save_graph_to_pdf

        # Generate the PDF report when the tab is accessed
        generate_and_save_graph_to_pdf('reports/emissions_report.pdf')
        
        messagebox.showinfo("Success", "Emissions data with a pdf report added successfully!")
        return True

    except Exception as e:
        messagebox.showerror("Error", f"Failed to store emissions data: {e}")
        return False

def get_conversion_factor(field):
    """Get the conversion factor for calculating emissions based on the field."""
    # Define conversion factors for each field
    conversion_factors = {
        "Electricity": 0.0005,
        "Natural Gas": 0.0053,
        "Fuel Oil": 2.32,
        "Propane": 2.75,  # Propane factor: 2.75 kgCO2/liter
        "Coal": 2.5,      # Coal factor: 2.5 kgCO2/kg
        "Car": 2.4,       # Car factor: 2.4 kgCO2/liter (estimated)
        "Bus": 5.5,       # Bus factor: 5.5 kgCO2/liter (estimated)
        "Train": 3.0      # Train factor: 3.0 kgCO2/liter (estimated)
        # Add more conversion factors as needed
    }
    return conversion_factors.get(field, 1.0)  # Default to 1.0 if no conversion factor is defined

def retrieve_emissions_data_by_id(company_id, retrieved_data_text, reports_text):
    """Retrieve emissions data for a specific company ID and display it."""
    try:
        # Convert company_id to integer
        company_id = int(company_id)

        with open('emissions_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            found = False
            for row in reader:
                if int(row['ID']) == company_id:
                    found = True
                    # emissions data
                    retrieved_data_text.delete(1.0, tk.END)
                    retrieved_data_text.insert(tk.END, f"Company ID: {company_id}\n")
                    for key, value in row.items():
                        retrieved_data_text.insert(tk.END, f"{key}: {value}\n")
                    # Reports
                    total_transportation_emissions = sum(float(row[method]) for method in ['Car', 'Bus', 'Train', 'Bicycle', 'Walking'])
                    total_energy_emissions = sum(float(row[source]) for source in ['Electricity', 'Natural Gas', 'Fuel Oil', 'Propane', 'Coal'])
                    total_emissions = total_transportation_emissions + total_energy_emissions
                    reports_text.delete(1.0, tk.END)
                    reports_text.insert(tk.END, "Summary Reports\n")
                    reports_text.insert(tk.END, f"Total Transportation Emissions: {total_transportation_emissions} kg CO2\n")
                    reports_text.insert(tk.END, f"Total Energy Source Emissions: {total_energy_emissions} kg CO2\n")
                    reports_text.insert(tk.END, f"Total Emissions: {total_emissions} kg CO2\n")

                    # Suggestions
                    suggestions = ""
                    if total_emissions < 75:
                        suggestions = "- Your company's emissions are relatively low. Keep going!"
                    elif total_emissions > 75:
                        suggestions = "- Consider implementing measures to reduce your carbon footprint,(using public transportation, carpooling, or investing in energy-efficient appliances."
                    else:
                        suggestions = "- Your company's emissions are moderate. you must evaluate your measurs regularly"
                    reports_text.insert(tk.END, "Suggestions for Reducing Emissions:\n")
                    reports_text.insert(tk.END, suggestions)

                    break

            if not found:
                messagebox.showerror("Error", "Company ID not found.")
    except ValueError:
        messagebox.showerror("Error", "Invalid company ID. Please enter a valid integer.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No data available.")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {e}")

def retrieve_all_companies_data():
    """
    Retrieve all companies' emissions data from the CSV file.

    This function reads the 'emissions_data.csv' file, sorts the data alphabetically by company name,
    and then returns a formatted string of company IDs and names.

    Returns:
        str: Formatted string of company IDs and names.
    """
    try:
        df = pd.read_csv('emissions_data.csv')
        if df.empty:
            return "No data available."

        # Sort the DataFrame by company names
        df_sorted = df.sort_values(by='Name')

        companies_data = df_sorted[['ID', 'Name']].to_string(index=False)
        return "List of Companies (Ordered Alphabetically by Name):\n" + companies_data

    except FileNotFoundError:
        return "No data available."
    except Exception as e:
        return f"Error occurred: {e}"

def delete_emissions_data_by_id(company_id):
    """Delete emissions data for a specific company ID from the CSV file."""
    try:
        # Convert company_id to integer
        company_id = int(company_id)

        # Open the CSV file and search for the company ID
        with open('emissions_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            rows = list(reader)
            found = False

            # Create a new list to store rows that should be kept
            updated_rows = []

            for row in rows:
                if int(row['ID']) == company_id:
                    found = True
                    messagebox.showinfo("Success", f"Emissions data for company ID {company_id} has been deleted successfully.")
                else:
                    updated_rows.append(row)

            # Write the updated rows to the CSV file
            with open('emissions_data.csv', mode='w', newline='') as outfile:
                fieldnames = reader.fieldnames
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(updated_rows)

            if not found:
                messagebox.showerror("Error", "Company ID not found.")
    except ValueError:
        messagebox.showerror("Error", "Invalid company ID. Please enter a valid integer.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No data available.")
    except Exception as e:
        messagebox.showerror("Error", f"Error occurred: {e}")