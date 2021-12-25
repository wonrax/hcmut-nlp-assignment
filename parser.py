from unicodedata import normalize
import re

query = "Tàu hoả nào đến Đà Nẵng lúc 19:00HR ?"
query = "Tàu hỏa nào đến thành phố Hồ Chí Minh ? "
query = "Tàu hỏa nào đến Đà Nẵng ? "

query = normalize("NFC", query)

N = "NOUN"
V = "VERB"
PP = "PREPOSITION"  # e.g. lúc
TIME = "TIME"  # e.g. 19:00HR
Q = "QUERY"  # e.g. nào
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
    ROOT: ROOT,
}
"""
Part-of-Speech tagging dictionary.
"""

RIGHT_ARC = {
    N: {Q: "query", NAME: "nmod"},
    V: {N: "dobj", TIME: "time", PUNC: "punc"},
    Q: [],
    PP: [],
    TIME: [],
    NAME: [],
    ROOT: {V: "root"},
}
"""
Dictionary for RIGHT_ARC. Key is the buffer item type and value is the
compatible stack item type that we can draw a right-arc to.
"""

LEFT_ARC = {
    N: {V: "subj"},
    V: [],
    Q: [],
    PP: {TIME: "timemod"},
    TIME: [],
    NAME: [],
    ROOT: [],
}
"""
Dictionary for LEFT_ARC. Key is the buffer item type and value is the
compatible stack item type that we can draw a left-arc from.
"""


class Dependency:
    """
    Represents a dependency relation of the dependency parser.
    E.g. subj(đến, tàu_hoả) == đến -subj-> tàu_hoả
    """
    
    def __init__(self, relation: str, head: str, dependent: str):
        self.relation = relation    # e.g. subj
        self.head = head            # e.g. đến
        self.dependent = dependent  # e.g. tàu_hoả
    
    def __str__(self) -> str:
        return f"\"{self.head}\" --{self.relation}-> \"{self.dependent}\""


def malt_parse(tokens: "list[str]") -> "list[Dependency]":
    """
    Parse a sentence using MaltParser.
    Return a list of Dependency objects.
    """

    buffer = tokens.copy()
    stack = [ROOT]
    dependencies = []

    while True:
        if not buffer:
            break

        stack_item = stack[len(stack) - 1]
        next_buffer_item = buffer[0]

        stack_item_type = POS[stack_item]
        buffer_item_type = POS[next_buffer_item]
        
        dep = None


        # RIGHT_ARC
        if buffer_item_type in RIGHT_ARC[stack_item_type]:

            dep = Dependency(
                RIGHT_ARC[stack_item_type][buffer_item_type],
                stack_item,
                next_buffer_item)

            stack.append(buffer.pop(0))


        # LEFT_ARC
        elif buffer_item_type in LEFT_ARC[stack_item_type]:

            dep = Dependency(
                LEFT_ARC[stack_item_type][buffer_item_type],
                next_buffer_item,
                stack_item)

            stack.pop()


        # SHIFT
        elif stack_item_type in [V, ROOT]:
            stack.append(buffer.pop(0))


        # REDUCE
        else:
            stack.pop()


        if dep:
            dependencies.append(dep)

    return dependencies

class Relation:
    """
    Grammar relation of an dependency.
    """
    
    def __init__(self, relation: str, left: str, right: str):
        self.relation = relation    # e.g. AGENT
        self.left = left            # e.g. s1
        self.right = right  # e.g. đến
    
    def __str__(self) -> str:
        return f"({self.left} {self.relation} {self.right})"

def create_variable(name: str, existing_variables: "list[str]") -> str:
    """
    Create a variable.
    """
    letter = name[0]
    
    i = 0
    while True:
        i += 1
        var = f"{letter}{i}"
        if var not in existing_variables:
            return var

class SEM:
    """
    Semantic representation object.
    """
    
    def __init__(self, predicate: str, variable, relations):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations
    
    def __str__(self) -> str:
        return f"({self.predicate} {self.variable} {' '.join(map(str, self.relations)) if isinstance(self.relations, list) else self.relations})"

def create_sem(word, existing_variables):
    """
    Create a semantic representation from a sentence.
    """

    var = create_variable(word, existing_variables)

    if POS[word] not in [NAME]:
        return word, None

    sem = SEM(POS[word], var, word)

    return sem, var


def grammar_relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
    """
    Relationalize a list of Dependency objects.
    """

    relations = []
    variables = []

    for dep in dependencies:


        if dep.relation == "query":
            relations.append(Relation("QUERY", "s1", dep.head))

        elif dep.relation == "root":
            variables.append("s1")
            relations.append(Relation("PRED", "s1", dep.dependent))

        elif dep.relation == "subj":
            relations.append(Relation("AGENT", "s1", dep.dependent))

        elif dep.relation == "nmod":
            dependent_sem, dependent_var = create_sem(dep.dependent, variables)
            variables.append(dependent_var)
            relations.append(Relation("AMOD", dep.head, dependent_sem))

        elif dep.relation == "dobj":
            dependent_sem, dependent_var = create_sem(dep.dependent, variables)
            if dependent_var is not None:
                variables.append(dependent_var)
            relations.append(Relation("THEME", "s1", dependent_sem))

    return relations

def preprocess(text: str) -> "list[str]":
    """
    Remove unknown words and add time expressions to POS dictionary.
    Return a list of preprocessed tokens from the given text.
    """

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

context_deps = malt_parse(tokens)

[print(x) for x in context_deps]

print("------\n-------Grammar Relationalize-------------")
[print(x) for x in grammar_relationalize(context_deps)]


