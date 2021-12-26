from models.global_vars import *
import re
from unicodedata import normalize

def preprocess(text: str) -> "list[str]":
    """
    Remove unknown words and add time expressions to POS dictionary.
    Return a list of preprocessed tokens from the given text.
    """

    text = normalize("NFC", text)
    
    # Remove redundant whitespaces
    text = re.sub(r"\s{2,}", " ", text)

    # Add space before question mark
    text = re.sub(r"(.)\?", r"\1 ?", text)

    text = text.lower()

    for token in TOKENIZE_DICT:
        # text = text.replace(token, TOKENIZE_DICT[token])
        text = re.sub(token, TOKENIZE_DICT[token], text)
    
    time_tokens = re.findall(r"\d+:\d+hr", text)
    for token in time_tokens:
        if token in POS:
            continue
        POS[token] = TIME

    tokens = text.split(" ")

    for token in tokens:
        if token not in POS:
            tokens = list(filter(lambda x: x != token, tokens))
    
    return tokens
