import sys
import string
import argparse

from eaas.client import Client
import jsonlines


def read_jsonlines_to_list(file_name):
    lines = []
    with jsonlines.open(file_name, 'r') as reader:
        for obj in reader:
            lines.append(obj)
    return lines


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluation-as-a-Service for NLP')

    parser.add_argument('--path_inputs', type=str, required=True,
                        help="Input texts to be evaluated")
    parser.add_argument('--metrics', type=str, required=True,
                        help="Metrics to be used, separated by commas")
    parser.add_argument("--task", type=str, default="sum",
                        help="The task of interest, can be sum/mt.")
    parser.add_argument("--lang", type=str, default="en",
                        help="Language of hypotheses")
    args = parser.parse_args()

    path_inputs = args.path_inputs
    metrics = args.metrics.rstrip(" ")

    print(path_inputs)

    inputs = read_jsonlines_to_list(path_inputs)
    metrics_list = [metric for metric in metrics.split(",")]

    client = Client()
    score_dic = client.score(inputs, metrics_list, args.lang)
    print(score_dic)

"""
python eaas_cli.py --path_inputs ../tests/inputs/multi_references.jsonl --metrics bleu,chrf --lang en
"""
