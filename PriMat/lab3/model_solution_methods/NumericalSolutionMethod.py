import numpy as np

from lab3.model_solution_methods.SolutionMethod import SolutionMethod


class NumericalSolutionMethod(SolutionMethod):
    def __init__(self, transition_matrix: np.ndarray,
                 initial_state: np.ndarray,
                 number_of_iterations: int = 10 ** 3,
                 tolerance: float = 10 ** -6):

        self.__transition_matrix = transition_matrix.T
        self.__initial_state = initial_state
        self.__number_of_iterations = number_of_iterations
        self.__tolerance = tolerance
        self.graph_data = np.array([])
        self.__stable_state_matrix = None
        self.__stable_transition_matrix = None

    def compute_stable_state_matrix(self) -> np.ndarray:
        iteration = 0
        current_state = self.__initial_state
        while iteration < self.__number_of_iterations:
            next_state = self.__transition_matrix @ current_state
            squared_error = np.std(next_state - current_state)
            self.graph_data = np.append(self.graph_data, squared_error)
            if squared_error < self.__tolerance:
                self.__stable_state_matrix = next_state
                return np.around(self.__stable_state_matrix, decimals=6)

            current_state = next_state
            iteration += 1

        raise Exception("The method did not converge in the given number of iterations")

    def compute_stable_transition_matrix(self) -> np.ndarray:
        self.__stable_transition_matrix = np.array([self.__stable_state_matrix] * self.__transition_matrix.shape[0])
        return np.around(self.__stable_transition_matrix, decimals=6)

    def get_graph_data(self) -> np.ndarray:
        return self.graph_data
