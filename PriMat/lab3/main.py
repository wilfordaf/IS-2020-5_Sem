import numpy as np
import matplotlib.pyplot as plt

from lab3.model_solution_methods.AnalyticalSolutionMethod import AnalyticalSolutionMethod
from lab3.model_solution_methods.NumericalSolutionMethod import NumericalSolutionMethod


def test_analytical_solution_method():
    transition_matrix = np.array([
        [0.3, 0.6, 0.1],
        [0.0, 1.0, 0.0],
        [0.6, 0.2, 0.2]
    ])

    analytical_solution = AnalyticalSolutionMethod(transition_matrix)
    stable_state_matrix = analytical_solution.compute_stable_state_matrix()
    stable_transition_matrix = analytical_solution.compute_stable_transition_matrix()
    print(stable_state_matrix)
    print(stable_transition_matrix)


def test_numerical_solution_method():
    transition_matrix = np.array([
        [0.3, 0.6, 0.1],
        [0.0, 1.0, 0.0],
        [0.6, 0.2, 0.2]
    ])

    initial_state = np.array([0.2, 0.3, 0.5])
    numerical_solution = NumericalSolutionMethod(transition_matrix, initial_state)
    stable_state_matrix = numerical_solution.compute_stable_state_matrix()
    stable_transition_matrix = numerical_solution.compute_stable_transition_matrix()
    print(stable_state_matrix)
    print(stable_transition_matrix)


def test_methods_comparison():
    transition_matrix_size = 8
    tolerance = 10 ** -6
    number_of_iterations = 10 ** 3

    transition_matrix = np.random.rand(transition_matrix_size, transition_matrix_size)
    transition_matrix /= transition_matrix.sum(axis=1, keepdims=True)

    initial_state_1 = np.random.random(transition_matrix_size)
    initial_state_1 /= np.sum(initial_state_1)

    initial_state_2 = np.random.random(transition_matrix_size)
    initial_state_2 /= np.sum(initial_state_2)

    print("Statement:")
    print("The transition matrix is:")
    print(transition_matrix)
    print("The initial states are:")
    print(initial_state_1)
    print(initial_state_2)

    analytical_solution = AnalyticalSolutionMethod(transition_matrix)
    numerical_solution_1 = NumericalSolutionMethod(transition_matrix,
                                                   initial_state_1,
                                                   number_of_iterations,
                                                   tolerance)

    numerical_solution_2 = NumericalSolutionMethod(transition_matrix,
                                                   initial_state_2,
                                                   number_of_iterations,
                                                   tolerance)

    analytical_stable_state_matrix = analytical_solution.compute_stable_state_matrix()
    analytical_stable_transition_matrix = analytical_solution.compute_stable_transition_matrix()

    numerical_stable_state_matrix_1 = numerical_solution_1.compute_stable_state_matrix()
    numerical_stable_transition_matrix_1 = numerical_solution_1.compute_stable_transition_matrix()

    numerical_stable_state_matrix_2 = numerical_solution_2.compute_stable_state_matrix()
    numerical_stable_transition_matrix_2 = numerical_solution_2.compute_stable_transition_matrix()

    print("Analytical solution:")
    print("The stable state matrix is:")
    print(analytical_stable_state_matrix)
    # print("The stable transition matrix is:")
    # print(analytical_stable_transition_matrix)

    print("Numerical solution 1:")
    print("The stable state matrix is:")
    print(numerical_stable_state_matrix_1)
    # print("The stable transition matrix is:")
    # print(numerical_stable_transition_matrix_1)

    print("Numerical solution 2:")
    print("The stable state matrix is:")
    print(numerical_stable_state_matrix_2)
    # print("The stable transition matrix is:")
    # print(numerical_stable_transition_matrix_2)

    print("Checking if found stable state matrices are equal to analytical solution:")
    print(f"First: {np.allclose(analytical_stable_state_matrix, numerical_stable_state_matrix_1, atol=tolerance)}")
    print(f"Second: {np.allclose(analytical_stable_state_matrix, numerical_stable_state_matrix_2, atol=tolerance)}")

    plt.xlabel("Iteration")
    plt.ylabel("Standard deviation")
    plt.legend(["Solution 1", "Solution 2"])
    plt.plot(numerical_solution_1.get_graph_data())
    plt.plot(numerical_solution_2.get_graph_data())
    plt.show()


if __name__ == '__main__':
    # test_analytical_solution_method()
    # test_numerical_solution_method()
    test_methods_comparison()
