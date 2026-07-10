from main import tokens_are_valid, tokenize

tokens = tokenize(input())
print(tokens)

are, message = tokens_are_valid(tokens)

if not are:
    print(message)
else:
    print("hooray")



