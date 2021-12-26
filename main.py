from core.preprocess import preprocess
from core.maltparse import malt_parse
from core.grammar_relation import relationalize
from core.logical_form import logicalize
from core.semantic_procedure import proceduralize
from core.execute import execute


query = "Tàu hoả nào đến thành phố Huế lúc 19:00HR ?"
query = "tàu hỏa nào đến thành phố hồ chí minh?"
query = "Tàu hỏa nào đến Đà Nẵng lúc 11:30HR?"
# query = "Thời gian tàu hỏa B3 chạy từ Đà Nẵng đến TP. Hồ Chí Minh" \
#         + " là mấy giờ?"

tokens = preprocess(query)
print(tokens)

context_deps = malt_parse(tokens)

[print(x) for x in context_deps]

print("------\n-------Grammar Relationalize-------------")
relations = relationalize(context_deps)
[print(x) for x in relations]

print("------\n-------Logical Form-------------")
sem = logicalize(relations)

print("------\n-------Procedural-------------")
procedure = proceduralize(sem)
print(procedure)

print("------\n-------Execute-------------")
execute(procedure)