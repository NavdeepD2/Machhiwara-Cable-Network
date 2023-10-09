import openpyxl
from datetime import datetime
import pandas as pd

def replace_employee_names(name):
    if name and name.startswith("01147"):
        return "RachhpalSingh"
    elif name and name.startswith("01149"):
        return "Gurpreet"
    elif name and name.startswith("01143"):
        return "Babbu"
    else:
        return name

def extract_date(date_str):
    if isinstance(date_str, str):
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            return date_obj.date()
        except ValueError:
            return date_str
    else:
        return date_str.date()

def generate_summary_table(file_path):
    # Load the workbook
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    # Create a dictionary to store the collected amount for each employee on each day
    summary_table = {}

    # Iterate through rows (ignore the first row - header) and update employee names while building the summary table
    for row in sheet.iter_rows(min_row=2, values_only=True):
        date, employee_name, amount = row[9], row[10], row[14]  # Columns 10, 11, and 15
        if not employee_name:  # Skip if employee name is empty (None)
            continue
        employee_name = replace_employee_names(employee_name)
        date = extract_date(date)
        if date not in summary_table:
            summary_table[date] = {employee_name: amount}
        else:
            if employee_name not in summary_table[date]:
                summary_table[date][employee_name] = amount
            else:
                summary_table[date][employee_name] += amount

    # Create a new worksheet to display the summary table
    summary_sheet = workbook.create_sheet(title="Summary")

    # Write the headers
    summary_sheet.append(["Date", "Employee Name", "Amount"])

    # Write the summary table data
    for date, employees in summary_table.items():
        for employee, amount in employees.items():
            summary_sheet.append([date, employee, amount])

    # Save the updated workbook
    workbook.save(file_path)

if __name__ == "__main__":
    excel_file_path = "collection.xlsx"
    generate_summary_table(excel_file_path)
