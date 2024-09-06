from assistal.logger import log, plog
from assistal.ui import commons
from tabulate import tabulate

import pandas as pd
import types
import os


class XLSX:
    def __init__(self, file_path: str, column_headers: list):
        self.file_path = file_path
        self.column_headers = column_headers

        if XLSX.file_exists(file_path, column_headers):
            self.df: pd.DataFrame = pd.read_excel(file_path, engine='openpyxl')

        return None

    @classmethod
    def file_exists(cls, destination_file, column_headers) -> bool:
        df = pd.DataFrame(columns=column_headers)
        
        if not os.path.isfile(destination_file):
            plog("warning", f"no hay un archivo presente en '{destination_file}'")
            response = commons.show_form({"Deseas crearlo?": ["si", "no"]})[0]
            if response == "no":
                return False

            df.to_excel(destination_file, index=False, engine='openpyxl')

        return True
    

    def save(self):
        self.df.to_excel(self.file_path, index=False, engine='openpyxl')
    
    def create_entry(self, new_data):
        # Check if the identifier already exists
        if new_data['identificacion'] in self.df['identificacion'].values:
            raise ValueError(f"ID {new_data['identificacion']} already exists.")
        self.df = self.df.append(new_data, ignore_index=True)
    
    def read_entry(self, identifier: int):
        return identifier in self.df['identificacion'].values
    
    def update_entry(self, identifier, updated_data):
        if identifier not in self.df['identificacion'].values:
            raise ValueError(f"No entry found for ID {identifier}")
        
        for key, value in updated_data.items():
            if key in self.df.columns:
                self.df.loc[self.df['identificacion'] == identifier, key] = value
            else:
                raise KeyError(f"Column '{key}' not found in DataFrame")
    
    def delete_entry(self, identifier):
        if identifier not in self.df['identificacion'].values:
            raise ValueError(f"No entry found for ID {identifier}")
        
        indices_to_drop = self.df.index[self.df['identificacion'] == identifier].tolist()
        
        # drop the rows in place
        self.df.drop(indices_to_drop, inplace=True)
    
    def pretty_print(self):
        print(tabulate(self.df, headers='keys', tablefmt='grid', showindex=False))

# # Example usage
# file_path = 'example.xlsx'
#
# # Load Excel data
# df = load_excel(file_path)
#
# # Example data
# new_entry = {
#     'acudiente': 'Carlos',
#     'parentesco': 'tio',
#     'grado': 9,
#     'grupo': 'A',
#     'identificacion': 1234,
#     'nombre_estudiante': 'Carlos Smith'
# }
#
# # Create a new entry
# df = create_entry(df, new_entry)
#
# # Read an entry
# entry = read_entry(df, 5200)  # Reading entry by ID
# print(entry)
#
# # Update an entry
# df = update_entry(df, 5200, {'nombre_estudiante': 'Amanda E.'})
#
# # Delete an entry
# df = delete_entry(df, 9371)  # Deleting entry by ID
#
# # Save changes to Excel
# save_excel(df, file_path)
