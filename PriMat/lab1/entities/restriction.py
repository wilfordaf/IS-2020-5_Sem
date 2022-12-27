import numpy as np

from enum import Enum


class RestrictionType(Enum):
    EQUAL = "="
    GREATER = ">="
    LESS = "<="


class Restriction:
    def __init__(self,
                 coefficients: np.array,
                 restriction_type: RestrictionType,
                 value: float):

        self.coefficients = coefficients
        self.restriction_type = restriction_type
        self.value = value

    def __str__(self):
        return f"{self.coefficients} {self.restriction_type.value} {self.value}"

    def __check_incorrect_data(self) -> bool:
        is_blank = np.all(self.coefficients == 0) and self.value == 0
        is_incorrect = (np.all(self.coefficients > 0)
                        and self.value < 0
                        and self.restriction_type == RestrictionType.LESS)

        return is_blank or is_incorrect

    def to_canonical(self) -> None:
        if self.__check_incorrect_data():
            raise ValueError("Incorrect data")

        if self.restriction_type == RestrictionType.GREATER:
            self.coefficients = -self.coefficients
            self.value = -self.value
            self.restriction_type = RestrictionType.LESS
