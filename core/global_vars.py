from collections import OrderedDict

N = "NOUN"
V = "VERB"
PP = "PREPOSITION"  # e.g. lúc
TIME = "TIME"  # e.g. 19:00HR
Q = "QUERY"  # e.g. nào
NAME = "NAME"  # e.g. HUẾ
PUNC = "PUNC"  # e.g. ?, .
DURATION = "DURATION"  # e.g. thời gian
YN = "YESNO"

TOKENIZE_DICT = OrderedDict({
    "tàu hoả": "tàu_hoả",
    "tàu hỏa": "tàu_hoả",
    "thời gian": "thời_gian",
    "thành phố": "thành_phố",
    "đà nẵng": "đà_nẵng",
    "tp. hồ chí minh": "tp_hồ_chí_minh",
    "hồ chí minh": "hồ_chí_minh",
    "nha trang": "nha_trang",
    "hà nội": "hà_nội",
})
"""
Maps compound words to a single token.
"""

POS = {
    "tàu_hoả": N,
    "thời_gian": DURATION,
    "đến": (V, PP),
    "từ": PP,
    "chạy": V,
    "nào": Q,
    "mấy": Q,
    "giờ": N,
    "thành_phố": N,
    "huế": NAME,
    "đà_nẵng": NAME,
    "tp_hồ_chí_minh": NAME,
    "hồ_chí_minh": NAME,
    "hà_nội": NAME,
    "nha_trang": NAME,
    "lúc": PP,
    "?": PUNC,
    "không": YN,
    "b1": NAME,
    "b2": NAME,
    "b3": NAME,
    "b4": NAME,
    "b5": NAME,
    "b6": NAME,
}
"""
Part-of-Speech tagging dictionary.
"""
