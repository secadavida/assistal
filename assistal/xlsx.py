from assistal.logger import log, plog
from assistal.ui import commons
from tabulate import tabulate

import pandas as pd
import os


class XLSX:

    def perform_save_on_change(self, func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            if self.write_on_change:
                self.save()

            return result

        return wrapper

    def save(self):
        self.df.to_excel(self.file_path, index=False, engine='openpyxl')

    def __init__(self, file_path: str, column_headers: list):
        self.file_path = file_path
        self.column_headers = column_headers
        self.write_on_change = False

        # custom function wrappers, because conventional decorators don't work here
        self.create_entry = self.perform_save_on_change(self.create_entry)
        self.update_entry = self.perform_save_on_change(self.update_entry)
        self.delete_entry = self.perform_save_on_change(self.delete_entry)

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

    def has_entry(self, identifier: int) -> bool:
        return identifier in self.df['identificacion'].values

    def create_entry(self, new_data) -> bool:
        if new_data["identificacion"]:
            if self.has_entry(new_data["identificacion"]):
                return False
        else:
            return False

        self.df = self.df._append(new_data, ignore_index=True)

        return True
     
    def update_entry(self, identifier, updated_data) -> bool:
        if not self.has_entry(identifier):
            return False
        
        for key, value in updated_data.items():
            if key in self.df.columns:
                self.df.loc[self.df['identificacion'] == identifier, key] = value
            else:
                return False

        return True
    
    def delete_entry(self, identifier: int) -> bool:
        if not self.has_entry(identifier):
            return False
        
        indices_to_drop = self.df.index[self.df['identificacion'] == identifier].tolist()
        self.df.drop(indices_to_drop, inplace=True)

        return True
    
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
