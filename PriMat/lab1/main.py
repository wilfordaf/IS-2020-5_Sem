import numpy as np

from lab1.entities.restriction import Restriction, RestrictionType
from lab1.entities.statement import Statement
from lab1.solution_methods.simplex_solution_method import SimplexSolutionMethod, SolutionAim


def main():
    r_1 = Restriction(np.array([3, 5]), RestrictionType.LESS, 30)
    r_2 = Restriction(np.array([4, -3]), RestrictionType.LESS, 12)
    r_3 = Restriction(np.array([1, -3]), RestrictionType.GREATER, 6)
    statement = Statement(np.array([1, 1]), [r_1, r_2, r_3])
    solution_aim = SolutionAim.MAX

    func_vector, right_hand_side, vectors, value = statement.create_statement()
    basis = statement.create_basis()
    basis_content = statement.create_basis_content()

    simplex_solution_method = SimplexSolutionMethod(
        solution_aim,
        func_vector,
        right_hand_side,
        vectors,
        basis,
        basis_content)

    func_extremum, extremum_coordinates = simplex_solution_method.solve(value)

    print(f'Function extremum: {func_extremum:.3f}')
    print(f'Extremum coordinates: {extremum_coordinates.tolist()}')


if __name__ == '__main__':
    main()
