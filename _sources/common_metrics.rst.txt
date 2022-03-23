.. _common_metrics:
Support for Common Metrics
=====================


We support quick calculation for BLEU and ROUGE(1,2,L), see the following for usage::

    from eaas import Config, Client
    config = Config()
    client = Client()
    client.load_config(config)

    # Note that the input format is different from the score function.
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
