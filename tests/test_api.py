# %%
import os
import unittest
from pathlib import Path

import jsonlines

from eaas import Client, Config

curr_dir = Path(__file__).parent


def read_jsonlines_to_list(file_name):
    lines = []
    with jsonlines.open(file_name, "r") as reader:
        for obj in reader:
            lines.append(obj)
    return lines


class TestMetrics(unittest.TestCase):
    def test_api(self):
        config = Config()
        client = Client(config)

        input_file = os.path.join(curr_dir, "inputs", "multi_references.jsonl")
        inputs = read_jsonlines_to_list(input_file)
        # res = client.score(inputs)
        res = client.score(inputs, metrics=["bleu", "rouge2"])
        print(res)

    def test_multilingual(self):
        config = Config()
        client = Client(config)

        for lang in ["en", "fr", "zh"]:
            # Single ref
            print(f"****** LANG: {lang} ******")
            print("For single reference")
            input_file = os.path.join(
                curr_dir, "inputs", f"{lang}_single_ref_tiny.jsonl"
            )
            inputs = read_jsonlines_to_list(input_file)
            # res = client.score(inputs, task="sum", metrics=None, lang=lang)
            res = client.score(inputs, metrics=["bleu", "rouge2"])
            print(res)

            # Multi ref
            if lang != "en":
                # Moverscore does not support languages other than English
                metrics = [
                    # "bart_score_cnn_hypo_ref",
                    # "bart_score_summ",
                    # "bart_score_mt",
                    # "bert_score_p",
                    # "bert_score_r",
                    # "bert_score_f",
                    "bleu",
                    # "chrf",
                    # "comet",
                    # "comet_qe",
                    # "prism",
                    # "prism_qe",
                    # "rouge1",
                    "rouge2",
                    # "rougeL"
                ]
            else:
                metrics = [
                    "bleu",
                    "rouge2",
                ]

            print("For multiple references")
            input_file = os.path.join(
                curr_dir, "inputs", f"{lang}_multi_ref_tiny.jsonl"
            )
            inputs = read_jsonlines_to_list(input_file)
            res = client.score(inputs, metrics=metrics)
            print(res)

    def test_main_example(self):
        client = Client(Config())

        inputs = [
            {
                "source": "Hello, my world",
                "references": ["Hello, world", "Hello my world"],
                "hypothesis": "Hi, my world",
            }
        ]
        metrics = ["rouge1", "bleu", "chrf"]

        score_list = client.score(inputs, metrics=metrics)
        print(score_list)
