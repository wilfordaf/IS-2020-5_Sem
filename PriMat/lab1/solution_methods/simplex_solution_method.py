import numpy as np

from enum import Enum


class SolutionAim(Enum):
    MIN = "min"
    MAX = "max"


class SimplexSolutionMethod:

    MAX_ITERATION_COUNT = 1000

    def __init__(self,
                 solution_aim: SolutionAim,
                 func_vector: np.array,
                 right_hand_side: np.array,
                 vectors: np.array,
                 basis: np.array,
                 basis_content: np.array):

        self.solution_aim = solution_aim
        self.func_vector = func_vector
        self.right_hand_side = right_hand_side
        self.vectors = vectors
        self.basis = basis
        self.basis_content = basis_content

    def solve(self, val: float) -> (np.array, float):
        new_basis_content = np.copy(self.basis_content)

        b_j = np.dot(self.basis, self.right_hand_side)
        a_j = np.array([])
        for index, vector in enumerate(self.vectors):
            a_j = np.append(a_j, np.dot(self.basis, vector) - self.func_vector[index])

        iteration_count = 0

        while self.__check_solution_is_invalid(a_j):
            permissive_column, permissive_line, permissive_element = self.__find_permissive_element(a_j)

            new_basis_content[permissive_line] = permissive_column
            self.basis[permissive_line] = self.func_vector[permissive_column]

            new_right_hand_side = np.full(self.right_hand_side.shape, np.inf)
            new_right_hand_side[permissive_line] = self.right_hand_side[permissive_line] / permissive_element
            for index, value in enumerate(new_right_hand_side):
                if value != np.inf:
                    continue

                multiplier = self.right_hand_side[permissive_line] * self.vectors[permissive_column, index]
                subtrahend = multiplier / permissive_element
                new_right_hand_side[index] = self.right_hand_side[index] - subtrahend

            new_vectors = np.full(self.vectors.shape, np.inf)
            for index, value in enumerate(self.vectors[:, permissive_line]):
                new_vectors[index, permissive_line] = value / permissive_element

            for index, line_number in enumerate(new_basis_content):
                new_vectors[line_number, :] = 0
                new_vectors[line_number, index] = 1

            for index_cl, line in enumerate(new_vectors):
                for index_ln, value in enumerate(line):
                    if value != np.inf:
                        continue

                    multiplier = self.vectors[permissive_column, index_ln] * self.vectors[index_cl, permissive_line]
                    subtrahend = multiplier / permissive_element

                    new_vectors[index_cl, index_ln] = self.vectors[index_cl, index_ln] - subtrahend

            b_j = np.dot(self.basis, new_right_hand_side)
            a_j = np.array([])
            for index, vector in enumerate(new_vectors):
                a_j = np.append(a_j, np.dot(self.basis, vector) - self.func_vector[index])

            self.right_hand_side = new_right_hand_side
            self.vectors = new_vectors

            if iteration_count == SimplexSolutionMethod.MAX_ITERATION_COUNT:
                raise ValueError("Extremum is not defined")
            iteration_count += 1

        return self.__make_answer(b_j + val, new_basis_content)

    def __check_solution_is_invalid(self, a_j: np.array) -> bool:
        return np.any(a_j > 0) if self.solution_aim == SolutionAim.MIN else np.any(a_j < 0)

    def __find_permissive_line(self, permissive_column: int) -> int:
        permissive_line = -1
        min_value = np.inf

        for index, value in enumerate(self.vectors[permissive_column]):
            if value <= 0:
                continue

            divided_value = self.right_hand_side[index] / value
            if divided_value < min_value:
                min_value = divided_value
                permissive_line = index

        return permissive_line

    def __find_permissive_element(self, a_j: np.array) -> (int, int, int):
        permissive_lines = np.where(self.right_hand_side < 0)[0]
        if permissive_lines.size != 0:
            permissive_line = permissive_lines[0]
            permissive_columns = np.where(self.vectors[:, permissive_line] < 0)[0]
            if permissive_columns.size == 0:
                raise ValueError("Extremum is not defined")

            permissive_column = permissive_columns[0]
            return permissive_column, permissive_line, self.vectors[permissive_column][permissive_line]

        match self.solution_aim:
            case SolutionAim.MIN:
                permissive_column = int(np.argmax(a_j))
            case SolutionAim.MAX:
                permissive_column = int(np.argmin(a_j))
            case _:
                raise ValueError("Unknown solution aim")

        permissive_line = self.__find_permissive_line(permissive_column)
        return permissive_column, permissive_line, self.vectors[permissive_column][permissive_line]

    def __make_answer(self, result: float, new_basis_content: np.array) -> (float, np.array):
        non_zero_indexes = np.isin(new_basis_content, self.basis_content, invert=True)
        answer = np.zeros(self.func_vector.size - self.basis.size)
        for index, value in enumerate(non_zero_indexes):
            if value:
                answer[new_basis_content[index]] = round(self.right_hand_side[index], 6)

        return round(result, 6), answer
