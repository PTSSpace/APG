def lowerize(txt: str) -> str:
    return txt[:1].lower() + txt[1:] if txt else ""
