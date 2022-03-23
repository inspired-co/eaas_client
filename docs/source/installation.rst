.. _installation:
Installation
============



To install EaaS, simply run::

   pip install eaas

To use the API, You should go through the following two steps.


* **Step 1**: You should load the default configurations and make modifications if needed::

    from eaas import Config
    config = Config()

    # To see the metrics we support, run
    print(config.metrics())

    # To see the default configuration of a metric, run
    print(config.bleu.to_dict())

    # Here is an example of modifying the default config.
    config.bleu.set_property("smooth_method", "floor")
    print(config.bleu.to_dict())

* **Step 2**: Initialize the client and send your inputs. Please send your inputs as a whole (a list of many dicts) instead of sending one sample at a time (which will be much slower)::

    from eaas import Client
    client = Client()
    client.load_config(config)  # The config you have created above

    # To use this API for scoring, you need to format your input as list of dictionary.
    # Each dictionary consists of `source` (string, optional), `references` (list of string, optional) and `hypothesis` (string, required). `source` and `references` are optional based on the metrics you want to use.
    # Please do not conduct any preprocessing on `source`, `references` or `hypothesis`.
    # We expect normal-cased detokenized texts. All the preprocessing steps are taken by the metrics.
    # Below is a simple example.

    inputs = [{"source": "This is the source.",
               "references": ["This is the reference one.", "This is the reference two."],
               "hypothesis": "This is the generated hypothesis."}]
    metrics = ["bleu", "chrf"] # Can be None for simplicity if you consider using all metrics

    score_dic = client.score(inputs, task="sum", metrics=metrics, lang="en", cal_attributes=True)
    # inputs is a list of Dict, task is the name of task (for calculating attributes), metrics is metric list, lang is the two-letter code language.
    # You can also set cal_attributes=False to save some time since some attribute calculations can be slow.

The output is like::

    # sample_level is a list of dict, corpus_level is a dict
    {
        'sample_level': [
            {
                'bleu': 32.46679154750991,
                'attr_compression': 0.8333333333333334,
                'attr_copy_len': 2.0,
                'attr_coverage': 0.6666666666666666,
                'attr_density': 1.6666666666666667,
                'attr_hypothesis_len': 6,
                'attr_novelty': 0.6,
                'attr_repetition': 0.0,
                'attr_source_len': 5,
                'chrf': 38.56890099861521
            }
        ],
        'corpus_level': {
            'corpus_bleu': 32.46679154750991,
            'corpus_attr_compression': 0.8333333333333334,
            'corpus_attr_copy_len': 2.0,
            'corpus_attr_coverage': 0.6666666666666666,
            'corpus_attr_density': 1.6666666666666667,
            'corpus_attr_hypothesis_len': 6.0,
            'corpus_attr_novelty': 0.6,
            'corpus_attr_repetition': 0.0,
            'corpus_attr_source_len': 5.0,
            'corpus_chrf': 38.56890099861521
        }
    }
