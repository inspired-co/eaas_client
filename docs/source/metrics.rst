.. _metrics:
Supported Metrics
=====================

The two-letter code or three-letter code for each language can be found here: https://www.science.co.il/language/Codes.php. We support the following metrics:


* :code:`bart_score_cnn_hypo_ref`: `BARTScore <https://arxiv.org/abs/2106.11520>`__ is a sequence to sequence framework based on pre-trained language model BART. :code:`bart_score_cnn_hypo_ref` uses the CNNDM finetuned BART. It calculates the average generation score of :code:`Score(hypothesis|reference)` and :code:`Score(reference|hypothesis)`.
* :code:`bart_score_summ`: `BARTScore <https://arxiv.org/abs/2106.11520>`__ using the CNNDM finetuned BART. It calculates :code:`Score(hypothesis|source)`.
* :code:`bart_score_mt`: `BARTScore <https://arxiv.org/abs/2106.11520>`__ using the Parabank2 finetuned BART. It calculates the average generation score of :code:`Score(hypothesis|reference)` and :code:`Score(reference|hypothesis)`.
* :code:`bert_score_p`: `BERTScore <https://arxiv.org/abs/1904.09675>`__ is a metric designed for evaluating translated text using BERT-based matching framework. :code:`bert_score_p` calculates the BERTScore precision.
* :code:`bert_score_r`: `BERTScore <https://arxiv.org/abs/1904.09675>`__ recall.
* :code:`bert_score_f`: `BERTScore <https://arxiv.org/abs/1904.09675>`__ f score.
* :code:`bleu`: `BLEU <https://aclanthology.org/P02-1040.pdf>`__ measures modified ngram matches between each candidate translation and the reference translations.
* :code:`chrf`: `CHRF <https://aclanthology.org/W15-3049/>`__ measures the character-level ngram matches between hypothesis and reference.
* :code:`comet`: `COMET <https://aclanthology.org/2020.emnlp-main.213/>`__ is a neural framework for training multilingual machine translation evaluation models. :code:`comet` uses the :code:`wmt20-comet-da` checkpoint which utilizes source, hypothesis and reference.
* :code:`comet_qe`: `COMET <https://aclanthology.org/2020.emnlp-main.213/>`__ for quality estimation. :code:`comet_qe` uses the :code:`wmt20-comet-qe-da` checkpoint which utilizes only source and hypothesis.
* :code:`mover_score`: `MoverScore <https://arxiv.org/abs/1909.02622>`__ is a metric similar to BERTScore. Different from BERTScore, it uses the Earth Mover’s Distance instead of the Euclidean Distance.
* :code:`prism`: `PRISM <https://arxiv.org/abs/2004.14564>`__ is a sequence to sequence framework trained from scratch. :code:`prism` calculates the average generation score of :code:`Score(hypothesis|reference)` and :code:`Score(reference|hypothesis)`.
* :code:`prism_qe`: `PRISM <https://arxiv.org/abs/2004.14564>`__ for quality estimation. It calculates :code:`Score(hypothesis| source)`.
* :code:`rouge1`: `ROUGE-1 <https://aclanthology.org/W04-1013/>`__ refers to the overlap of unigram (each word) between the system and reference summaries.
* :code:`rouge2`: `ROUGE-2 <https://aclanthology.org/W04-1013/>`__ refers to the overlap of bigrams between the system and reference summaries.
* :code:`rougeL`: `ROUGE-2 <https://aclanthology.org/W04-1013/>`__ refers to the longest common subsequence between the system and reference summaries.



******************************
BARTScore
******************************
.. important::
    Reference: `BARTScore: Evaluating Generated Text as Text Generation <https://arxiv.org/abs/2106.11520>`__

* Supported Language:

Arabic (ar),
Czech (cs),
German (de),
English (en),
Spanish (es),
Estonian (et),
Finnish (fi),
French (fr),
Gujarati (gu),
Hindi (hi),
Italian (it),
Japanese (ja),
Kazakh (kk),
Korean (ko),
Lithuanian (lt),
Latvian (lv),
Burmese (my),
Nepali (ne),
Dutch (nl),
Romanian (ro),
Russian (ru),
Sinhala (si),
Turkish (tr),
Vietnamese (vi),
Chinese (zh),
Afrikaans (af),
Azerbaijani (az),
Bengali (bn),
Persian (fa),
Hebrew (he),
Croatian (hr),
Indonesian (id),
Georgian (ka),
Khmer (km),
Macedonian (mk),
Malayalam (ml),
Mongolian (mn),
Marathi (mr),
Polish (pl),
Pashto (ps),
Portuguese (pt),
Swedish (sv),
Swahili (sw),
Tamil (ta),
Telugu (te),
Thai (th),
Tagalog (tl),
Ukrainian (uk),
Urdu (ur),
Xhosa (xh),
Galician (gl),
Slovene (sl)


******************************
BERTScore
******************************
.. important::
    Reference: `BERTScore: Evaluating Text Generation with BERT <https://arxiv.org/abs/1904.09675>`__


