# src/pii/masker.py
import regex as re

PHONE = re.compile(r"\b\+?\d[\d\s\-]{7,}\b")
EMAIL = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")

def mask_pii(text):
    mapping = {}

    def mask(pattern, key_prefix, text):
        def repl(m):
            val = m.group(0)
            key = f"<{key_prefix}_{len(mapping)+1}>"
            mapping[key] = val
            return key
        return pattern.sub(repl, text)

    masked = mask(PHONE, "PHONE", text)
    masked = mask(EMAIL, "EMAIL", masked)
    return masked, mapping

def unmask(text, mapping):
    for k, v in mapping.items():
        text = text.replace(k, v)
    return text
