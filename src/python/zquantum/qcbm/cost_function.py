from zquantum.core.cost_function import AnsatzBasedCostFunction
from zquantum.core.interfaces.backend import QuantumBackend
from zquantum.core.interfaces.ansatz import Ansatz
from zquantum.core.bitstring_distribution import (
    BitstringDistribution,
    evaluate_distribution_distance,
)
from zquantum.core.circuit import build_ansatz_circuit
from zquantum.core.utils import ValueEstimate
from typing import Union, Callable
import numpy as np


class QCBMCostFunction(AnsatzBasedCostFunction):
    """ Cost function used for evaluating QCBM.

    Args:
        ansatz (zquantum.core.interfaces.ansatz.Ansatz): the ansatz used to construct the variational circuits
        backend (zquantum.core.interfaces.backend.QuantumBackend): backend used for QCBM evaluation
        distance_measure (callable): function used to calculate the distance measure
        distance_measure_parameters (dict): dictionary containing the relevant parameters for the chosen distance measure
        target_bitstring_distribution (zquantum.core.bitstring_distribution.BitstringDistribution): bistring distribution which QCBM aims to learn
        save_evaluation_history (bool): flag indicating whether we want to store the history of all the evaluations.
        gradient_type (str): parameter indicating which type of gradient should be used.

    Params:
        ansatz zquantum.core.interfaces.ansatz.Ansatz): see Args
        backend (zquantum.core.interfaces.backend.QuantumBackend): see Args
        distance_measure (callable): see Args
        target_bitstring_distribution (zquantum.core.bitstring_distribution.BitstringDistribution): see Args
        save_evaluation_history (bool): see Args
        gradient_type (str): see Args
        evaluations_history (list): List of the tuples (parameters, value) representing all the evaluation in a chronological order.
    """

    def __init__(
        self,
        ansatz: Ansatz,
        backend: QuantumBackend,
        distance_measure: Callable,
        distance_measure_parameters: dict,
        target_bitstring_distribution: BitstringDistribution,
        save_evaluation_history: bool = True,
        gradient_type: str = "finite_difference",
    ):
        self.ansatz = ansatz
        self.backend = backend
        self.distance_measure = distance_measure
        self.distance_measure_parameters = distance_measure_parameters
        self.target_bitstring_distribution = target_bitstring_distribution
        self.evaluations_history = []
        self.save_evaluation_history = save_evaluation_history
        self.gradient_type = gradient_type

    def evaluate(self, parameters: np.ndarray) -> ValueEstimate:
        """
        Evaluates the value of the cost function for given parameters and saves the results (if specified).

        Args:
            parameters: parameters for which the evaluation should occur

        Returns:
            value: cost function value for given parameters, either int or float.
        """
        value, distribution = self._evaluate(parameters)
        if self.save_evaluation_history:
            self.evaluations_history.append(
                {
                    "value": value,
                    "params": parameters,
                    "bitstring_distribution": distribution.distribution_dict,
                }
            )
        return ValueEstimate(value)

    def _evaluate(self, parameters: np.ndarray) -> (float, BitstringDistribution):
        """
        Evaluates the value of the cost function for given parameters.

        Args:
            parameters: parameters for which the evaluation should occur.

        Returns:
            (float): cost function value for given parameters
            zquantum.core.bitstring_distribution.BitstringDistribution: distribution obtained
        """
        circuit = self.ansatz.get_executable_circuit(parameters)
        distribution = self.backend.get_bitstring_distribution(circuit)
        value = evaluate_distribution_distance(
            self.target_bitstring_distribution,
            distribution,
            self.distance_measure,
            distance_measure_parameters=self.distance_measure_parameters,
        )

        return value, distribution
