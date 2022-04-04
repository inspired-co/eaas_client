from __future__ import annotations

import copy
import json
import sys
from collections import defaultdict
from time import gmtime, strftime
from typing import Union

import requests
from tqdm import trange

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

    @property
    def metrics(self):
        return self._endpoint_config.valid_metrics

    @staticmethod
    def word_count(word_list):
        """count words in a list (or list of list)"""
        c = 0
        for x_ in word_list:
            if isinstance(x_, list):
                c += Client.word_count(x_)
            else:
                c += len(x_.split(" "))
        return c

    def log_request(self, inputs, metrics):
        """Log the metadata of this request."""

        srcs = [x["source"] for x in inputs]
        refs = [x["references"] for x in inputs]
        hypos = [x["hypothesis"] for x in inputs]

        srcs_wc = Client.word_count(srcs)
        refs_wc = Client.word_count(refs)
        hypos_wc = Client.word_count(hypos)

        return {
            "date:": strftime("%Y-%m-%d %H:%M:%S", gmtime()),
            "user": "placeholder",
            "metrics": metrics,
            "src_tokens": srcs_wc,
            "refs_tokens": refs_wc,
            "hypos_tokens": hypos_wc,
        }

    def add_prompts(self, raw_inputs: list[dict], **prompt_info):
        inputs = copy.deepcopy(raw_inputs)
        if prompt_info:
            prompt_source = prompt_info["source"] if "source" in prompt_info else None
            prompt_reference = (
                prompt_info["reference"] if "reference" in prompt_info else None
            )
            prompt_hypothesis = (
                prompt_info["hypothesis"] if "hypothesis" in prompt_info else None
            )
            if prompt_source:
                prompt_source_prefix = (
                    prompt_source["prefix"] if "prefix" in prompt_source else ""
                )
                prompt_source_suffix = (
                    prompt_source["suffix"] if "suffix" in prompt_source else ""
                )
                for i in range(len(inputs)):
                    inputs[i]["source"] = (
                        prompt_source_prefix
                        + " "
                        + inputs[i]["source"]
                        + " "
                        + prompt_source_suffix
                    )

            if prompt_reference:
                prompt_reference_prefix = (
                    prompt_reference["prefix"] if "prefix" in prompt_reference else ""
                )
                prompt_reference_suffix = (
                    prompt_reference["suffix"] if "suffix" in prompt_reference else ""
                )
                for i in range(len(inputs)):
                    for j in range(len(inputs[0]["references"])):
                        inputs[i]["references"][j] = (
                            prompt_reference_prefix
                            + " "
                            + inputs[i]["references"][j]
                            + " "
                            + prompt_reference_suffix
                        )

            if prompt_hypothesis:
                prompt_hypothesis_prefix = (
                    prompt_hypothesis["prefix"] if "prefix" in prompt_hypothesis else ""
                )
                prompt_hypothesis_suffix = (
                    prompt_hypothesis["suffix"] if "suffix" in prompt_hypothesis else ""
                )
                for i in range(len(inputs)):
                    inputs[i]["hypothesis"] = (
                        prompt_hypothesis_prefix
                        + " "
                        + inputs[i]["hypothesis"]
                        + " "
                        + prompt_hypothesis_suffix
                    )
        return inputs

    def score(
        self,
        inputs: list[dict],
        metrics: list[str],
        task="sum",
        lang="en",
        cal_attributes=False,
        **prompt_info,
    ):

        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang

        for metric in metrics:
            if metric not in self._endpoint_config.valid_metrics:
                raise ValueError(
                    f"Your have entered invalid metric {metric}, please check."
                )

        # First record the request
        metadata = self.log_request(inputs, metrics)
        response = requests.post(
            url=self._endpoint_config.record_end_point, json=json.dumps(metadata)
        )
        if response.status_code != 200:
            raise RuntimeError("Internal server error.")
        print("EaaS: Your request has been sent.", file=sys.stderr)

        # Add prompts
        inputs = self.add_prompts(inputs, **prompt_info)
        inputs_len = len(inputs)

        final_score_dic: dict[str, float] = {}

        # First deal with BLEU and CHRF
        for my_metric in [x for x in ("bleu", "chrf") if x in metrics]:

            my_cal = cal_attributes and any(["attr" in x for x in final_score_dic])
            data = {
                "inputs": inputs,
                "metrics": [my_metric],
                "config": self._config,
                "task": task,
                "cal_attributes": my_cal,
            }
            response = requests.post(
                url=self._endpoint_config.score_end_point,
                json=json.dumps(data),
            )

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(
                    f"[Error on metric: {rjson['metric']}]\n"
                    f"[Error Message]: {rjson['message']}"
                )

            scores = rjson["scores"]
            assert len(scores[my_metric]) == inputs_len
            final_score_dic[my_metric] = scores[my_metric]
            final_score_dic[f"corpus_{my_metric}"] = scores[f"corpus_{my_metric}"]
            for k, v in scores.items():
                if "attr" in k:
                    final_score_dic[k] = v
                    final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

        # Deal with the inputs 100 samples at a time
        score_dic: defaultdict[str, list] = defaultdict(list)
        for i in trange(0, len(inputs), BATCH_SIZE, desc="Calculating scores."):
            my_cal = cal_attributes and any(["attr" in x for x in final_score_dic])
            data = {
                "inputs": inputs[i : i + BATCH_SIZE],
                "metrics": metrics,
                "config": self._config,
                "task": task,
                "cal_attributes": my_cal,
            }

            response = requests.post(
                url=self._endpoint_config.score_end_point, json=json.dumps(data)
            )

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(
                    f"[Error on metric: {rjson['metric']}]\n"
                    f"[Error Message]: {rjson['message']}"
                )

            scores = rjson["scores"]

            for k, v in scores.items():
                if "corpus" in k:
                    continue
                score_dic[k] += v

        # Aggregate scores and get corpus-level scores for some metrics
        for k, v in score_dic.items():
            assert len(v) == inputs_len
            final_score_dic[k] = v
            final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

        # Reformat the returned dict
        sample_level: list[dict] = []
        for i in range(len(inputs)):
            sample_level.append({})
        corpus_level = {}
        reformatted_final_score_dic: dict[str, Union[dict, list]] = {}
        for k, v in final_score_dic.items():
            if "corpus" in k:
                corpus_level[k] = v
            else:
                for i in range(len(inputs)):
                    sample_level[i][k] = v[i]

        reformatted_final_score_dic["sample_level"] = sample_level
        reformatted_final_score_dic["corpus_level"] = corpus_level

        return reformatted_final_score_dic

    def signature(self):
        pass
