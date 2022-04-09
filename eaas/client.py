from __future__ import annotations

import json
from typing import Union

import requests

from eaas.config import Config
from eaas.endpoint import EndpointConfig

BATCH_SIZE = 100


class Client:
    def __init__(
        self, config: Config, endpoint_config: EndpointConfig = EndpointConfig()
    ):
        """A client wrapper"""
        self._config = config.to_dict()
        self._endpoint_config = endpoint_config

    def validate_metric(self, metric: Union[str, dict]):
        metric_name: str = metric if isinstance(metric, str) else metric["name"]
        # This could be made more rigorous for checking dictionaries too
        return metric_name in self._endpoint_config.valid_metrics

    def score(
        self,
        inputs: list[dict],
        metrics: list[Union[str, dict]],
        calculate: list[str] = None,
    ):
        """
        Takes a list of inputs and a list of metrics, and returns appropriate metric
        values.
        :param inputs: A list of input dictionaries, each containing
                       * source: a string indicating the source
                       * reference: a string or list of strings indicating reference
                         or references
                       * hypothesis: a string indicating the hypothesis
        :param metrics: A list of metrics to calculate, either as a string indicating
                        the metric, or a dictionary containing a "name" entry
                        indicating the metric, and other entries indicating the various
                        hyperparameters of the metric
        :param calculate: A list of what to calculate, including
                          * 'corpus': corpus-level scores
                          * 'sample': sample-level scores
                          * 'stat': sample-level sufficient statistics
        """

        calculate = calculate if calculate is not None else ["corpus", "sample"]

        # Sanity checks
        for metric in metrics:
            if not self.validate_metric(metric):
                raise ValueError(f"Invalid metric specification: {metric}")
        valid_calculate = {"corpus", "sample", "stats"}
        for calc in calculate:
            if calc not in valid_calculate:
                raise ValueError(
                    f"Invalid calculation item: {calc}."
                    f"Valid options include {valid_calculate}"
                )

        # Make the request
        data = {
            "inputs": inputs,
            "metrics": metrics,
            "calculate": calculate,
        }
        response = requests.post(
            url=self._endpoint_config.score_end_point,
            json=json.dumps(data),
        )

        # Check the request
        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(
                f"[Error on metric: {rjson['metric']}]\n"
                f"[Error Message]: {rjson['message']}"
            )
        return rjson
