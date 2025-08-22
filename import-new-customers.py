import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime
import shutil
import paramiko
import os

# Define the scope and credentials
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name("your-credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet and get the worksheet
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1MEojoL2sBa4_aP634LUtAB6lNIbHsROUpT2AxiLvfQU")
worksheet = sheet.worksheet("Form Responses 2")

# Get all data from the sheet
data = worksheet.get_all_records()

# Convert to DataFrame
df = pd.DataFrame(data)

# Ensure that 'No.' column is treated as integers
df['No.'] = pd.to_numeric(df['No.'], errors='coerce')

# Prompt the user for the starting serial number
start_serial = int(input("Enter the serial number from which to begin (e.g., 10): "))

# Filter the DataFrame based on the serial number
filtered_df = df[df['No.'] >= start_serial]

# Prepare the new DataFrame with the required columns
new_columns = ['STB', 'VC', 'SAF', 'UA', 'challanno', 'STBRENT', 'STB_Security', 'STBDiscount', 'CRNNO', 'MSOID',
               'StbEntryDate', 'STBACDC', 'PACK', 'BoxCompanyName', 'AccountNo', 'Customerid', 'MrMrs', 'InternetID',
               'SubID', 'FirstName', 'MiddleName', 'LastName', 'FatherName', 'NickName', 'Cu_Addr', 'Occupation',
               'AddressLandMark', 'Cu_PhNo', 'Cu_MNo', 'MobNoWhatsAap', 'Email', 'Remarks', 'Debit', 'Area', 'Street',
               'Employee', 'Joining Date', 'CUSTACTIVE', 'RootNo', 'AadharNo', 'GSTIN', 'UIDNo', 'VPANo', 'PANNo',
               'BillingMode', 'Cu_PinCode', 'StateName', 'District', 'CityName', 'HOName', 'HOODE', 'Balance', 'MsoName',
               'ImportType']

# Create a new DataFrame with the mapped values
new_df = pd.DataFrame(columns=new_columns)

# Iterate through the rows in the filtered DataFrame
for index, row in filtered_df.iterrows():
    new_row = {
        'STB': '',  # Add default or mapped value as needed
        'VC': '',  # Add default or mapped value as needed
        'SAF': 0,  # Default value as 0
        'UA': 0,  # Default value as 0
        'challanno': 0,  # Default value as 0
        'STBRENT': 0,  # Default value as 0
        'STB_Security': 0,  # Default value as 0
        'STBDiscount': 0,  # Default value as 0
        'CRNNO': '',  # Add default or mapped value as needed
        'MSOID': 0,  # Default value as 0
        'StbEntryDate': '',  # Add default or mapped value as needed
        'STBACDC': 0,  # Default value as 0
        'PACK': '',  # Add default or mapped value as needed
        'BoxCompanyName': '',  # Add default or mapped value as needed
        'AccountNo': 0,  # Default value as 0
        'Customerid': row['CUSTOMER ID'],
        'MrMrs': '',  # Add default or mapped value as needed
        'InternetID': '',  # Add default or mapped value as needed
        'SubID': '',  # Add default or mapped value as needed
        'FirstName': row['NAME'],
        'MiddleName': '',  # Add default or mapped value as needed
        'LastName': '',  # Add default or mapped value as needed
        'FatherName': row['FATHER NAME'],
        'NickName': '',  # Add default or mapped value as needed
        'Cu_Addr': row['FATHER NAME'],
        'Occupation': '',  # Add default or mapped value as needed
        'AddressLandMark': '',  # Add default or mapped value as needed
        'Cu_PhNo': '',  # Add default or mapped value as needed
        'Cu_MNo': '',  # Add default or mapped value as needed
        'MobNoWhatsAap': row['MOBILE'],
        'Email': row['EMAIL'],
        'Remarks': row['PLAN'],
        'Debit': '',  # Add default or mapped value as needed
        'Area': 'SKYNET MCH' if str(row['CUSTOMER ID']).startswith('4') else 'SKYNET INTERNET',
        'Street': row['ADDRESS'],
        'Employee': 'SKYNET',
        'Joining Date': row['Timestamp'],
        'CUSTACTIVE': 1,
        'RootNo': '',  # Add default or mapped value as needed
        'AadharNo': '',  # Add default or mapped value as needed
        'GSTIN': '',  # Add default or mapped value as needed
        'UIDNo': '',  # Add default or mapped value as needed
        'VPANo': '',  # Add default or mapped value as needed
        'PANNo': '',  # Add default or mapped value as needed
        'BillingMode': 'PREPAID',
        'Cu_PinCode': '',  # Add default or mapped value as needed
        'StateName': '',  # Add default or mapped value as needed
        'District': '',  # Add default or mapped value as needed
        'CityName': '',  # Add default or mapped value as needed
        'HOName': 'SKYNET MCH' if str(row['CUSTOMER ID']).startswith('4') else 'SKYNET INTERNET',
        'HOODE': 'SKYMCH' if str(row['CUSTOMER ID']).startswith('4') else 'SKY123',
        'Balance': 0,
        'MsoName': '',  # Add default or mapped value as needed
        'ImportType': ''  # Add default or mapped value as needed
    }

    # Use pd.concat() instead of append()
    new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

# Generate the filename with current date and month
current_time = datetime.now().strftime("%d%b").lower()  # Format: 23aug
file_name = f"cif{current_time}.xlsx"

# Save the new DataFrame to an Excel file
new_df.to_excel(file_name, index=False)

print(f"Excel file saved as {file_name}")

# Upload to SSH Server using Paramiko
hostname = "123.123.123.123"
port = 22
username = "root"
private_key_path = r"C:\Users\navde\Downloads\alma8_openssh.pem"
remote_path = "/PATH_HERE/"

# Initialize SSH client
private_key = paramiko.RSAKey.from_private_key_file(private_key_path)
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, port=port, username=username, pkey=private_key)

# Use SFTP to upload the file and overwrite if it exists
sftp = ssh.open_sftp()
sftp.put(file_name, remote_path + file_name)

# Close the SFTP and SSH connection
sftp.close()
ssh.close()

print(f"File uploaded successfully to {remote_path}{file_name}")
