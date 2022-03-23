.. _attributes:
Supported Attributes
=====================


The :code:`task` option in the :code:`client.score()` function decides what attributes we calculate. Currently, we only support attributes for summarization task (:code:`task=sum`). The following attributes (reference: `this paper <https://arxiv.org/pdf/2010.05139.pdf>`__) will be calculated if :code:`cal_attributes` is set to :code:`True` in :code:`client.score()`. They are all reference-free.


* :code:`source_len`: measures the length of the source text.
* :code:`hypothesis_len`: measures the length of the hypothesis text.
* :code:`density & coverage`: measures to what extent a summary covers the content in the source text.
* :code:`compression`: measures the compression ratio from the source text to the generated summary.
* :code:`repetition`: measures the rate of repeated segments in summaries. The segments are instantiated as trigrams.
* :code:`novelty`: measures the proportion of segments in the summaries that haven’t appeared in source documents. The segments are instantiated as bigrams.
* :code:`copy_len`: measures the average length of segments in summary copied from source document.