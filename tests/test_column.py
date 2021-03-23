"""
    Unit tests for Column class
"""

import unittest
from mockdataset.column import Column, MappingColumn, PercentageDiscreteColumn


def test_value_generator_fn(total_rows, row_number, previous_row_values):
    """
    test value generator function for the test column
    """
    return 10


class TestColumn(unittest.TestCase):
    """
        Unit tests for Column class
    """

    def setUp(self):
        """
        test set up
        """
        self.column = Column(
            column_name="test_column",
            value_generator=test_value_generator_fn)

    def test_init(self):
        """
        test that Column initializes correctly
        """
        self.assertEqual(self.column.column_name, "test_column")

    def test_create_value(self):
        """
        test that Column call its create_value function correctly
        """
        test_total_rows = 10
        test_row_number = 0
        test_previous_row_values = []

        column_next_value = self.column.create_value(
            total_rows=test_total_rows,
            row_number=test_row_number,
            previous_row_values=test_previous_row_values)

        expected_next_value = test_value_generator_fn(
            total_rows=test_total_rows,
            row_number=test_row_number,
            previous_row_values=test_previous_row_values)

        self.assertEqual(column_next_value, expected_next_value)


class TestMappingColumn(unittest.TestCase):
    def setUp(self):
        test_mapping = {
            "Whale": "Big",
            "Cat": "Small"
        }
        self.test_previous_rows_with_match = {
            "Animal": "Whale"
        }
        self.test_previous_rows_without_match = {
            "Animal": "Dog"
        }
        self.test_default_value = "Medium"
        self.column = MappingColumn(
            column_name="Size",
            column_to_map="Animal",
            mapping=test_mapping,
            default_value=self.test_default_value)

    def test_create_value(self):
        next_value = self.column.create_value(
            total_rows=10,
            row_number=3,
            previous_row_values=self.test_previous_rows_with_match)
        self.assertEqual(next_value, "Big")

    def test_default_value_for_unmapped_values(self):
        next_value = self.column.create_value(
            total_rows=10,
            row_number=3,
            previous_row_values=self.test_previous_rows_without_match)
        self.assertEqual(next_value, self.test_default_value)


class TestPercentageDiscreteColumn(unittest.TestCase):
    def setUp(self):
        self.test_category_to_percentage = {
            "Cat": 0.2,
            "Dog": 0.2,
            "Whale": 0.2,
            "Lion": 0.4
        }
        self.column = PercentageDiscreteColumn(
            column_name="Animal",
            category_to_percentage=self.test_category_to_percentage,
            default_value="Lion"
        )

        self.test_category_to_percentage_not_all_covered = {
            "Cat": 0.33,
            "Dog": 0.33,
        }
        self.column_not_all_covered = PercentageDiscreteColumn(
            column_name="Animal",
            category_to_percentage=self.test_category_to_percentage_not_all_covered,
            default_value="Lion"
        )

    def test_create_value(self):
        """
        test the PercentageDiscreteColumn creates the correct number of each
        user provided value based on the percentages provided by the user
        """
        total_test_rows = 5
        values = []
        for i in range(total_test_rows):
            values.append(self.column.create_value(
                total_rows=total_test_rows,
                row_number=i,
                previous_row_values=values))

        expected_values = [*self.test_category_to_percentage.keys(), "Lion"]
        for value, expected_value in zip(values, expected_values):
            self.assertEqual(value, expected_value)

    def test_create_default_value(self):
        """
        test the PercentageDiscreteColumn uses it's default value once it has
        filled the required percentages from the user for the column
        """
        total_test_rows = 3
        values = []
        for i in range(total_test_rows):
            values.append(self.column_not_all_covered.create_value(
                total_rows=total_test_rows,
                row_number=i,
                previous_row_values=values))

        expected_values = [
            *self.test_category_to_percentage_not_all_covered.keys(),
            "Lion"
        ]
        for value, expected_value in zip(values, expected_values):
            self.assertEqual(value, expected_value)
