import unittest
import numpy as np

from lab1.entities.restriction import Restriction, RestrictionType
from lab1.entities.statement import Statement
from lab1.solution_methods.simplex_solution_method import SimplexSolutionMethod, SolutionAim
from lab1.input_parsers.file_input_parser import FileInputParser


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        np.seterr(all="ignore")

    def test_case_1(self):
        parser = FileInputParser("input.txt")
        statement, solution_aim = parser.create_statement()

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)

        self.assertEqual(-4, func_extremum)
        self.assertTrue(np.array_equal(np.array([0, 4, 0, 0]), extremum_coordinates))

    def test_case_2(self):
        r_1 = Restriction(np.array([3, 2, 5]), RestrictionType.LESS, 18)
        r_2 = Restriction(np.array([4, 2, 3]), RestrictionType.LESS, 16)
        r_3 = Restriction(np.array([2, 1, 1]), RestrictionType.GREATER, 4)
        statement = Statement(np.array([3, 2, 4]), [r_1, r_2, r_3])
        solution_aim = SolutionAim.MAX

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)

        self.assertEqual(17, func_extremum)
        self.assertTrue(np.array_equal([0, 6.5, 1], extremum_coordinates))

    def test_case_3(self):
        r_1 = Restriction(np.array([1, 2]), RestrictionType.LESS, 7)
        r_2 = Restriction(np.array([2, 1]), RestrictionType.LESS, 8)
        r_3 = Restriction(np.array([0, 1]), RestrictionType.LESS, 3)
        statement = Statement(np.array([-3, -2]), [r_1, r_2, r_3])
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)

        self.assertEqual(-13, func_extremum)
        self.assertTrue(np.array_equal(np.array([3, 2]), extremum_coordinates))

    def test_case_4(self):
        r_1 = Restriction(np.array([1, 1]), RestrictionType.GREATER, 1)
        r_2 = Restriction(np.array([2, -1]), RestrictionType.GREATER, -1)
        r_3 = Restriction(np.array([1, -2]), RestrictionType.LESS, 0)
        statement = Statement(np.array([-1, -2]), [r_1, r_2, r_3])
        solution_aim = SolutionAim.MIN

        self.assertRaises(ValueError, Tests.simplex_solution_method_solve, statement, solution_aim)

    def test_case_5(self):
        r_1 = Restriction(np.array([3, -1, 0, 2, 1]), RestrictionType.EQUAL, 5)
        r_2 = Restriction(np.array([2, -3, 1, 2, 1]), RestrictionType.EQUAL, 6)
        r_3 = Restriction(np.array([3, -1, 1, 3, 2]), RestrictionType.EQUAL, 9)
        statement = Statement(np.array([-5, 4, -1, -3, -5]), [r_1, r_2, r_3])
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-17, func_extremum)
        self.assertTrue(np.array_equal(np.array([1, 0, 2, 0, 2]), extremum_coordinates))

    def test_case_6(self):
        r_1 = Restriction(np.array([1, 2]), RestrictionType.LESS, 4)
        r_2 = Restriction(np.array([1, -1]), RestrictionType.GREATER, 1)
        r_3 = Restriction(np.array([1, 1]), RestrictionType.LESS, 8)
        statement = Statement(np.array([-1, 3]), [r_1, r_2, r_3])
        solution_aim = SolutionAim.MAX

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(1, func_extremum)
        self.assertTrue(np.array_equal(np.array([2, 1]), extremum_coordinates))

    def test_case_7(self):
        r_1 = Restriction(np.array([3, 1, -1, 1]), RestrictionType.EQUAL, 4)
        r_2 = Restriction(np.array([5, 1, 1, -1]), RestrictionType.EQUAL, 4)
        statement = Statement(np.array([-6, -1, -4, 5]), [r_1, r_2], input_basis=np.array([1, 0, 0, 1]))
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-4, func_extremum)
        self.assertTrue(np.array_equal(np.array([0, 4, 0, 0]), extremum_coordinates))

    def test_case_8(self):
        r_1 = Restriction(np.array([1, -3, -1, -2]), RestrictionType.EQUAL, -4)
        r_2 = Restriction(np.array([1, -1, 1, 0]), RestrictionType.EQUAL, 0)
        statement = Statement(np.array([-1, -2, -3, 1]), [r_1, r_2], input_basis=np.array([0, 1, 1, 0]))
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-6, func_extremum)
        self.assertTrue(np.array_equal(np.array([2, 2, 0, 0]), extremum_coordinates))

    def test_case_9(self):
        r_1 = Restriction(np.array([1, 1, 0, 2, 1]), RestrictionType.EQUAL, 5)
        r_2 = Restriction(np.array([1, 1, 1, 3, 2]), RestrictionType.EQUAL, 9)
        r_3 = Restriction(np.array([0, 1, 1, 2, 1]), RestrictionType.EQUAL, 6)
        statement = Statement(np.array([-1, -2, -1, 3, -1]), [r_1, r_2, r_3], input_basis=np.array([0, 0, 1, 2, 1]))
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-11, func_extremum)
        self.assertTrue(np.array_equal(np.array([3, 2, 4, 0, 0]), extremum_coordinates))

    def test_case_10(self):
        r_1 = Restriction(np.array([1, 1, 2, 0, 0]), RestrictionType.EQUAL, 4)
        r_2 = Restriction(np.array([0, -2, -2, 1, -1]), RestrictionType.EQUAL, -6)
        r_3 = Restriction(np.array([1, -1, 6, 1, 1]), RestrictionType.EQUAL, 12)
        statement = Statement(np.array([-1, -1, -1, 1, -1]), [r_1, r_2, r_3], input_basis=np.array([1, 1, 2, 0, 0]))
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-10, func_extremum)
        self.assertTrue(np.array_equal(np.array([4, 0, 0, 1, 7]), extremum_coordinates))

    def test_case_11(self):
        r_1 = Restriction(np.array([1, 1, -1, -10]), RestrictionType.EQUAL, 0)
        r_2 = Restriction(np.array([1, 14, 10, -10]), RestrictionType.EQUAL, 11)
        statement = Statement(np.array([-1, 4, -3, 10]), [r_1, r_2])
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-4, func_extremum)
        self.assertTrue(np.array_equal(np.array([1, 0, 1, 0]), extremum_coordinates))

    def test_case_12(self):
        r_1 = Restriction(np.array([1, 3, 3, 1]), RestrictionType.LESS, 3)
        r_2 = Restriction(np.array([2, 0, 3, -1]), RestrictionType.LESS, 4)
        statement = Statement(np.array([-1, 5, 1, -1]), [r_1, r_2])
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(-3, func_extremum)
        self.assertTrue(np.array_equal(np.array([2.333333, 0, 0, 0.666667]), extremum_coordinates))

    def test_case_13(self):
        r_1 = Restriction(np.array([3, 1, 1, 1, -2]), RestrictionType.EQUAL, 10)
        r_2 = Restriction(np.array([6, 1, 2, 3, -4]), RestrictionType.EQUAL, 20)
        r_3 = Restriction(np.array([10, 1, 3, 6, -7]), RestrictionType.EQUAL, 30)
        statement = Statement(np.array([-1, -1, 1, -1, 2]), [r_1, r_2, r_3])
        solution_aim = SolutionAim.MIN

        func_extremum, extremum_coordinates = Tests.simplex_solution_method_solve(statement, solution_aim)
        self.assertEqual(10, func_extremum)
        self.assertTrue(np.array_equal(np.array([0, 0, 10, 0, 0]), extremum_coordinates))

    @staticmethod
    def simplex_solution_method_solve(statement: Statement, solution_aim: SolutionAim) -> (float, np.array):
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
        # print(f'Function extremum: {func_extremum:.3f}')
        # print(f'Extremum coordinates: {extremum_coordinates.tolist()}')
        return func_extremum, extremum_coordinates


if __name__ == '__main__':
    unittest.main()
