import numpy as np

from abc import ABC, abstractmethod


class SolutionMethod(ABC):
    """Represents a solution method for a Markov chain"""

    @abstractmethod
    def compute_stable_state_matrix(self) -> np.ndarray:
        """Computes the stable state matrix of the Markov chain"""

    @abstractmethod
    def compute_stable_transition_matrix(self) -> np.ndarray:
        """Computes the stable transition matrix of the Markov chain"""

    @abstractmethod
    def get_graph_data(self) -> np.ndarray:
        """Returns the data used to draw the graph of standard deviation of the state matrix"""
