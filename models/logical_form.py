from models.grammar_relation import Relation, SEM

def logicalize(relations: "list[Relation]") -> SEM:
    """
    Logicalize a list of relations into logical form.
    """
    mapping: "dict[str, Relation]" = {}
    for relation in relations:
        mapping[relation.type] = relation

    sem = None
    time_sem = None
    agent_sem = None

    # TIME SEM
    if "QUERY" in mapping:
        if mapping["QUERY"].right == "tàu_hoả":
            time = mapping["AT-TIME"] if "AT-TIME" in mapping else None
            time_sem = SEM("AT-TIME", "", [time.right]) if time else None
            agent = mapping["TRAIN"]
            agent_sem = SEM("TRAIN","", [SEM("WHICH", "", [agent.right])])
        elif mapping["QUERY"].right == "giờ":
            if "DURATION" not in mapping:
                time = mapping["AT-TIME"] if "AT-TIME" in mapping else None
                time_sem = SEM("AT-TIME", "", [time.right]) if time else None
            else:
                time = mapping["DURATION"] if "DURATION" in mapping else None
                time_sem = SEM("WHICH", "", [SEM("DURATION", "", [time.right])]) if time else None
            agent = mapping["TRAIN"]
            agent_sem = SEM("TRAIN","", [agent.right])


    if "QUERY" in mapping:
        pred = mapping["PRED"]
        if "THEME" in mapping:

            theme = mapping["THEME"]
            theme_sem = SEM("THEME", "", [theme.right])

            pred_sem_relations = list(filter(None.__ne__,
                                    [agent_sem, theme_sem, time_sem]))
            pred_sem = SEM(pred.right, pred.left, pred_sem_relations)

            sem = SEM("WH-QUERY", "", [pred_sem])

        elif "SRC" in mapping or "DES" in mapping:
            src_sem = None
            des_sem = None
            if "SRC" in mapping:
                src_sem = SEM("FROM-LOC", "", [mapping["SRC"].right])
            if "DES" in mapping:
                des_sem = SEM("TO-LOC", "", [mapping["DES"].right])

            pred_sem_relations = list(filter(None.__ne__,
                                    [agent_sem, src_sem, des_sem, time_sem]))
            pred_sem = SEM(pred.right, pred.left, pred_sem_relations)

            sem = SEM("WH-QUERY", "", [pred_sem])

    if "YESNO" in mapping:

        pred = mapping["PRED"]

        agent = mapping["TRAIN"]
        agent_sem = SEM("TRAIN", "", [agent.right])
        
        src_sem = None
        des_sem = None

        if "SRC" in mapping:
            src_sem = SEM("FROM-LOC", "", [mapping["SRC"].right])
        if "DES" in mapping:
            des_sem = SEM("TO-LOC", "", [mapping["DES"].right])

        pred_sem_relations = list(filter(None.__ne__,
                                [agent_sem, src_sem, des_sem]))
        pred_sem = SEM(pred.right, pred.left, pred_sem_relations)
        sem = SEM("YESNO", "", [pred_sem])

    
    return sem
