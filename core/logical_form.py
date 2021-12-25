from core.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    """
    Logicalize a list of relations into logical form.
    """
    mapping: "dict[str, Relation]" = {}
    for relation in relations:
        mapping[relation.type] = relation

    sem = None


    if "QUERY" in mapping:
        pred = mapping["PRED"]
        agent = mapping["AGENT"]
        theme = mapping["THEME"]
        time = mapping["AT-TIME"]
        agent_sem = SEM("AGENT","", [SEM("WHICH", "", [agent.right])])
        theme_sem = SEM("THEME", "", [theme.right])
        time_sem = SEM("AT-TIME", "", [time.right])

        pred_sem_relations = list(filter(None.__ne__,
                                [agent_sem, theme_sem, time_sem]))
        pred_sem = SEM(pred.right, pred.left, pred_sem_relations)

        sem = SEM("WH-QUERY", "", [pred_sem])

    print(sem)
    
    return sem
