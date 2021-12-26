from models.preprocess import preprocess
from models.maltparse import malt_parse
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.execute import execute
from models.io import get_questions, write_to_file
import argparse

def run_query(query: str, extra_log=True):

    log_string = ""
    
    log_string += "Câu hỏi: " + query + "\n"

    tokens = preprocess(query)
    context_deps = malt_parse(tokens)
    relations = relationalize(context_deps)
    sem = logicalize(relations)
    procedure = proceduralize(sem)
    ans = execute(procedure)

    if extra_log:
        log_string += "\n** Dependencies **\n"
        for x in context_deps:
            log_string += str(x) + "\n"

        log_string += "\n** Grammar Relations **\n"
        for x in relations:
            log_string += str(x) + "\n"

        log_string += "\n** Logical Form **\n"
        log_string += str(sem) + "\n"

        log_string += "\n** Procedure **\n"
        log_string += str(procedure) + "\n"

        log_string += "\n"

    log_string += f"Trả lời: {ans}\n"

    return log_string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbosity",
                        help="In ra chi tiết output của các thành phần được phân tích.",
                        action="store_true", default=False)
    parser.add_argument("-s", "--sentence",
                        help="Nhập câu hỏi trực tiếp trên command line")
    
    args = parser.parse_args()

    if args.sentence:
        try:
            print(run_query(args.sentence, args.verbosity), end="")
        except:
            print("Không thể trả lời câu hỏi này. Vui lòng thử câu khác.")
        return

    queries = get_questions("input/questions.txt")

    a_th = ord("a")

    for index, query in enumerate(queries):
        output_log = ""
        try:
            output_log += run_query(query, True)
        except:
            output_log("Không thể trả lời câu hỏi này. Vui lòng thử câu khác.")

        write_to_file(output_log, f"output/output_{chr(a_th + index)}.txt")

if __name__ == "__main__":
    main()