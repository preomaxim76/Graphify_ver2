from main import create_points, tokenize

tokens = tokenize("log[x]")

func = create_points(tokens, "x")
print(func)
