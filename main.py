import matplotlib.pyplot as plt
from os import system, name
import math

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
    "operator": ["number", "(", "var"],
    "(": ["number", "(", "pro_operator", "var"],
    ")": ["number", "(", "operator", ""],
    "pro_operator": ["number", "("],
}

operators = {
    "operator": ["+", "-", "*", "/", "^"],
    "pro_operator": ["log", "sqrt", "sin", "cos", "tng", "ctg"]
}

# Input
def get_equation() -> str:
    statement = "Please enter your equation: "
    while True:
        eq = input(statement).lower()
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
    if second_half.isspace():
        return False, "Error: no equation has been found..."

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
def tokens_are_valid() -> tuple[bool, str]:
    pass

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
        second_half = equation.split()[1].strip()
        tokenized_half = tokenize(second_half)

        if not tokens_are_valid(tokenized_half):
            # TODO: Print error
            continue 

        


if __name__ == "__main__":
    main()

