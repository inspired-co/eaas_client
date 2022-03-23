.. _prompt:
Support for Prompts
=====================


Prompts can sometimes improve the performance for certain metrics (See `this paper <https://arxiv.org/abs/2106.11520>`__). In our :code:`client.score()` function, we support adding prompts to the source/hypothesis/references with both prefix position and suffix position. An example is shown below::

    from eaas import Config, Client
    config = Config()
    client = Client()
    client.load_config(config)

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
