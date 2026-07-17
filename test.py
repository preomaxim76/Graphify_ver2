from main import evaluate, tokenize, solve

tokens = tokenize("cos[30]")
var = "x"

str_tokens = "".join(tokens)
start, end = str_tokens.rfind("("), str_tokens.find(")")

tokens = [float(i) if i.isdigit() else i for i in tokens]

#print(tokens)
print(tokens)
print(evaluate(tokens))
#print(solve(tokens))
