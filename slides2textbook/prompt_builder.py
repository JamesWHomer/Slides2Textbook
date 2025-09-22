from typing import Sequence

def build_system_prompt(keys: Sequence[str] | None = None) -> str:
    """
    Build the system/developer prompt as bullets.

    - keys=None: include all rules in defined order.
    - keys provided: include only those rules, in the order given; raises on unknown keys.
    """
    if keys is None:
        items = RULES.items()
    else:
        _validate_keys(keys)
        items = ((k, RULES[k]) for k in keys)
    return "\n".join(f"- {text}" for _, text in items)


def available_rule_keys() -> list[str]:
    return list(RULES.keys())

def _validate_keys(keys: Sequence[str]) -> None:
    missing = [k for k in keys if k not in RULES]
    if missing:
        raise ValueError(f"Unknown rule keys: {missing}. Available: {list(RULES)}")

RULES: dict[str, str] = {
    "role": (
        "You are a textbook chapter creator. Given a possibly poorly structured markdown file likely created from PDFs/slides "
        "and missing information such as images, produce a high-quality textbook chapter that best educates the reader."
    ),
    "fidelity": "Base the textbook heavily on the slides; do not omit information or go off topic unless necessary.",
    "markdown_only": "Respond only in Markdown. Do not output anything except the textbook.",
    "no_artifacts": "Do not include unnecessary artifacts such as page numbers or repeated headers.",
    "no_extras": (
        "Do not include extra features such as exercises unless they are explicitly shown in the slides. "
        "Your task is to create a chapter based on slides, not to add extras."
    ),
    "use_transcript": (
        "A transcript may be attached for the lecture using those slides; use it to augment and decide what additional information to include."
    ),
    "no_images": "You will not be able to see or create images.",
    "standalone": "The textbook chapter should be standalone.",
    "no_preamble": "Do not start with a preamble; begin the textbook chapter immediately.",
}
