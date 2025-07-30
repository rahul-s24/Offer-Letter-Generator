import pandas as pd

def load_employee(name: str, csv_path: str):
    df = pd.read_csv(csv_path)
    emp_row = df[df['Employee Name'].str.strip().str.lower() == name.strip().lower()]
    if emp_row.empty:
        raise ValueError(f"Employee {name} not found.")
    return emp_row.iloc[0].to_dict()