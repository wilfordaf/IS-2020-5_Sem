import numpy as np

from lab3.model_solution_methods.SolutionMethod import SolutionMethod


class AnalyticalSolutionMethod(SolutionMethod):
    def __init__(self, transition_matrix: np.ndarray):
        self.__transition_matrix = transition_matrix.T
        self.__stable_state_matrix = None
        self.__stable_transition_matrix = None

    def __make_equations(self) -> np.ndarray:
        equations = self.__transition_matrix - np.eye(self.__transition_matrix.shape[0])
        probability_equation = np.ones(self.__transition_matrix.shape[0])
        equations = np.vstack((equations, probability_equation))
        return equations

    def compute_stable_state_matrix(self) -> np.ndarray:
        equations = self.__make_equations()
        right_hand_side = np.zeros(equations.shape[0])
        right_hand_side[-1] = 1
        self.__stable_state_matrix = np.linalg.lstsq(equations, right_hand_side, rcond=-1)[0]
        return np.around(self.__stable_state_matrix, decimals=6)

    def compute_stable_transition_matrix(self) -> np.ndarray:
        self.__stable_transition_matrix = np.array([self.__stable_state_matrix] * self.__transition_matrix.shape[0])
        return np.around(self.__stable_transition_matrix, decimals=6)

    def get_graph_data(self) -> np.ndarray:
        ...
