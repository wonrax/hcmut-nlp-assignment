N = "NOUN"
V = "VERB"
PP = "PREPOSITION"  # e.g. lúc
TIME = "TIME"  # e.g. 19:00HR
Q = "QUERY"  # e.g. nào
NAME = "NAME"  # e.g. HUẾ
PUNC = "PUNC"  # e.g. ?, .

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
"""
Maps compound words to a single token.
"""

POS = {
    "tàu_hoả": N,
    "đến": V,
    "nào": Q,
    "thành_phố": N,
    "huế": NAME,
    "đà_nẵng": NAME,
    "hồ_chí_minh": NAME,
    "lúc": PP,
    "?": PUNC,
}
"""
Part-of-Speech tagging dictionary.
"""
