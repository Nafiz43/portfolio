"""Load the operator's private prompt; its contents never belong in Git."""
import hashlib
import os
from pathlib import Path

DEFAULT_PROMPT = Path(__file__).resolve().parent / ".private/assistant.txt"


def load_prompt():
    path = Path(os.getenv("PORTFOLIO_PROMPT_FILE", str(DEFAULT_PROMPT)))
    try:
        template = path.read_text(encoding="utf-8")
    except OSError as error:
        raise RuntimeError("Private assistant prompt is missing or unreadable. Configure PORTFOLIO_PROMPT_FILE.") from error
    if "{{context}}" not in template or "{{date}}" not in template:
        raise RuntimeError("Private assistant prompt must contain {{context}} and {{date}} placeholders.")
    return template, hashlib.sha256(template.encode()).hexdigest()
