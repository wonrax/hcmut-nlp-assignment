from core.preprocess import preprocess
from core.maltparse import malt_parse
from core.grammar_relation import relationalize

query = "Tàu hoả nào đến thành phố Huế lúc 19:00HR ?"
query = "tàu hỏa nào đến thành phố hồ chí minh ? "
query = "Tàu hỏa nào đến Đà Nẵng lúc 12:45HR ? "

tokens = preprocess(query)
print(tokens)

context_deps = malt_parse(tokens)

[print(x) for x in context_deps]

print("------\n-------Grammar Relationalize-------------")
[print(x) for x in relationalize(context_deps)]