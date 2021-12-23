from unicodedata import normalize
import re

# from utils.normalize_unicode import convert_unicode as normalize
query = "Tàu hoả nào đến Đà Nẵng lúc 19:00HR ?"
query = "Tàu hỏa nào đến thành phố Hồ Chí Minh ? "

query = normalize("NFC", query)

N = "NOUN"
V = "VERB"
PP = "PREPOSITION"  # e.g. lúc
TIME = "TIME"  # e.g. 19:00HR
QUERY = "QUERY"  # e.g. nào
NAME = "NAME"  # e.g. HUẾ
PUNC = "PUNC"  # e.g. ?, .

ROOT = "ROOT"

TOKENIZE_DICT = {
    "tàu hoả": "tàu_hoả",
    "tàu hỏa": "tàu_hoả",
    "thành phố": "thành_phố",
    "đà nẵng": "đà_nẵng",
    "tp. hồ chí minh": "tp_hồ_chí_minh",
    "hồ chí minh": "hồ_chí_minh",
    "nha trang": "nha_trang",
    "hà nội": "hà_nội",
}

POS = {
    "tàu_hoả": N,
    "đến": V,
    "nào": QUERY,
    "thành_phố": N,
    "huế": NAME,
    "đà_nẵng": NAME,
    "hồ_chí_minh": NAME,
    "lúc": PP,
    "?": PUNC,
    ROOT: ROOT,
}

RIGHT_ARC = {
    N: {QUERY: "query", NAME: "nmod"},
    V: {N: "dobj", TIME: "time", PUNC: "punc"},
    QUERY: [],
    PP: [],
    TIME: [],
    NAME: [],
    ROOT: {V: "root"},
}

LEFT_ARC = {
    N: {V: "subj"},
    V: [],
    QUERY: [],
    PP: {TIME: "timemod"},
    TIME: [],
    NAME: [],
    ROOT: [],
}


class Dependency:
    """
    Represents a dependency relation of the dependency parser.
    E.g. subj(đến, tàu_hoả) == đến -subj-> tàu_hoả
    """
    
    def __init__(self, relation, head, dependent):
        self.relation = relation    # e.g. subj
        self.head = head            # e.g. đến
        self.dependent = dependent  # e.g. tàu_hoả
    
    def __str__(self) -> str:
        return f"\"{self.head}\" --{self.relation}-> \"{self.dependent}\""


def malt_parse(tokens):
    buffer = tokens
    stack = [ROOT]
    dependencies = []

    while True:
        if not buffer:
            break

        last_stack_item = stack[len(stack) - 1]
        next_buffer_item = buffer[0]

        last_stack_item_type = POS[last_stack_item]
        next_buffer_item_type = POS[next_buffer_item]
        
        dep = None

        if next_buffer_item_type in RIGHT_ARC[last_stack_item_type]:
            dep = Dependency(RIGHT_ARC[last_stack_item_type][next_buffer_item_type], last_stack_item, next_buffer_item)
            stack.append(buffer.pop(0))

        elif next_buffer_item_type in LEFT_ARC[last_stack_item_type]:
            dep = Dependency(LEFT_ARC[last_stack_item_type][next_buffer_item_type], next_buffer_item, last_stack_item)
            stack.pop()

        # SHIFT
        elif last_stack_item_type in [V, ROOT]:
            stack.append(buffer.pop(0))

        # REDUCE
        else:
            stack.pop()
        
        if dep:
            dependencies.append(dep)

    return dependencies

def preprocess(text: str):

    text = text.lower()

    for token in TOKENIZE_DICT:
        text = text.replace(token, TOKENIZE_DICT[token])
    
    time_tokens = re.findall(r"\d\d:\d\dhr", text)
    for token in time_tokens:
        if token in POS:
            continue
        POS[token] = TIME

    tokens = text.split(" ")

    for token in tokens:
        if token not in POS:
            tokens.remove(token)
    
    return tokens

tokens = preprocess(query)
print(tokens)

[print(x) for x in malt_parse(tokens)]
