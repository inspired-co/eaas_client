from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class EndpointConfig:
    record_end_point: str = "http://eaas.inspiredco.ai:4000/record"  # noqa
    score_end_point: str = "http://eaas.inspiredco.ai:4000/score"  # noqa
    valid_metrics: set[str] = field(
        default_factory=lambda: {
            "bart_score_en_ref",
            "bart_score_en_src",
            "bert_score_p",
            "bert_score_r",
            "bert_score_f",
            "bleu",
            "length",
            "length_ratio",
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
