# %%
class BaseConfig:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def set_property(self, k, v):
        assert hasattr(self, k)
        setattr(self, k, v)

    def get_propety(self, k):
        assert hasattr(self, k)
        return getattr(self, k)

    def to_dict(self):
        return self.__dict__


class Config:
    def __init__(self):
        self.bart_score_summ = BaseConfig()
        self.bart_score_mt = BaseConfig()
        self.bart_score_cnn_hypo_ref = BaseConfig()
        self.bert_score_p = BaseConfig(**{"idf": False, "rescale_with_baseline": False})
        self.bert_score_r = BaseConfig(**{"idf": False, "rescale_with_baseline": False})
        self.bert_score_f = BaseConfig(**{"idf": False, "rescale_with_baseline": False})
        self.bleu = BaseConfig(**{
            "smooth_method": "exp",
            "smooth_value": None,
            "force": False,
            "lowercase": False,
            "use_effective_order": False}
                               )
        self.chrf = BaseConfig(**{
            "char_order": 6,
            "word_order": 0,
            "beta": 2,
            "lowercase": False,
            "remove_whitespace": True,
            "eps_smoothing": False
        })
        self.comet = BaseConfig()
        self.comet_qe = BaseConfig()
        self.mover_score = BaseConfig(**{
            "remove_stopwords": True,
            "n_gram": 1,
            "remove_subwords": True,
            "idf": False
        })
        self.prism = BaseConfig(**{"temperature": 1.0})
        self.prism_qe = BaseConfig(**{"temperature": 1.0})
        self.rouge1 = BaseConfig()
        self.rouge2 = BaseConfig()
        self.rougeL = BaseConfig()

    def metrics(self):
        return self.__dict__.keys()

    def to_dict(self):
        dic = {}
        for k, v in self.__dict__.items():
            dic[k] = v.to_dict()
        return dic
