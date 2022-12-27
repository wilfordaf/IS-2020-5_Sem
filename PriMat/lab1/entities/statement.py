import numpy as np

from lab1.entities.restriction import Restriction, RestrictionType


class Statement:
    def __init__(self,
                 func_coefficients: np.array,
                 restrictions: np.array,
                 value: float = 0,
                 input_basis: np.array = None):

        self.func_coefficients = func_coefficients
        self.restrictions = restrictions
        self.value = value
        self.input_basis = input_basis

    def __str__(self):
        return f"{self.func_coefficients} {self.restrictions} {self.value} {self.input_basis}"

    def __restrictions_count(self) -> int:
        return len(self.restrictions)

    def __transform_equations(self) -> None:
        new_restrictions = np.array([])
        for index, restriction in enumerate(self.restrictions):
            if restriction.restriction_type != RestrictionType.EQUAL:
                new_restrictions = np.append(new_restrictions, restriction)
                continue

            new_r_less = Restriction(restriction.coefficients, RestrictionType.LESS, restriction.value)
            new_r_greater = Restriction(restriction.coefficients, RestrictionType.GREATER, restriction.value)
            new_restrictions = np.append(new_restrictions, np.array([new_r_less, new_r_greater]))

        self.restrictions = np.copy(new_restrictions)

    def to_canonical(self) -> None:
        self.__transform_equations()
        for restriction in self.restrictions:
            restriction.to_canonical()

    def create_statement(self) -> (np.array, np.array, np.array, float):
        self.to_canonical()
        func_vector = np.concatenate((self.func_coefficients, np.zeros(self.__restrictions_count())))
        right_hand_side = np.array([])
        vectors = []

        for index, restriction in enumerate(self.restrictions):
            additional_vector = np.zeros(self.__restrictions_count())
            right_hand_side = np.append(right_hand_side, restriction.value)
            additional_vector[index] = -1 if restriction.restriction_type == RestrictionType.GREATER else 1
            vectors.append(np.concatenate((restriction.coefficients, additional_vector)))

        vectors = np.asarray(vectors)
        vectors_transpose = vectors.T

        return func_vector, right_hand_side, vectors_transpose, self.value

    def create_basis(self) -> np.array:
        if self.input_basis is not None:
            basis = np.concatenate((self.input_basis, np.zeros(self.__restrictions_count() - self.input_basis.size)))
            return basis

        return np.zeros(self.__restrictions_count())

    def create_basis_content(self) -> np.array:
        return np.arange(
            self.func_coefficients.size,
            self.func_coefficients.size + self.__restrictions_count(),
            step=1)