* Supported Language:
Afrikaans,
Albanian,
Arabic,
Aragonese,
Armenian,
Asturian,
Azerbaijani,
Bashkir,
Basque,
Bavarian,
Belarusian,
Bengali,
Bishnupriya Manipuri,
Bosnian,
Breton,
Bulgarian,
Burmese,
Catalan,
Cebuano,
Chechen,
Chinese (Simplified),
Chinese (Traditional),
Chuvash,
Croatian,
Czech,
Danish,
Dutch,
English,
Estonian,
Finnish,
French,
Galician,
Georgian,
German,
Greek,
Gujarati,
Haitian,
Hebrew,
Hindi,
Hungarian,
Icelandic,
Ido,
Indonesian,
Irish,
Italian,
Japanese,
Javanese,
Kannada,
Kazakh,
Kirghiz,
Korean,
Latin,
Latvian,
Lithuanian,
Lombard,
Low Saxon,
Luxembourgish,
Macedonian,
Malagasy,
Malay,
Malayalam,
Marathi,
Minangkabau,
Nepali,
Newar,
Norwegian (Bokmal),
Norwegian (Nynorsk),
Occitan,
Persian (Farsi),
Piedmontese,
Polish,
Portuguese,
Punjabi,
Romanian,
Russian,
Scots,
Serbian,
Serbo-Croatian,
Sicilian,
Slovak,
Slovenian,
South Azerbaijani,
Spanish,
Sundanese,
Swahili,
Swedish,
Tagalog,
Tajik,
Tamil,
Tatar,
Telugu,
Turkish,
Ukrainian,
Urdu,
Uzbek,
Vietnamese,
Volapük,
Waray-Waray,
Welsh,
West Frisian,
Western Punjabi,
Yoruba

******************************
BLEU
******************************
.. important::
    Reference: `BLEU: a Method for Automatic Evaluation of Machine Translation <https://aclanthology.org/P02-1040.pdf>`__

* Supported Languages: All


******************************
CHRF
******************************
.. important::
    Reference: `chrF: character n-gram F-score for automatic MT evaluation <https://aclanthology.org/W15-3049/>`__

* Supported Languages: All

******************************
COMET
******************************
.. important::
    Reference: `COMET: A Neural Framework for MT Evaluation <https://aclanthology.org/2020.emnlp-main.213/>`__

* Supported Languages: Afrikaans, Albanian, Amharic, Arabic, Armenian, Assamese, Azerbaijani, Basque, Belarusian, Bengali, Bengali Romanized, Bosnian, Breton, Bulgarian, Burmese, Burmese, Catalan, Chinese (Simplified), Chinese (Traditional), Croatian, Czech, Danish, Dutch, English, Esperanto, Estonian, Filipino, Finnish, French, Galician, Georgian, German, Greek, Gujarati, Hausa, Hebrew, Hindi, Hindi Romanized, Hungarian, Icelandic, Indonesian, Irish, Italian, Japanese, Javanese, Kannada, Kazakh, Khmer, Korean, Kurdish (Kurmanji), Kyrgyz, Lao, Latin, Latvian, Lithuanian, Macedonian, Malagasy, Malay, Malayalam, Marathi, Mongolian, Nepali, Norwegian, Oriya, Oromo, Pashto, Persian, Polish, Portuguese, Punjabi, Romanian, Russian, Sanskri, Scottish, Gaelic, Serbian, Sindhi, Sinhala, Slovak, Slovenian, Somali, Spanish, Sundanese, Swahili, Swedish, Tamil, Tamil Romanized, Telugu, Telugu Romanized, Thai, Turkish, Ukrainian, Urdu, Urdu Romanized, Uyghur, Uzbek, Vietnamese, Welsh, Western, Frisian, Xhosa, Yiddish.

******************************
MoverScore
******************************
.. important::
    Reference: `MoverScore: Text Generation Evaluating with Contextualized Embeddings and Earth Mover Distance <https://arxiv.org/abs/1909.02622>`__

* Supported Languages: English

******************************
PRISM
******************************
.. important::
    Reference: `Automatic Machine Translation Evaluation in Many Languages via Zero-Shot Paraphrasing <https://arxiv.org/abs/2004.14564>`__

* Supported Languages: Albanian, Arabic, Bengali, Bulgarian, Catalan; Valencian, Chinese, Croatian, Czech, Danish, Dutch, English, Esperanto, Estonian, Finnish, French, German, Greek, Modern, Hebrew (modern), Hungarian, Indonesian, Italian, Japanese, Kazakh, Latvian, Lithuanian, Macedonian, Norwegian, Polish, Portuguese, Romanian, Moldavan, Russian, Serbian, Slovak, Slovene, Spanish; Castilian, Swedish, Turkish, Ukrainian, Vietnamese

******************************
ROUGE
******************************
.. important::
    Reference: `ROUGE: A Package for Automatic Evaluation of Summaries <https://aclanthology.org/W04-1013/>`__

* Supported Languages:
Bengali (bn),
Hindi (hi),
Turkish (tr),
Arabic (ar),
Danish (da),
Dutch (nl),
English (en),
Finnish (fi),
French (fr),
German (de),
Hungarian (hu),
Italian (it),
Norwegian (nb),
Portuguese (pt),
Romanian (ro),
Russian (ru),
Spanish (es),
Swedish (sv)
Chinese (zh)
Thai (th),
Japanese (ja)

