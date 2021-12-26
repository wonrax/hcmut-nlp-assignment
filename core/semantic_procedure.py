from core.grammar_relation import SEM

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
    "đà_nẵng": "DANANG"
}

def proceduralize(sem: SEM) -> "list[Procedure]":
    if sem.predicate == "WH-QUERY":

        subj = find_subj(sem)
        theme = find_theme(sem)
        time = find_time(sem)
        if not time:
            time = "?t"
        verb_type = find_verb_type(sem)
        
        # (ATIME ?t HUE 19:00HR)
        procedures: "list[Procedure]" = []

        if subj:
            procedures.append(Procedure(subj, ["?x"]))
        if theme:
            procedures.append(Procedure(verb_type, ["?x", theme, time]))
        return Procedure("PRINT-ALL", ["?x"] + procedures)

def find_subj(sem):
    which_subj = find_sem_given_predicate(sem, "WHICH")
    if which_subj and which_subj.relations:
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