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

BATCH_SIZE = 100


class Client:
    def __init__(self, config: Config):
        """A client wrapper"""
        self._record_end_point = "https://notebooksa.jarvislabs.ai/q-yr_VkZdJkNWZA1KFyHjP5HjPwgmaw3BXqXL8-9IU-truL4vpXUs31S2mIBaZXo/record"  # noqa
        self._score_end_point = "https://notebooksa.jarvislabs.ai/q-yr_VkZdJkNWZA1KFyHjP5HjPwgmaw3BXqXL8-9IU-truL4vpXUs31S2mIBaZXo/score"  # noqa
        self._valid_metrics = [
            "bart_score_cnn_hypo_ref",
            "bart_score_summ",
            "bart_score_mt",
            "bert_score_p",
            "bert_score_r",
            "bert_score_f",
            "bleu",
            "chrf",
            "comet",
            "comet_qe",
            "mover_score",
            "prism",
            "prism_qe",
            "rouge1",
            "rouge2",
            "rougeL",
        ]
        self._config = config.to_dict()

    @property
    def metrics(self):
        return self._valid_metrics

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

    # TODO: Beautify bleu, rouge1, rouge2, rougeL

    def bleu(
        self,
        refs: list[list[str]],
        hypos: list[str],
        task="sum",
        lang="en",
        cal_attributes=False,
        **prompt_info,
    ):
        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang
        inputs = []
        for ref_list, hypo in zip(refs, hypos):
            inputs.append({"source": "", "references": ref_list, "hypothesis": hypo})

        inputs = self.add_prompts(inputs, **prompt_info)
        metadata = self.log_request(inputs, ["bleu"])
        response = requests.post(url=self._record_end_point, json=json.dumps(metadata))
        if response.status_code != 200:
            raise RuntimeError("Internal server error.")
        print("EaaS: Your request has been sent.", file=sys.stderr)

        data = {
            "inputs": inputs,
            "metrics": ["bleu"],
            "config": self._config,
            "task": task,
            "cal_attributes": cal_attributes,
        }
        response = requests.post(
            url=self._score_end_point,
            json=json.dumps(data),
        )

        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(
                f"[Error on metric: {rjson['metric']}]\n"
                f"[Error Message]: {rjson['message']}"
            )

        final_score_dic: dict[str, float] = {}
        scores = rjson["scores"]
        assert len(scores["bleu"]) == len(inputs)
        final_score_dic["bleu"] = scores["bleu"]
        final_score_dic["corpus_bleu"] = scores["corpus_bleu"]
        for k, v in scores.items():
            if "attr" in k:
                final_score_dic[k] = v
                final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

        return scores

    def rouge(
        self,
        rouge_name,
        refs: list[list[str]],
        hypos: list[str],
        task="sum",
        lang="en",
        cal_attributes=False,
        **prompt_info,
    ):
        # Add the language property
        for k in self._config:
            self._config[k]["lang"] = lang
        inputs = []
        for ref_list, hypo in zip(refs, hypos):
            inputs.append({"source": "", "references": ref_list, "hypothesis": hypo})
        inputs = self.add_prompts(inputs, **prompt_info)
        metadata = self.log_request(inputs, [rouge_name])
        response = requests.post(url=self._record_end_point, json=json.dumps(metadata))
        if response.status_code != 200:
            raise RuntimeError("Internal server error.")
        print("EaaS: Your request has been sent.", file=sys.stderr)

        data = {
            "inputs": inputs,
            "metrics": [rouge_name],
            "config": self._config,
            "task": task,
            "cal_attributes": cal_attributes,
        }
        response = requests.post(
            url=self._score_end_point,
            json=json.dumps(data),
        )

        rjson = response.json()
        if response.status_code != 200:
            raise ConnectionError(
                f"[Error on metric: {rjson['metric']}]\n"
                f"[Error Message]: {rjson['message']}"
            )

        final_score_dic = {}
        scores = rjson["scores"]
        assert len(scores[rouge_name]) == len(inputs)
        final_score_dic[rouge_name] = scores[rouge_name]
        final_score_dic[f"corpus_{rouge_name}"] = scores[f"corpus_{rouge_name}"]
        for k, v in scores.items():
            if "attr" in k:
                final_score_dic[k] = v
                final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

        return scores

    def rouge1(
        self,
        refs: list[list[str]],
        hypos: list[str],
        task="sum",
        lang="en",
        cal_attributes=False,
        **prompt_info,
    ):
        return self.rouge(
            "rouge1", refs, hypos, task, lang, cal_attributes, **prompt_info
        )

    def rouge2(
        self,
        refs: list[list[str]],
        hypos: list[str],
        task="sum",
        lang="en",
        cal_attributes=False,
        **prompt_info,
    ):
        return self.rouge(
            "rouge2", refs, hypos, task, lang, cal_attributes, **prompt_info
        )

    def rougeL(
        self,
        refs: list[list[str]],
        hypos: list[str],
        task="sum",
        lang="en",
        cal_attributes=False,
        **prompt_info,
    ):
        return self.rouge(
            "rougeL", refs, hypos, task, lang, cal_attributes, **prompt_info
        )

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
            if metric not in self._valid_metrics:
                raise ValueError(
                    f"Your have entered invalid metric {metric}, please check."
                )

        # First record the request
        metadata = self.log_request(inputs, metrics)
        response = requests.post(url=self._record_end_point, json=json.dumps(metadata))
        if response.status_code != 200:
            raise RuntimeError("Internal server error.")
        print("EaaS: Your request has been sent.", file=sys.stderr)

        # Add prompts
        inputs = self.add_prompts(inputs, **prompt_info)
        inputs_len = len(inputs)

        final_score_dic: dict[str, float] = {}

        def attr_in_dic(_dic):
            _flag = False
            for _k in _dic:
                if "attr" in _k:
                    _flag = True
            return _flag

        # First deal with BLEU and CHRF
        if "bleu" in metrics:

            data = {
                "inputs": inputs,
                "metrics": ["bleu"],
                "config": self._config,
                "task": task,
                "cal_attributes": (not attr_in_dic(final_score_dic))
                if cal_attributes
                else False,
            }
            response = requests.post(
                url=self._score_end_point,
                json=json.dumps(data),
            )

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(
                    f"[Error on metric: {rjson['metric']}]\n"
                    f"[Error Message]: {rjson['message']}"
                )

            scores = rjson["scores"]
            assert len(scores["bleu"]) == inputs_len
            final_score_dic["bleu"] = scores["bleu"]
            final_score_dic["corpus_bleu"] = scores["corpus_bleu"]
            for k, v in scores.items():
                if "attr" in k:
                    final_score_dic[k] = v
                    final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

            metrics.remove("bleu")

        if "chrf" in metrics:
            data = {
                "inputs": inputs,
                "metrics": ["chrf"],
                "config": self._config,
                "task": task,
                "cal_attributes": (not attr_in_dic(final_score_dic))
                if cal_attributes
                else False,
            }
            response = requests.post(url=self._score_end_point, json=json.dumps(data))

            rjson = response.json()
            if response.status_code != 200:
                raise ConnectionError(
                    f"[Error on metric: {rjson['metric']}]\n"
                    f"[Error Message]: {rjson['message']}"
                )

            scores = rjson["scores"]
            assert len(scores["chrf"]) == inputs_len
            final_score_dic["chrf"] = scores["chrf"]
            final_score_dic["corpus_chrf"] = scores["corpus_chrf"]
            for k, v in scores.items():
                if "attr" in k:
                    final_score_dic[k] = v
                    final_score_dic[f"corpus_{k}"] = sum(v) / len(v)

            metrics.remove("chrf")

        # Deal with the inputs 100 samples at a time
        score_dic: defaultdict[str, list] = defaultdict(list)
        for i in trange(0, len(inputs), BATCH_SIZE, desc="Calculating scores."):
            data = {
                "inputs": inputs[i : i + BATCH_SIZE],
                "metrics": metrics,
                "config": self._config,
                "task": task,
                "cal_attributes": (not attr_in_dic(final_score_dic))
                if cal_attributes
                else False,
            }

            response = requests.post(url=self._score_end_point, json=json.dumps(data))

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
