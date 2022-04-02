# %%
import os
import unittest
from pathlib import Path

import jsonlines

from eaas import Config
from eaas.async_client import AsyncClient

curr_dir = Path(__file__).parent


def read_jsonlines_to_list(file_name):
    lines = []
    with jsonlines.open(file_name, "r") as reader:
        for obj in reader:
            lines.append(obj)
    return lines


class TestAsync(unittest.TestCase):
    def test_async_requests(self):
        config = Config()
        client = AsyncClient(config)

        input_file = os.path.join(curr_dir, "inputs", "multi_references.jsonl")
        inputs = read_jsonlines_to_list(input_file)
        req1 = client.async_score(inputs, metrics=["bleu"])
        req2 = client.async_score(inputs, metrics=["rouge1", "rouge2"])
        result1 = req1.get_result()
        result2 = req2.get_result()
        self.assertTrue("corpus_bleu" in result1["corpus_level"])
        self.assertTrue("corpus_rouge1" not in result1["corpus_level"])
        self.assertTrue("corpus_rouge2" not in result1["corpus_level"])
        self.assertTrue("corpus_bleu" not in result2["corpus_level"])
        self.assertTrue("corpus_rouge1" in result2["corpus_level"])
        self.assertTrue("corpus_rouge2" in result2["corpus_level"])
