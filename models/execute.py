from models.semantic_procedure import Procedure

def execute(procedure: Procedure):
    """
    Execute a procedure.
    """

    TRAIN_DATA, ATIME_DATA, DTIME_DATA, RUNTIME_DATA = load_data()
    
    q_type = None

    train_query = []
    duration = []
    truth = None
    if procedure.name == "PRINT-ALL":
        for pro in procedure.args:
            if isinstance(pro, Procedure) and pro.name == "TRAIN":
                if pro.args[0] == "?x":
                    train_query = [x for x in TRAIN_DATA]
                    q_type = "TRAIN"

            elif isinstance(pro, Procedure) and pro.name == "ATIME":
                atimes_query = {} # ATIME of only trains in question
                args = pro.args
                for train in train_query:
                    atimes_query[train] = ATIME_DATA[train]

                queries = []
                if "?" not in args[1]:
                    queries.append(args[1])
                if "?" not in args[2]:
                    queries.append(args[2])
                tmp = []
                for train in train_query:
                    if(all(x in atimes_query[train] for x in queries)):
                        tmp.append(train)
                train_query = tmp

            elif isinstance(pro, Procedure) and pro.name == "DTIME":
                dtimes_query = {} # DTIME of only trains in question
                args = pro.args
                for train in train_query:
                    dtimes_query[train] = DTIME_DATA[train]

                queries = []
                if "?" not in args[1]:
                    queries.append(args[1])
                if "?" not in args[2]:
                    queries.append(args[2])

                tmp = []
                for train in train_query:
                    if(all(x in dtimes_query[train] for x in queries)):
                        tmp.append(train)
                train_query = tmp
            # elif isinstance(pro, Procedure) and pro.name == "DURATION":
            #     # Mark duration in question
            #     duration = 0
            elif isinstance(pro, Procedure) and pro.name == "RUN-TIME":
                q_type = "RUN-TIME"
                args = pro.args

                queries = []
                for i in range(4):
                    if "?" not in args[i]:
                        queries.append(args[i])

                runtime_data = []

                for train in RUNTIME_DATA:
                    runtime_data.append([train] + RUNTIME_DATA[train])

                for runtime in runtime_data:
                    if(all(x in runtime for x in queries)):
                        duration.append(runtime)

    if procedure.name == "EXISTS":
        q_type = "YESNO"
        for pro in procedure.args:
            if isinstance(pro, Procedure) and pro.name == "TRAIN":
                if pro.args[0] == "?x":
                    train_query = [x for x in TRAIN_DATA]
                    q_type = "TRAIN"
                else:
                    train_query = [x for x in TRAIN_DATA if pro.args[0] == x]
                if not train_query:
                    truth = "Không."
                    break

            elif isinstance(pro, Procedure) and pro.name == "ATIME":
                atimes_query = {} # ATIME of only trains in question
                args = pro.args
                for train in train_query:
                    atimes_query[train] = ATIME_DATA[train]

                queries = []
                if "?" not in args[1]:
                    queries.append(args[1])
                if "?" not in args[2]:
                    queries.append(args[2])
                tmp = []
                for train in train_query:
                    if(all(x in atimes_query[train] for x in queries)):
                        tmp.append(train)
                train_query = tmp

            elif isinstance(pro, Procedure) and pro.name == "DTIME":
                dtimes_query = {} # DTIME of only trains in question
                args = pro.args
                for train in train_query:
                    dtimes_query[train] = DTIME_DATA[train]

                queries = []
                if "?" not in args[1]:
                    queries.append(args[1])
                if "?" not in args[2]:
                    queries.append(args[2])

                tmp = []
                for train in train_query:
                    if(all(x in dtimes_query[train] for x in queries)):
                        tmp.append(train)
                train_query = tmp
        
        if not train_query:
            truth = "Không."
        else:
            truth = "Có."

    ans_string = ""
    if q_type == "TRAIN" and train_query:
        ans_string += ", ".join(train_query) + "."
    elif q_type == "TRAIN":
        ans_string += "Không tìm thấy."
    if duration:
        ans_string += str(duration[0][3])
    elif q_type == "RUN-TIME":
        ans_string += "Không tìm thấy."
    if truth:
        ans_string += truth
    elif q_type == "YESNO":
        ans_string += "Không xác định được."
    
    return ans_string

def load_data(path=None):
    """
    Load data from a file.
    """
    TRAIN = {}
    ATIME = {}
    DTIME = {}
    RUNTIME = {}
    path = "input/database.txt"
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
            if tokens[0] == "RUN-TIME":
                RUNTIME[tokens[1]] = tokens[2:]
    
    return TRAIN, ATIME, DTIME, RUNTIME