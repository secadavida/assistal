from typing import Any, Dict, List, Optional, Type, Union

from assistal.classes.Base import Base
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

    def __init__(self, file_path: str, column_headers: List[str]):
        self.file_path = file_path
        self.column_headers = column_headers
        self.write_on_change = False

        # custom function wrappers, because conventional decorators don't work here
        self.create_entry = self.perform_save_on_change(self.create_entry)
        self.update_entry = self.perform_save_on_change(self.update_entry)
        self.delete_entry = self.perform_save_on_change(self.delete_entry)

        if XLSX.file_exists(file_path, self.column_headers):
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

    # query by specific row index
    def get_row(self, row_index: int) -> Optional[Dict[str, Any]]:

        # if row index is within range
        if 0 <= row_index < len(self.df):
            return self.df.iloc[row_index].to_dict()

        return None

    def make_query_mask(self, _query: Dict[str, Any]) -> pd.Series:

        # Remove any keys from the query where the value is NaN
        _query = {k: v for k, v in _query.items() if not pd.isna(v)}

        # Construct a boolean mask based on the criteria
        mask = pd.Series([True] * len(self.df))  # Start with a mask of True values

        for column, value in _query.items():
            if column in self.df.columns:
                mask &= (self.df[column] == value)
            else:
                raise ValueError(f"Column '{column}' does not exist in DataFrame")

        return mask

    def query(self, _query: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """
        Check if there are entries in the DataFrame that match all the given identifiers.

        Parameters:
        _query (dict): A query matching columns and the values to match them for.

        Returns:
        List[dict] or None: A list of dictionaries representing the rows that match the query.
                            If no match is found, return None.
        """
        mask = self.make_query_mask(_query)

        # Filter the DataFrame for matching rows
        matching_rows = self.df[mask]

        if not matching_rows.empty:
            # Manually convert each row to a dictionary and return as a list
            result = []
            for _, row in matching_rows.iterrows():
                result.append(row.to_dict())
            return result

        # Return None if no match is found
        return None

    def create_entry(self, new_data: Dict[str, Any]) -> bool:
        if self.query(new_data):
            return False

        self.df = self.df._append(new_data, ignore_index=True)

        return True
     
    def update_entry(self, _query: Dict[str, Any], updated_data: Dict[str, Any]) -> bool:
        if not _query:
            return False

        if not self.query(_query):
            return False

        # Construct a boolean mask based on the identifiers
        mask = self.make_query_mask(_query)

        if not mask.any():
            return False
        
        # Update the matching rows with the updated_data
        for key, value in updated_data.items():
            if key in self.df.columns:
                if value is not None:
                    self.df.loc[mask, key] = value
            else:
                raise ValueError(f"Column '{key}' does not exist in DataFrame")

        return True
    
    def delete_entry(self, _query: Dict[str, Any]) -> bool:
        if not _query:
            return False

        # Use the query method to check if any entry matches the identifiers
        if not self.query(_query):
            return False

        # Construct a boolean mask based on the identifiers
        mask = self.make_query_mask(_query)

        # Get indices to drop
        indices_to_drop = self.df.index[mask].tolist()

        if not indices_to_drop:
            return False

        # Drop the rows from the DataFrame
        self.df.drop(indices_to_drop, inplace=True)

        return True
    
    def pretty_print(self, show_index: bool = False):
        print(tabulate(self.df, headers='keys', tablefmt='grid', showindex=show_index))
