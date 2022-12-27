import numpy as np
import re

from lab1.entities.restriction import Restriction, RestrictionType
from lab1.entities.statement import Statement
from lab1.solution_methods.simplex_solution_method import SolutionAim


class FileInputParser:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def create_statement(self) -> (Statement, SolutionAim):
        function, restrictions, solution_aim, basis = self.__parse_file_to_expression()

        func_coefficients = function[0]
        value = function[-1]
        restrictions = np.array([Restriction(*restriction) for restriction in restrictions])

        statement = Statement(func_coefficients=func_coefficients,
                                restrictions=restrictions,
                                value=value,
                                input_basis=basis)

        return statement, solution_aim

    def __parse_file_to_expression(self) -> (tuple, list, SolutionAim, np.array):
        with open(self.file_path, "r") as f_in:
            variables_count, restrictions_count, solution_aim, override_basis = f_in.readline().split()
            variables_count, restrictions_count = int(variables_count), int(restrictions_count)
            solution_aim = self.__parse_solution_aim(solution_aim.lower())
            override_basis = bool(override_basis)

            function_data = f_in.readline()
            function = self.__parse_expression_to_vector(function_data, variables_count)

            restrictions = []
            for _ in range(restrictions_count):
                restriction_data = f_in.readline()
                restrictions.append(self.__parse_expression_to_vector(restriction_data, variables_count))

            basis = None
            if override_basis:
                basis_data = re.sub("\(|\)| ", "", f_in.readline())
                basis = np.array(list(map(float, basis_data.split(","))))

            return function, restrictions, solution_aim, basis

    @classmethod
    def __parse_expression_to_vector(cls, expr: str, variables_count: int) -> (np.array, RestrictionType, float):
        expression = expr.replace("\n", "")

        expression_value = float(re.split("[<=|>=|=]", expression)[-1].replace(" ", ""))
        expression_sign = cls.__get_expression_sign(expression)

        expression_coefficients = np.zeros(variables_count)
        expression_blocks = re.findall("[-|+]\d \* x_\d+", expr)
        for item in expression_blocks:
            item = item.replace(" ", "")
            item_coefficient, item_variable = item.split("*")
            variable_number = int(item_variable.replace("x_", ""))
            expression_coefficients[variable_number - 1] = float(item_coefficient)

        return expression_coefficients, expression_sign, expression_value

    @staticmethod
    def __get_expression_sign(expr: str) -> RestrictionType:
        if "<=" in expr:
            return RestrictionType.LESS
        elif ">=" in expr:
            return RestrictionType.GREATER
        elif "=" in expr:
            return RestrictionType.EQUAL

        raise SyntaxError("Expression sign is not found")

    @staticmethod
    def __parse_solution_aim(solution_aim: str) -> SolutionAim:
        return SolutionAim[SolutionAim(solution_aim).name]
