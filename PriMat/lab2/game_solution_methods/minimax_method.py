import numpy as np


class MinimaxMethod:
    def __init__(self, matrix: np.array):
        self.__matrix = matrix
        self.max_min_row_element_indices = None
        self.min_max_column_element_indices = None

    def solve(self) -> None:
        min_row_indexes = np.argmin(self.__matrix, axis=1)
        min_row_elements = np.min(self.__matrix, axis=1)
        max_min_row_element_index = np.argmax(min_row_elements)
        self.max_min_row_element_indices = (
            max_min_row_element_index,
            min_row_indexes[max_min_row_element_index]
        )

        max_column_indexes = np.argmax(self.__matrix, axis=0)
        max_column_elements = np.max(self.__matrix, axis=0)
        min_max_column_element_index = np.argmin(max_column_elements)
        self.min_max_column_element_indices = (
            max_column_indexes[min_max_column_element_index],
            min_max_column_element_index
        )

    def has_saddle_point(self) -> bool:
        return self.max_min_row_element_indices == self.min_max_column_element_indices
