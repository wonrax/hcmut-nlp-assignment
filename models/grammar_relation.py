from models.global_vars import *
from models.maltparse import Dependency

class Relation:
    """
    Grammar relation of an dependency.
    """
    
    def __init__(self, type: str, left: str, right: str):
        self.type = type    # e.g. AGENT
        self.left = left            # e.g. s1
        self.right = right  # e.g. đến
    
    def __str__(self) -> str:
        return f"({self.left} {self.type} {self.right})"

class SEM:
    """
    Semantic representation object.
    """
    
    def __init__(self, predicate: str, variable, relations=None):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations if relations else []
    
    def __str__(self) -> str:
        return f"({self.predicate} {self.variable}" \
                + f"{' ' + ' '.join(map(str, self.relations)) if self.relations else ''})"

def create_sem(word, existing_variables):
    """
    Create a semantic representation from a sentence.
    """

    var = create_variable(word, existing_variables)

    if POS[word] not in [NAME]:
        return word, None

    sem = SEM(POS[word], var, [word])

    return sem, var

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

def relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
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
            relations.append(Relation("TRAIN", "s1", dep.dependent))

        elif dep.relation == "nmod":
            # dependent_sem, dependent_var = create_sem(dep.dependent, variables)
            # variables.append(dependent_var)
            # relations.append(Relation("NMOD", dep.head, dependent_sem))
            pass

        elif dep.relation == "dobj":
            dependent_sem, dependent_var = create_sem(dep.dependent, variables)
            if dependent_var is not None:
                variables.append(dependent_var)
            relations.append(Relation("THEME", "s1", dependent_sem))

        elif dep.relation == "time":
            relations.append(Relation("AT-TIME", "s1", dep.dependent))
        
        elif dep.relation == "pmod" and dep.head == "từ":
            relations.append(Relation("SRC", "s1", dep.dependent))

        elif dep.relation == "pmod" and dep.head == "đến":
            relations.append(Relation("DES", "s1", dep.dependent))

        elif dep.relation == "duration":
            relations.append(Relation("DURATION", "s1", dep.dependent))

        elif dep.relation == "yesno":
            relations.append(Relation("YESNO", "s1", dep.dependent))

    return relations

