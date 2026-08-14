from main import create_points, tokenize, solve, tokens_are_valid, last_touch, evaluate
import sympy as sp

tokens = tokenize("sin[x]^x")

print(tokens)

print(tokens_are_valid(tokens))

print(create_points(tokens, "x"))
