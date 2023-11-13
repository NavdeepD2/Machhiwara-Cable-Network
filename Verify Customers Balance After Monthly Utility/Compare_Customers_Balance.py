import tkinter as tk
from tkinter import filedialog
import pandas as pd
from datetime import datetime

def open_file(button_id):
    file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx')])
    if file_path:
        if button_id == 1:
            global file_a_path
            file_a_path = file_path
        elif button_id == 2:
            global file_b_path
            file_b_path = file_path

def compare_files():
    if file_a_path and file_b_path:
        df_a = pd.read_excel(file_a_path, sheet_name='CustomerReportportrait', header=1)
        df_b = pd.read_excel(file_b_path, sheet_name='CustomerReportportrait', header=1)

        merged_df = pd.merge(df_a, df_b, on='Cust ID', suffixes=('_Before', '_After'))

        matched_rows = merged_df[merged_df['Balance_Before'] == merged_df['Balance_After']]

        output_file = f"Same_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            matched_rows.to_excel(writer, index=False, sheet_name='DifferentRows')

        print(f"Comparison result saved to {output_file}")
    else:
        print("Please select both files before comparing.")

# GUI setup
root = tk.Tk()
root.title("Excel File Comparator")

file_a_path = None
file_b_path = None

# Buttons
before_button = tk.Button(root, text="Before", command=lambda: open_file(1))
before_button.pack(pady=10)

after_button = tk.Button(root, text="After", command=lambda: open_file(2))
after_button.pack(pady=10)

compare_button = tk.Button(root, text="Compare", command=compare_files)
compare_button.pack(pady=20)

root.mainloop()
