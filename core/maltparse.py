from core.global_vars import *

ROOT = "ROOT"

RIGHT_ARC = {
    N: {Q: "query", NAME: "nmod"},
    V: {N: "dobj", TIME: "time", PUNC: "punc", NAME: "dobj"},
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

        stack_item_type = POS[stack_item] if stack_item is not ROOT \
                                            else stack_item
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

