from core.preprocess import preprocess
from core.maltparse import malt_parse
from core.grammar_relation import relationalize
from core.logical_form import logicalize
from core.semantic_procedure import proceduralize
from core.execute import execute

queries = []

queries.append("Tàu hỏa nào đến thành phố Huế lúc 19:00HR ?")
queries.append("Thời gian tàu hỏa B3 chạy từ thành phố Đà Nẵng đến TP. Hồ Chí Minh là mấy giờ?")
queries.append("Tàu hỏa nào đến thành phố Hồ Chí Minh ?")
# queries.append("Tàu hỏa nào chạy từ Nha Trang, lúc mấy giờ?")
queries.append("Tàu hỏa nào chạy từ Nha Trang?")
queries.append("Tàu hỏa nào chạy từ TP. Hồ Chí Minh đến Hà Nội ?")
queries.append("Tàu hỏa B5 có chạy từ Đà Nẵng không ?")

def run_query(query: str):
    tokens = preprocess(query)

    context_deps = malt_parse(tokens)

    print("\n** Dependencies **")
    [print(x) for x in context_deps]

    print("\n** Grammar Relations **")
    relations = relationalize(context_deps)
    [print(x) for x in relations]

    print("\n** Logical Form **")
    sem = logicalize(relations)

    print("\n** Procedure **")
    procedure = proceduralize(sem)
    print(procedure)

    print("\n** Execute **")
    execute(procedure)

if __name__ == "__main__":
    for query in queries:
        print("\n----------------------------------")
        print("---------------Query--------------")
        print("----------------------------------")
        print(query)
        run_query(query)