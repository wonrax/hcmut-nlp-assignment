from core.semantic_procedure import Procedure

def execute(procedure: Procedure):
    """
    Execute a procedure.
    """

    TRAIN_DATA, ATIME_DATA, DTIME_DATA, RUNTIME_DATA = load_data()

    if procedure.name == "PRINT-ALL":
        train_query = []
        for pro in procedure.args:
            if isinstance(pro, Procedure) and pro.name == "TRAIN":
                if pro.args[0] == "?x":
                    train_query = [x for x in TRAIN_DATA]
            elif isinstance(pro, Procedure) and pro.name == "ATIME":
                atimes_query = {} # ATIME of only trains in question
                args = pro.args
                for train in train_query:
                    atimes_query[train] = ATIME_DATA[train]

                train_query = []
                for train in atimes_query:
                    queries = []
                    if "?" not in args[1]:
                        queries.append(args[1])
                    if "?" not in args[2]:
                        queries.append(args[2])
                    if(all(x in atimes_query[train] for x in queries)):
                        train_query.append(train)
        print(train)

def load_data(path=None):
    """
    Load data from a file.
    """
    TRAIN = {}
    ATIME = {}
    DTIME = {}
    RUNTIME = {}
    path = "data/database.txt"
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            line = line.replace("\n", "")
            
            tokens = line.split(" ")

            if tokens[0] == "TRAIN":
                TRAIN[tokens[1]] = ""
            if tokens[0] == "ATIME":
                ATIME[tokens[1]] = tokens[2:]
            if tokens[0] == "DTIME":
                DTIME[tokens[1]] = tokens[2:]
            if tokens[0] == "RUNTIME":
                RUNTIME[tokens[1]] = tokens[2:]
    
    return TRAIN, ATIME, DTIME, RUNTIME