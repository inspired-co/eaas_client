from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EndpointConfig:
    record_end_point: str = "https://notebooksa.jarvislabs.ai/q-yr_VkZdJkNWZA1KFyHjP5HjPwgmaw3BXqXL8-9IU-truL4vpXUs31S2mIBaZXo/record"  # noqa
    score_end_point: str = "https://notebooksa.jarvislabs.ai/q-yr_VkZdJkNWZA1KFyHjP5HjPwgmaw3BXqXL8-9IU-truL4vpXUs31S2mIBaZXo/score"  # noqa
    valid_metrics: set[str] = field(
        default_factory=lambda: {
            "bart_score_cnn_hypo_ref",
            "bart_score_summ",
            "bart_score_mt",
            "bert_score_p",
            "bert_score_r",
            "bert_score_f",
            "bleu",
            "chrf",
            "comet",
            "comet_qe",
            "mover_score",
            "prism",
            "prism_qe",
            "rouge1",
            "rouge2",
            "rougeL",
        }
    )
