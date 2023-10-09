import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd


def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xls")])
    if file_path:
        try:
            # Read the XLS file
            xls_df = pd.read_excel(file_path)

            # Get the file name without extension
            file_name = file_path.split("/")[-1].split(".")[0]

            # Create a new XLSX file name with "_conv" appended
            xlsx_file_name = file_name + "_conv.xlsx"

            # Save the DataFrame as XLSX
            xls_df.to_excel(xlsx_file_name, index=False)

            # Show a success message
            messagebox.showinfo("Success", f"Conversion complete. File saved as {xlsx_file_name}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Create the main window
root = tk.Tk()
root.title("XLS to XLSX Converter")

# Create a Browse button
browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
