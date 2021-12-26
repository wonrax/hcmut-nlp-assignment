from core.preprocess import preprocess
from core.maltparse import malt_parse
from core.grammar_relation import relationalize
from core.logical_form import logicalize
from core.semantic_procedure import proceduralize
from core.execute import execute


# query = " Tàu hỏa nào đến thành phố Huế lúc 19:00HR ?"
# query = "Thời gian tàu hỏa B3 chạy từ thành phố Đà Nẵng đến TP. Hồ Chí Minh" \
#         + " là mấy giờ?"
# query = "Tàu hỏa nào đến thành phố Hồ Chí Minh ?"
# query = "Tàu hỏa nào chạy từ Nha Trang, lúc mấy giờ"
query = "Tàu hỏa nào chạy từ TP. Hồ Chí Minh đến Hà Nội ?"
# query = "Tàu hỏa B5 có chạy từ Đà Nẵng không ?"

tokens = preprocess(query)
print(tokens)

context_deps = malt_parse(tokens)

print("\n-------------Dependencies--------------")
[print(x) for x in context_deps]

print("\n-------------Grammar Relations--------------")
relations = relationalize(context_deps)
[print(x) for x in relations]

print("\n-------------Logical Form--------------")
sem = logicalize(relations)

print("\n-------------Procedure--------------")
procedure = proceduralize(sem)
print(procedure)

print("\n-------------Execute--------------")
execute(procedure)