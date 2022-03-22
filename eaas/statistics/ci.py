# %%
class ConfidenceInterval:
    """ This is for calculating confidence interval for general metrics.
        Some special metrics like BLEU should not use this.
    """
    @staticmethod
    def __call__(**kwargs):
        """ Feel free to change the signature. """
        raise NotImplementedError
