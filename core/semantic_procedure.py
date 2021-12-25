from core.grammar_relation import SEM

class Procedure:
    pass

MAP_WORD_TO_DATA_VAR = {
    "tàu_hoả": "TRAIN",
    "đến": "ATIME",
    "từ": "DTIME"
}

def proceduralize(sem: SEM) -> "list[Procedure]":
    if sem.predicate == "WH-QUERY":

        subj = find_subj(sem)
        theme = find_theme(sem)
        time = find_time(sem)
        verb_type = find_verb_type(sem)
        
        # (ATIME ?t HUE 19:00HR)

        q_type = f"PRINT-ALL ?x ({subj} ?x) ({verb_type} ?t {theme} {time})"
        
        return q_type

def find_subj(sem):
    which_subj = find_sem_given_predicate(sem, "WHICH")
    if which_subj and which_subj.relations:
        return MAP_WORD_TO_DATA_VAR[which_subj.relations[0]]

def find_theme(sem):
    theme = find_sem_given_predicate(sem, "THEME")
    if theme and theme.relations:
        return theme.relations[0].relations[0]

def find_time(sem):
    theme = find_sem_given_predicate(sem, "AT-TIME")
    if theme and theme.relations:
        return theme.relations[0]

def find_verb_type(sem):
    wh = find_sem_given_predicate(sem, "WH-QUERY")
    if wh and wh.relations:
        return wh.relations[0].predicate


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