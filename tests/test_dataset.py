"""
    Unit tests for Dataset class
"""

import unittest

from mockdataset.dataset import Dataset
from mockdataset.column import Column


def test_value_generator(total_rows, row_number, previous_row_values):
    """
    test function for generating column values

    Returns
    _______
    int
        the row number plus the previous row value (or zero if it's the first)
    """
    return row_number + len(previous_row_values)


TEST_COLUMNS = [
    Column(column_name=f"test{i}", value_generator=test_value_generator)
    for i in range(10)
]

TEST_NUM_ROWS = 10


class TestDataset(unittest.TestCase):
    """
        Unit tests for Dataset class
    """

    def setUp(self):
        """
        run before each test
        """
        self.dataset = Dataset(
            columns=TEST_COLUMNS,
            number_of_rows=TEST_NUM_ROWS)

    def test_init(self):
        """
        test Dataset get initialized correctly
        """
        self.assertEqual(
            self.dataset.columns,
            TEST_COLUMNS)

        self.assertEqual(
            self.dataset.number_of_rows,
            TEST_NUM_ROWS)

    def test_get_next_row(self):
        """
        test the ability to get rows based on a Dataset's columns
        """
        next_row = self.dataset.get_next_row(1)
        self.assertEqual(len(next_row), TEST_NUM_ROWS)
        for i, val in enumerate(next_row.values()):
            self.assertEqual(val, i+1)

    def test_iteration(self):
        """
        test the ability to iterate through a Dataset object
        """
        row_sums = [sum(row.values()) for row in self.dataset]
        self.assertEqual(len(row_sums), TEST_NUM_ROWS)
        for i, row_sum in enumerate(row_sums):
            expected_sum = sum([j + i for j in range(1, TEST_NUM_ROWS + 1)])
            self.assertEqual(row_sum, expected_sum)

    def test_to_list(self):
        """
        test the to_list method
        """
        lst = self.dataset.to_list()
        test_column_titles = [col.column_name for col in TEST_COLUMNS]
        for column_title, test_column_title in zip(lst[0], test_column_titles):
            self.assertEqual(column_title, test_column_title)
        for i, row in enumerate(lst[1:]):
            for j, val in enumerate(row):
                self.assertEqual(val, i + 1 + j)

    def test_to_df(self):
        """
        test the to_df method
        (get a pandas dataframe representation of the Dataset)
        """
        pass

    def test_to_csv(self):
        """
        test the to_csv method (write the Dataset out to a csv)
        """
        pass
