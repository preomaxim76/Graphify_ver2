from main import create_points, tokenize, solve, tokens_are_valid, last_touch, evaluate
import sympy as sp

tokens = tokenize("-1.5x(10x+20x)")

print(tokens)

print(tokens_are_valid(tokens))

print(last_touch(tokens))