# %%
from eaas import Client, Config
import jsonlines
from pathlib import Path
import os
import unittest

curr_dir = Path(__file__).parent


def read_jsonlines_to_list(file_name):
    lines = []
    with jsonlines.open(file_name, 'r') as reader:
        for obj in reader:
            lines.append(obj)
    return lines


class TestMetrics(unittest.TestCase):
    def test_api(self):
        client = Client()
        config = Config()
        client.load_config(config)

        input_file = os.path.join(curr_dir, "inputs", "multi_references.jsonl")
        inputs = read_jsonlines_to_list(input_file)
        # res = client.score(inputs)
        res = client.score(inputs, metrics=["bleu", "rouge2"])
        print(res)

    def test_multilingual(self):
        client = Client()
        config = Config()
        client.load_config(config)

        for lang in ["en", "fr", "zh"]:
            # Single ref
            print(f"****** LANG: {lang} ******")
            print("For single reference")
            input_file = os.path.join(curr_dir, "inputs", f"{lang}_single_ref_tiny.jsonl")
            inputs = read_jsonlines_to_list(input_file)
            # res = client.score(inputs, task="sum", metrics=None, lang=lang)
            res = client.score(inputs, task="sum", metrics=["bleu", "rouge2"], lang=lang)
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
                metrics = None

            print(f"For multiple references")
            input_file = os.path.join(curr_dir, "inputs", f"{lang}_multi_ref_tiny.jsonl")
            inputs = read_jsonlines_to_list(input_file)
            res = client.score(inputs, task="sum", metrics=metrics, lang=lang)
            print(res)
