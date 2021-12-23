query = "Tàu_hoả nào đến thành_phố Huế lúc 19:00HR ?"

N = "NOUN"
V = "VERB"
PP = "PREPOSITION"  # e.g. lúc
TIME = "TIME"  # e.g. 19:00HR
QUERY = "QUERY"  # e.g. nào
NAME = "NAME"  # e.g. HUẾ
PUNC = "PUNC"  # e.g. ?, .

ROOT = "ROOT"

POS = {
    "tàu_hoả": N,
    "đến": V,
    "nào": QUERY,
    "thành_phố": N,
    "huế": NAME,
    "lúc": PP,
    "19:00hr": TIME,
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
        return f"{self.dependent} -{self.relation}-> {self.head}"


def malt_parse(string):
    buffer = query.lower().split(" ")
    stack = [ROOT]
    dependencies = []

    while True:
        if not buffer:
            break

        last_stack_item = stack[len(stack) - 1]
        next_buffer_item = buffer[0]

        last_stack_item_type = POS[last_stack_item]
        next_buffer_item_type = POS[next_buffer_item]

        # dep = ""

        if next_buffer_item_type in RIGHT_ARC[last_stack_item_type]:
            # dep = f"{RIGHT_ARC[last_stack_item_type][next_buffer_item_type]}({last_stack_item}, {next_buffer_item})"
            dep = Dependency(RIGHT_ARC[last_stack_item_type][next_buffer_item_type], last_stack_item, next_buffer_item)
            dependencies.append(dep)
            stack.append(buffer.pop(0))

        elif next_buffer_item_type in LEFT_ARC[last_stack_item_type]:
            # dep = f"{LEFT_ARC[last_stack_item_type][next_buffer_item_type]}({next_buffer_item}, {last_stack_item})"
            dep = Dependency(LEFT_ARC[last_stack_item_type][next_buffer_item_type], next_buffer_item, last_stack_item)
            dependencies.append(dep)
            stack.pop()

        elif last_stack_item_type in [V, ROOT]:
            # SHIFT
            stack.append(buffer.pop(0))
        else:
            # REDUCE
            stack.pop()

        # print("dep", dep)

    return dependencies


[print(x) for x in malt_parse(query)]
