from main import create_points, tokenize, solve
import sympy as sp

tokens = tokenize("tng[x]")

func = create_points(tokens, "x")
print(func)

