from main import create_points, tokenize, solve, tokens_are_valid, last_touch
import sympy as sp

tokens = tokenize("log[x]")

print(tokens)
print(tokens_are_valid(tokens))

print(last_touch(tokens))
