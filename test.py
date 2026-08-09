from main import create_points, tokenize, solve, tokens_are_valid, last_touch, evaluate
import sympy as sp

tokens = tokenize("sin[30]")

print(tokenize(tokens))

print(create_points(tokens, ""))