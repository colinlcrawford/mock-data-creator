"""
    Package to allow the easy creation of sample datasets
"""

from __future__ import annotations
from typing import List, Dict, Any
import pandas as pd

from mockdataset.column import Column


class Dataset():
    """
        A Dataset represents a table like dataset with rows and columns
        of data. Each columns represents an attribute and rows an entry.
    """

    def __init__(self,
                 columns: List[Column],
                 number_of_rows: int):
        """
        constructor for the Dataset class

        Parameters
        __________
        columns : List[Column]
            The columns that will be used to create the dataset

        number_of_rows : int
            The number of rows in the dataset
        """
        if number_of_rows <= 0:
            raise ValueError("Datasets must contain at least 1 row")

        self.columns = columns
        self.number_of_rows = number_of_rows
        self._current_row = 0

    def __iter__(self) -> Dataset:
        """
        sets up the Dataset instance to be iterated through and returns it
        as an interable
        """
        self._current_row = 0
        return self

    def __next__(self) -> Dict[str, Any]:
        """
        step function for iterating through the dataset
        """
        self._current_row += 1

        if self._current_row > self.number_of_rows:
            raise StopIteration

        return self.get_next_row(self._current_row)

    def get_next_row(self, row_number: int) -> Dict[str, Any]:
        """
        returns the next row for this dataset

        Parameters
        __________
        row_number : int
            The current row number

        Returns
        _______
        Dict[str, Any]
            The provious columns in the row in a dict {"column_name": column_value}
        """
        column_values = {}

        for column in self.columns:
            next_value = column.create_value(
                total_rows=self.number_of_rows,
                row_number=row_number,
                previous_row_values=column_values,
            )
            column_values[column.column_name] = next_value

        return column_values

    def to_list(self) -> List[List[str, Any]]:
        """
        Returns a 2d list representation of the dataset
        """
        lst = []
        column_names = [col.column_name for col in self.columns]
        lst.append(column_names)
        for row in self:
            lst.append([row[col_name] for col_name in column_names])
        return lst

    def to_df(self) -> pd.DataFrame:
        """
        Returns a pandas dataframe representation of the dataset
        """
        pass

    def to_csv(self, filename: str):
        """
        Writes this dataset out to a csv

        Parameters
        __________
        filename : str
            Name of the file to write to
        """
        pass
