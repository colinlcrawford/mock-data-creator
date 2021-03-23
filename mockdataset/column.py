"""
    Contains the Column class and subclasses
"""

from __future__ import annotations
from typing import List, Dict, Any, Callable, TypeVar

T = TypeVar('T')


class Column():
    """
        The Column class represents a column in a Dataset. Each column is
        an attribute in the data set and a row is an entry with a value for each
        column.
    """

    def __init__(self,
                 column_name: str,
                 value_generator: Callable[Dict[str, Any], T] = lambda x: None):
        """
        Constructor for the Column class

        Parameters
        __________
        column_name : str
            The name of this column

        value_generator : Callable[Dict[str, Any]]
            The a callable (function) to produce a the next value for
            this column
        """
        self.column_name = column_name
        self._value_generator = value_generator

    def create_value(self,
                     total_rows: int,
                     row_number: int,
                     previous_row_values: Dict[str, Any]) -> T:
        """
        Produces this column's next value

        Uses the object's value_generator to produce a new value for this column

        Parameters
        __________
        total_rows : int
            total rows to be created using this Column
        row_number : int
            the current row who's value is being created
        previous_row_values : Dict[str, Any]
            The previous values for the row this value is being created for

        Returns
        _______
        T
            Whatever value this object's value_generator produces
        """
        return self._value_generator(
            total_rows=total_rows,
            row_number=row_number,
            previous_row_values=previous_row_values)


class MappingColumn(Column):
    def __init__(self,
                 column_name: str,
                 column_to_map: str,
                 mapping: Dict[str, Any],
                 default_value: Any):
        self._column_to_map = column_to_map
        self._mapping = mapping
        self._default_value = default_value
        super().__init__(self)

        self._value_generator = self._generate_mapped_value

    def _generate_mapped_value(self,
                               total_rows: int,
                               row_number: int,
                               previous_row_values: Dict[str, Any]) -> Any:
        mapped_column_row_val = previous_row_values.get(self._column_to_map)
        return self._mapping.get(
            mapped_column_row_val,
            self._default_value)


class PercentageDiscreteColumn(Column):
    def __init__(self,
                 column_name: str,
                 category_to_percentage: Dict[Any, float],
                 default_value):
        super().__init__(self)

        sum_percentage_values = sum(category_to_percentage.values()) * 100

        if (sum_percentage_values > 100):
            raise ValueError(
                f"percentage is greater than 100% : {sum_percentage_values}")

        self._default_value = default_value
        self._category_to_percentage = category_to_percentage
        self._percentage_upper_bounds = self._get_category_upper_percent_bounds()
        self._value_generator = self._generate_next

    def _get_category_upper_percent_bounds(self) -> Dict[Any, float]:
        category_to_upper_bound = {}
        current_upper_bound = 0
        for category, percentage_target in self._category_to_percentage.items():
            current_upper_bound += percentage_target
            category_to_upper_bound[category] = current_upper_bound
        return category_to_upper_bound

    def _generate_next(self,
                       total_rows: int,
                       row_number: int,
                       previous_row_values: Dict[str, Any]) -> Any:
        percent_rows_completed = row_number / total_rows
        incomplete_categories = [
            category for category, pct_upper_bound
            in self._percentage_upper_bounds.items()
            if pct_upper_bound > percent_rows_completed
        ]
        if incomplete_categories:
            return incomplete_categories[0]
        return self._default_value
