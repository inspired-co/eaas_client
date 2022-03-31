# Default configurations for metrics

Here are our default configurations for each metric. `None` means there are no parameters in the metric.

* bart_score_cnn_hypo_ref: None
* bart_score_summ: None
* bart_score_mt: None
* bert_score_p: For a given language, BERTScore chooses the model and layer based on empirical results, see [here](https://github.com/Tiiiger/bert_score/blob/master/bert_score/utils.py). By default, we do not use the IDF, and we do not rescale with baseline.
* bert_score_r: Same as `bert_score_p`
* bert_score_f: Same as `bert_score_p`
* bleu: By default, we use exponential decay for smoothing method.
* chrf: By default, we set character n-gram order to be 6 and word n-gram order to be 0. We do not nclude whitespaces when extracting character n-grams. Besides, we use effective order smoothing by default.
* comet: None
* comet_qe: None
* mover_score: By default, we remove stopwords, and subwords. We do not apply IDF and use the unigram-based MoverScore. 
* prism: By default, we set the temperature to be 1.0.
* prism_qe: Same as `prism`
* rouge1: None
* rouge2: None
* rougeL: None
