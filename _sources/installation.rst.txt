.. _installation:
Installation
============



To install EaaS, simply run::

   pip install eaas

To use the API, run the following as a simple example::

   from eaas import Client
   client = Client()

   # To use this API for scoring, you need to format your input as list of dictionary.
   # Each dictionary consists of `source` (string, optional), `references` (list of string, optional)
   # and `hypothesis` (string, required). `source` and `references` are optional based on the metrics
   # you want to use. Please do not conduct any preprocessing on `source`, `references` or `hypothesis`,
   # we expect normal-cased detokenized texts. All the preprocessing steps are taken by the metrics.
   # Below is a simple example.

   inputs = [{"source": "This is the source.",
              "references": ["This is the reference one.", "This is the reference two."],
              "hypothesis": "This is the generated hypothesis."}]
   metrics = ["bleu", "chrf"] # Can be None for simplicity if you consider using all metrics

   score_dic = client.score(inputs, metrics, lang="en")
   # `inputs` is a list of Dict, `metrics` is metric list, `lang` is the two-letter code for language

The output is like::

   {
     'bleu': [32.46679154750991],  # Sample-level scores. A list of scores one for each sample.
     'corpus_bleu': 32.46679154750991, # Corpus-level score.
     'chrf': [38.56890099861521],
     'corpus_chrf': 38.56890099861521
   }





