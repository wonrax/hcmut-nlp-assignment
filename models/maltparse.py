from models.global_vars import *

ROOT = "ROOT"

RIGHT_ARC = {
    N: {Q: "query"},
    V: {TIME: "time", PUNC: "punc", NAME: "dobj", PP: "pp", YN: "yesno"},
    Q: [],
    PP: {NAME: "pmod"},
    TIME: [],
    NAME: [],
    ROOT: {V: "root"},
    DURATION: [],
    YN: [],
}
"""
Dictionary for RIGHT_ARC. Key is the buffer item type and value is the
compatible stack item type that we can draw a right-arc to.
"""

LEFT_ARC = {
    N: {V: "subj", NAME: "nmod"},
    V: {},
    Q: {N: "query"},
    PP: {TIME: "timemod"},
    TIME: [],
    NAME: {V: "subj"},
    ROOT: [],
    DURATION: {V: "duration"},
    YN: [],
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
    dependencies: "list[Dependency]" = []
    root_verb = None

    while True:
        if not buffer:
            break
        
        stack_item = stack[len(stack) - 1]
        buffer_item = buffer[0]

        stack_item_type = POS[stack_item] if stack_item is not ROOT \
                                            else stack_item
        buffer_item_type = POS[buffer_item]
        
        if buffer_item_type == V and root_verb is None:
            root_verb = buffer_item
        
        #TODO refactor this
        if isinstance(buffer_item_type, tuple):
            if root_verb is None:
                root_verb = buffer_item
                buffer_item_type = buffer_item_type[0]
            elif root_verb != buffer_item:
                buffer_item_type = buffer_item_type[1]
            else:
                buffer_item_type = buffer_item_type[0]
        if isinstance(stack_item_type, tuple):
            if root_verb == stack_item:
                stack_item_type = stack_item_type[0]
            else:
                stack_item_type = stack_item_type[1]

        dep = None


        # RIGHT_ARC
        if buffer_item_type in RIGHT_ARC[stack_item_type]:

            dep = Dependency(
                RIGHT_ARC[stack_item_type][buffer_item_type],
                stack_item,
                buffer_item)

            stack.append(buffer.pop(0))


        # LEFT_ARC
        elif buffer_item_type in LEFT_ARC[stack_item_type]:

            dep = Dependency(
                LEFT_ARC[stack_item_type][buffer_item_type],
                buffer_item,
                stack_item)

            stack.pop()


        # SHIFT
        elif stack_item_type in [V, ROOT, PP, DURATION]:
            if stack_item_type == PP and buffer_item_type in [YN, PUNC]:
                stack.pop()
            else:
                stack.append(buffer.pop(0))

        # REDUCE
        else:
            stack.pop()

        if dep:
            dependencies.append(dep)

    return dependencies

