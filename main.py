import matplotlib.pyplot as plt
from os import system, name
import math
import sys

# Clear terminal
def clear() -> None:
    # If windows
    if name == "nt":
        system("cls")
    # If Linux/Mac
    else:
        system("clear")
    
    return 

valid_tokens = {
    "number": ["operator", "number", ")", "pro_operator", "var", "(", ""], 
    "operator": ["number", "(", "var", "pro_operator"],
    "(": ["number", "(", "pro_operator", "var"],
    ")": ["number", "(", "operator", ")", ""],
    "pro_operator": ["number", "("],
    "var": ["operator", "pro_operator", "(", ")", ""]
}

operators = {
    "operator": ["+", "-", "*", "/", "^"],
    "pro_operator": ["log", "sqrt", "sin", "cos", "tng", "ctg"]
}

# Input
def get_equation() -> str:
    statement = "Please enter your equation (quit to stop): "
    while True:
        eq = input(statement).lower()
        if eq == "quit":
            sys.exit()
        func_call = equation_is_valid(eq)
        if func_call[0]:
            return eq
        else:
            print(func_call[1])
            statement = "Please enter a valid equation: "

# Check if the equation is valid
def equation_is_valid(eq: str) -> tuple[bool, str]:
    # Must be one = only
    if eq.count("=") != 1:
        return False, "Error: '=' has not been found..."
    
    first_half, second_half = eq.split("=")
    first_half = first_half.strip()
    # First half check
    if first_half != "y" and first_half != "f(x)":
        return False, "Error: 'y' or 'f(x)' has not been found..."

    # Second half check: surface_level
    if second_half.isspace() or second_half == "":
        return False, "Error: no equation has been found..."
    if second_half.count('(') != second_half.count(')'):
        return False, "Brackets don't match"

    return True, "No error has been detected"

# Tokenize the second part of the equation (after =)
def tokenize(half: str) -> list[str]:
    stack: list[str] = []
    for token in half:
        if token.isspace() or not token:
            continue
        if stack:
            if token.isdigit() and stack[-1].isdigit():
                stack[-1] = stack[-1] + token

            elif token.isalpha() and stack[-1].isalpha():
                stack[-1] = stack[-1] + token

            else:
                stack.append(token)

        else:
            stack.append(token)
    
    return stack

# Check if the second part is valid
def tokens_are_valid(tokens: list[str]) -> tuple[bool, str, list[str]]:
    possible = operators["operator"] + operators["pro_operator"] + [")", "("]

    last_token = ""
    new_token = ""
    var = ""
    for token in tokens:
        if not (token.isdigit() or token.isalpha() or token in possible):
            return False, f"{token} is not registered"
        if token == "y":
            return False, "'y' can not be used as a variable"
        
        if not last_token and token in ("+", "*", "/"):
            return False, "Can't start with an operator"

        if token.isdigit():
            new_token = "number"
        elif token.isalpha():
            if len(token) > 4:
                return False, "Too many characters given for one word"
            if len(token) == 1:
                if not var:
                    var = token
                    new_token = "var"
                elif token == var:
                    new_token = "var"
                else:
                    return False, "Unregistered Token"
            elif token in operators["operator"]:
                new_token = "operator"
            elif token in operators["pro_operator"]:
                new_token = "pro_operator"
            else:
                return False, "Unregistered Character"

        elif token in "()":
            new_token = token
        elif token in operators["operator"]:
            new_token = "operator"
        else:
            new_token = "pro_operator"

        if last_token:
            for vt in valid_tokens:
                if vt == last_token and new_token in valid_tokens[vt]:
                    break
            else:
                return False, "Incorrect Sequence"
        
        last_token = new_token

    if "" in valid_tokens[new_token]:
        return True, "200"
    else:
        return False, "Cannot end with that character"

# Create graph points
def create_points():
    pass

# Simplify equation and give it to solve_expression()
def evaluate():
    pass

# Solve simplified equation
def solve_expression():
    pass

# Open a window with graph
def create_graph():
    pass


def main():
    clear()
    while True:
        # Get equation, checked on a surface level
        equation = get_equation()

        # Check on a deep level
        second_half = equation.split("=")[1].strip()
        tokenized_half = tokenize(second_half)

        func_return = tokens_are_valid(tokenized_half)

        if not func_return[0]:
            print(f"Error: {func_return[1]}")
            continue 
        else:
            print("checked!")

        


if __name__ == "__main__":
    main()

