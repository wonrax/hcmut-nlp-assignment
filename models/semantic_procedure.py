from models.grammar_relation import SEM

class Procedure:
    def __init__(self, name:str,  args: "list[str]"):
        self.name = name
        self.args = args
    
    def __str__(self):
        return f"({self.name} " \
            + f"{' '.join(map(str, self.args)) if isinstance(self.args, list) else self.args})"

MAP_WORD_TO_DATA_VAR = {
    "tàu_hoả": "TRAIN",
    "đến": "ATIME",
    "từ": "DTIME",
    "đà_nẵng": "DANANG",
    "huế": "HUE",
    "tp_hồ_chí_minh": "HCM",
    "hồ_chí_minh": "HCM",
    "nha_trang": "NTrang",
    "hà_nội": "HN",
    "thời_gian": "DURATION",
}

def proceduralize(sem: SEM) -> "list[Procedure]":
    subj = find_subj(sem)
    theme = find_theme(sem)
    
    src = find_src(sem)
    des = find_des(sem)

    procedures: "list[Procedure]" = []

    if sem.predicate == "WH-QUERY":

        if subj == "TRAIN" and theme is not None:
            time = find_time(sem)
            if not time:
                time = "?t"
            verb_type = find_verb_type(sem)
            

            if subj:
                procedures.append(Procedure(subj, ["?x"]))
            if theme:
                procedures.append(Procedure(verb_type, ["?x", theme, time]))
            return Procedure("PRINT-ALL", ["?x"] + procedures)
        
        if subj == "TRAIN":

            procedures.append(Procedure(subj, ["?x"]))
            if src:
                procedures.append(Procedure("DTIME", ["?x", src, "?t"]))
            if des:
                procedures.append(Procedure("ATIME", ["?x", des, "?t"]))

            return Procedure("PRINT-ALL", ["?x"] + procedures)

        if subj == "DURATION":
            procedures.append(Procedure("DURATION", ["?rt"]))
            
        
            rtprocedure = Procedure("RUN-TIME", [])

            train_id = find_train(sem)
            if train_id:
                rtprocedure.args.append(train_id.upper())
            else:
                rtprocedure.args.append("?x")

            if src:
                rtprocedure.args.append(src)
            if des:
                rtprocedure.args.append(des)
            rtprocedure.args.append("?rt")
            
            procedures.append(rtprocedure)

            return Procedure("PRINT-ALL", ["?rt"] + procedures)

    if sem.predicate == "YESNO":

        train_id = find_train(sem)
        if train_id:
            train_id = train_id.upper()

        if not train_id:
            train_id = "?x"

        procedures.append(Procedure("TRAIN", [train_id]))

        if src:
            procedures.append(Procedure("DTIME", [train_id, src, "?t"]))
        if des:
            procedures.append(Procedure("ATIME", [train_id, des, "?t"]))
        
        return Procedure("EXISTS", ["?y"] + procedures)


def find_subj(sem):
    which_subj = find_sem_given_predicate(sem, "WHICH")
    if which_subj and which_subj.relations:
        if isinstance(which_subj.relations[0], SEM):
            return MAP_WORD_TO_DATA_VAR[which_subj.relations[0].relations[0]]
        return MAP_WORD_TO_DATA_VAR[which_subj.relations[0]]

def find_theme(sem):
    theme = find_sem_given_predicate(sem, "THEME")
    if theme and theme.relations:
        return MAP_WORD_TO_DATA_VAR[theme.relations[0].relations[0]]

def find_time(sem):
    theme = find_sem_given_predicate(sem, "AT-TIME")
    if theme and theme.relations:
        return theme.relations[0].upper()

def find_verb_type(sem):
    wh = find_sem_given_predicate(sem, "WH-QUERY")
    if wh and wh.relations:
        return MAP_WORD_TO_DATA_VAR[wh.relations[0].predicate]

def find_src(sem):
    src = find_sem_given_predicate(sem, "FROM-LOC")
    if src and src.relations:
        return MAP_WORD_TO_DATA_VAR[src.relations[0]]

def find_des(sem):
    src = find_sem_given_predicate(sem, "TO-LOC")
    if src and src.relations:
        return MAP_WORD_TO_DATA_VAR[src.relations[0]]

def find_train(sem):
    train = find_sem_given_predicate(sem, "TRAIN")
    if train and train.relations:
        return train.relations[0]

def find_sem_given_predicate(sem: SEM, predicate: str) -> SEM:
    if sem.predicate == predicate:
        return sem
    else:
        found = None
        for relation in sem.relations:
            if not isinstance(relation, str):
                found = find_sem_given_predicate(relation, predicate)
            if found:
                return found