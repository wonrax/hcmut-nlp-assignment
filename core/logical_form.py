from core.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    """
    Logicalize a list of relations into logical form.
    """
    
    for relation in relations:
        if relation.type == "PRED":
            pass