import os
import numpy as np
import pandas as pd

class CSV:

    def __init__(self, name):

        self.name = name.strip().lower()
        self.excel_directory = fr"{os.path.dirname(os.path.abspath(__file__))}\{self.name}.csv"  # Path to the CSV file
       
        try:
            # Load the CSV file into a DataFrame using ISO-8859-1 encoding to handle special characters
            self.df = pd.read_csv(self.excel_directory, encoding='utf-8-sig')  # Reading CSV into pandas DataFrame

        except FileNotFoundError:
            print(f'File not found. Check if "{name}" exists in the directory {os.path.dirname(os.path.abspath(__file__))}')
            raise SystemExit
            

    def full_file(self):
        return self.df

    # Get the list of column names in the DataFrame
    def columns(self):
        return self.df.columns.tolist()

    # Get the list of values in a specific column of the DataFrame
    def rows(self, column):
        return self.df[column].tolist()

    # Insert a row with NaN values at a specified index
    def insert_none_at(self, index):
        new_row = {column: np.nan for column in self.df.columns}  # Create a new row with NaN values
        self.df = pd.concat([  # Insert the NaN row at the specified index
            self.df.iloc[:index],
            pd.DataFrame([new_row]),
            self.df.iloc[index:]
        ], ignore_index=True)
        


