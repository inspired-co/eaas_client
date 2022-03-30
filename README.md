# Evaluation-as-a-Service for NLP
<p align="center">
    <br>
    <img src="docs/Resources/figs/logo.png" width="400"/>
    <br>
  <a href="https://github.com/ExpressAI/eaas_client/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/expressai/DataLab" /></a>
  <a href="https://github.com/expressai/eaas_client/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/expressai/eaas_client" /></a>
  <a href="https://pypi.org/project//"><img alt="PyPI" src="https://img.shields.io/pypi/v/eaas" /></a>
  <a href=".github/workflows/ci.yml"><img alt="Integration Tests", src="https://github.com/expressai/eaas_client/actions/workflows/ci.yml/badge.svg?event=push" /></a>
</p>


## Usage
Before using EaaS, please see the [terms of use](TERMS.md).
Detailed documentation can be found [here](https://expressai.github.io/autoeval/). To install the EaaS, simply run
```bash
pip install eaas
```


## Run your "Hello, world"
A minimal EaaS application looks someting like this:
```python
from eaas import Config, Client

client = Client(Config())

inputs = [{
    "source":"Hello, my world", 
    "references":["Hello, world"], 
    "hypothesis":"Hi, my world"
    }]
score_dic = client.score(inputs, metrics=metrics) 



```

If `eaas` has been installed successfully, you should get the results below by printing `score_dic`:

 
```python
{
    'sample_level': [
        {'rouge1': 0.4}
        ],
    'corpus_level': {'corpus_rouge1': 0.4}
}
```
 



Notably: 
* To use this API for scoring, you need to format your input as list of dictionary. 
* Each dictionary consists of `source` (string, optional), `references` (list of string, optional) and `hypothesis` (string, required). `source` and `references` are optional based on the metrics you want to use. 
* Please do not conduct any preprocessing on `source`, `references` or `hypothesis`. 
* We expect normal-cased detokenized texts. All the preprocessing steps are taken by the metrics. 
* There are other parameters that can be set in the `score` function:  `task` is the name of task (for calculating attributes), `metrics` is metric list, `lang` is the two-letter code language, `cal_attributes` is an indicator that decides whether to calculate some task-dependent attributes.
* You can also set `cal_attributes=False` to save some time since some attribute calculations can be slow.



 
## Supported Metrics
Currently, EaaS supports the following metrics:
* `bart_score_cnn_hypo_ref`: [BARTScore](https://arxiv.org/abs/2106.11520) is a sequence to sequence framework based on pre-trained language model BART.  `bart_score_cnn_hypo_ref` uses the CNNDM finetuned BART. It calculates the average generation score of `Score(hypothesis|reference)` and `Score(reference|hypothesis)`.
* `bart_score_summ`: [BARTScore](https://arxiv.org/abs/2106.11520) using the CNNDM finetuned BART. It calculates `Score(hypothesis|source)`.
* `bart_score_mt`: [BARTScore](https://arxiv.org/abs/2106.11520) using the Parabank2 finetuned BART. It calculates the average generation score of `Score(hypothesis|reference)` and `Score(reference|hypothesis)`.
* `bert_score_p`: [BERTScore](https://arxiv.org/abs/1904.09675) is a metric designed for evaluating translated text using BERT-based matching framework. `bert_score_p` calculates the BERTScore precision.
* `bert_score_r`: [BERTScore](https://arxiv.org/abs/1904.09675) recall.
* `bert_score_f`: [BERTScore](https://arxiv.org/abs/1904.09675) f score.
* `bleu`: [BLEU](https://aclanthology.org/P02-1040.pdf) measures modified ngram matches between each candidate translation and the reference translations. 
* `chrf`: [CHRF](https://aclanthology.org/W15-3049/) measures the character-level ngram matches between hypothesis and reference.
* `comet`: [COMET](https://aclanthology.org/2020.emnlp-main.213/) is a neural framework for training multilingual machine translation evaluation models. `comet` uses the `wmt20-comet-da` checkpoint which utilizes source, hypothesis and reference.
* `comet_qe`: [COMET](https://aclanthology.org/2020.emnlp-main.213/) for quality estimation. `comet_qe` uses the `wmt20-comet-qe-da` checkpoint which utilizes only source and hypothesis.
* `mover_score`: [MoverScore](https://arxiv.org/abs/1909.02622) is a metric similar to BERTScore. Different from BERTScore, it uses the Earth Mover’s Distance instead of the Euclidean Distance.
* `prism`: [PRISM](https://arxiv.org/abs/2004.14564) is a sequence to sequence framework trained from scratch. `prism` calculates the average generation score of `Score(hypothesis|reference)` and `Score(reference|hypothesis)`.
* `prism_qe`: [PRISM](https://arxiv.org/abs/2004.14564) for quality estimation. It calculates `Score(hypothesis| source)`.
* `rouge1`: [ROUGE-1](https://aclanthology.org/W04-1013/) refers to the overlap of unigram (each word) between the system and reference summaries.
* `rouge2`: [ROUGE-2](https://aclanthology.org/W04-1013/) refers to the overlap of bigrams between the system and reference summaries.
* `rougeL`: [ROUGE-L](https://aclanthology.org/W04-1013/) refers to the longest common subsequence between the system and reference summaries.

## Support for Attributes
The `task` option in the `client.score()` function decides what attributes we calculate. Currently, we only support attributes for summarization task (`task=sum`). The following attributes (reference: [this paper](https://arxiv.org/pdf/2010.05139.pdf)) will be calculated if `cal_attributes` is set to `True` in `client.score()`. They are all reference-free.
* `source_len`: measures the length of the source text.
* `hypothesis_len`: measures the length of the hypothesis text.
* `density & coverage`: measures to what extent a summary covers the content in the source text.
* `compression`: measures the compression ratio from the source text to the generated summary.
* `repetition`: measures the rate of repeated segments in summaries. The segments are instantiated as trigrams.
* `novelty`: measures the proportion of segments in the summaries that haven’t appeared in source documents. The segments are instantiated as bigrams.
* `copy_len`: measures the average length of segments in summary copied from source document.


### Example

```python
from eaas import Config, Client

client = Client(Config())

inputs = [{"source": "This is the source.", 
           "references": ["This is the reference one.", "This is the reference two."],
           "hypothesis": "This is the generated hypothesis."}]
metrics = ["bleu", "chrf"] # Can be None for simplicity if you consider using all metrics

score_dic = client.score(inputs, task="sum", metrics=metrics, lang="en", cal_attributes=True) 
# inputs is a list of Dict, task is the name of task (for calculating attributes), metrics is metric list, lang is the two-letter code language.
# You can also set cal_attributes=False to save some time since some attribute calculations can be slow.
```





## Support for Common Metrics
We support quick calculation for BLEU and ROUGE(1,2,L), see the following for usage.
```python
from eaas import Config, Client

client = Client(Config())


# Note that the input format is different from the `score` function. 
references = [["This is the reference one for sample one.", "This is the reference two for sample one."],
              ["This is the reference one for sample two.", "This is the reference two for sample two."]]
hypothesis = ["This is the generated hypothesis for sample one.", 
              "This is the generated hypothesis for sample two."]

# Calculate BLEU
client.bleu(references, hypothesis, task="sum", lang="en", cal_attributes=False)

# Calculate ROUGEs
client.rouge1(references, hypothesis, task="sum", lang="en", cal_attributes=False)
client.rouge2(references, hypothesis, task="sum", lang="en", cal_attributes=False)
client.rougeL(references, hypothesis, task="sum", lang="en", cal_attributes=False)
```

The output is like
```
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
```



## Support for Prompts
Prompts can sometimes improve the performance for certain metrics (See [this paper](https://arxiv.org/abs/2106.11520)). In our `client.score()` function, we support adding prompts to the source/hypothesis/references with both prefix position and suffix position. An example is shown below.

```python
from eaas import Config, Client

client = Client(Config())



inputs = [
    {
        "source": "This is the source.",
        "references": ["This is the reference one.", "This is two."],
        "hypothesis": "This is the generated hypothesis."
    }
]

prompt_info = {
    "source": {"prefix": "This is source prefix", "suffix": "This is source suffix"},
    "hypothesis": {"prefix": "This is hypothesis prefix", "suffix": "This is hypothesis suffix"},
    "reference": {"prefix": "This is reference prefix", "suffix": "This is reference suffix"}
}

# adding this prompt info will automatically turn the inputs into
# [{'source': 'This is source prefix This is the source. This is source suffix', 
#   'references': ['This is reference prefix This is the reference one. This is reference suffix', 'This is reference prefix This is two. This is reference suffix'], 
#   'hypothesis': 'This is hypothesis prefix This is the generated hypothesis. This is hypothesis suffix'}]

# Here is a simpler example.
# prompt_info = {"source": {"prefix": "This is prefix"}}

score_dic = client.score(inputs, task="sum", metrics=["bart_score_summ"], lang="en", cal_attributes=False, **prompt_info)

``` 
