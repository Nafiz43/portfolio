"""Deterministic boundary checks complement the model's private instructions."""
import re
import unicodedata

RULES = [
    ("instruction_override", r"\b(ignore|disregard|override|bypass|forget)\b.{0,100}\b(instructions?|rules?|guardrails?|system|prompts?)\b"),
    ("prompt_extraction", r"\b(system|developer|hidden|private|internal|initial)\s+(prompt|instructions?|messages?)\b"),
    ("prompt_extraction", r"\b(repeat|print|quote|reveal|show|dump|translate|encode)\b.{0,80}\b(instructions|configuration|secret|prompt)\b"),
    ("privileged_role", r"\b(you are now|act as|pretend to be)\b.{0,60}\b(unrestricted|administrator|system|developer|jailbroken)\b"),
    ("private_data", r"\b(home address|private phone|personal phone|passwords?|api keys?|access tokens?|other (users?|visitors?).{0,25}(messages?|chats?|transcripts?))\b"),
    ("filesystem_or_execution", r"\b(read|open|list|write|delete|execute|run|download)\b.{0,100}(/users/|/etc/|\.env\b|private files|shell|terminal|subprocess|os\.system)"),
]


def inspect_input(message):
    normalized = unicodedata.normalize("NFKC", message).casefold()
    normalized = re.sub(r"[\u200b-\u200f\ufeff]", "", normalized)
    for name, pattern in RULES:
        if re.search(pattern, normalized, re.S):
            return name
    return None


def refusal(reason):
    if reason == "private_data":
        return "I can share Nafiz’s public work, not private details or other visitors’ conversations. His research is much better conversation material anyway—want to explore a project or arrange a meeting?"
    return "I’m here to talk about Nafiz’s work, not reveal private instructions or operate his computer. Happy to take the scenic route through his research, though—AI for health or open-source software?"


def scope_redirect():
    return "That’s outside this portfolio’s neighborhood. My specialties are Nafiz’s research, projects, experience, and helping you find a time to talk. Want the quick tour?"


def ungrounded_response():
    return "I don’t have a reliable source for that in Nafiz’s portfolio, and I’d rather leave a blank than invent a plot twist. Try asking about a named project, publication, or role—or arrange a meeting with him."


def output_leaks_prompt(answer, template):
    # Detect long verbatim policy excerpts even if an input attack evades the rules.
    chunks = [line.strip() for line in template.splitlines() if len(line.strip()) >= 90 and "{{" not in line]
    return any(chunk.casefold() in answer.casefold() for chunk in chunks)


def unsupported_embellishment(answer):
    """Keep playful metaphors from introducing exaggerated capabilities."""
    return bool(re.search(
        r"\b(super[ -]smart|caffeine[ -]fueled|genius)\b|"
        r"\b(read|scan|understand|analy[sz]e)\w*\b.{0,65}\b(all|every)\b.{0,35}\b(code|files?|repositories|chat logs)\b",
        answer, re.I | re.S))
