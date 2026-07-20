import matplotlib.pyplot as plt
from os import system, name
import math
import sys
import sympy as sp

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
    "number": ["operator", "number", ")", "pro_operator", "var", "(", "]", ""], 
    "operator": ["number", "(", "var", "pro_operator"],
    "(": ["number", "(", "pro_operator", "var"],
    ")": ["number", "(", "operator", ")", ""],
    "pro_operator": ["number", "["],
    "var": ["operator", "pro_operator", "(", ")", "]", ""],
    "[": ["number", "pro_operator", "(", "var"],
    "]": ["operator", "(", ")", ""]
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
    possible = operators["operator"] + operators["pro_operator"] + [")", "(", "[", "]"] 

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

        elif token in "()" or token in "[]":
            new_token = token
        elif token in operators["operator"]:
            new_token = "operator"
        else:
            new_token = "pro_operator"

        if last_token and new_token not in valid_tokens[last_token]:
            return False, "Incorrect Sequence"
        
        last_token = new_token

    if "" in valid_tokens[new_token]:
        return True, "200", var
    else:
        return False, "Cannot end with that character"

def ctg(value):
    return 1 / sp.tan(value)

def solve(tokens: list[str]) -> tuple[float, str]:
    emergency_break = False
    if len(tokens) != 1:
        while len(tokens) > 1:
            # 1. Powers and Roots
            while "^" in tokens or "sqrt" in tokens:
                for i in range(len(tokens)):
                    if tokens[i] == "sqrt":
                        # Square root
                        if tokens[i+1] == "[":
                            if tokens[i+2] < 0:
                                return 0, "Cannot find a square root of a negative number"
                            
                            temp = math.sqrt(tokens[i+2])
                            del tokens[i:i+4]
                        # Other root
                        else:
                            if tokens[i+3] < 0 and tokens[i+1] % 2 == 0:
                                return 0, "Cannot find an even root of a negative number"
                            temp = math.pow(tokens[i+3], 1/tokens[i+1])
                            del tokens[i:i+5]

                        tokens.insert(i, temp)
                        break

                    elif tokens[i] == "^":
                        if tokens[i-1] == "]" or tokens[i+1] == "]":
                            emergency_break = True
                            break
                        temp = tokens[i-1] ** tokens[i+1]
                        del tokens[i-1:i+2]
                        tokens.insert(i-1, temp)
                        break
                if emergency_break:
                    break

                    
            # 2. Functions
            while "log" in tokens or "sin" in tokens or "cos" in tokens or "tng" in tokens or "ctg" in tokens:
                for i in range(len(tokens)):
                    match tokens[i]:
                        case "log":
                            # log2
                            if tokens[i+1] == "[":
                                if tokens[i+2] <= 0:
                                    return 0, "Value cannot be 0 or a negative number"

                                temp = math.log2(tokens[i+2])
                                del tokens[i:i+4]

                            else:
                                
                                if tokens[i+1] <= 1:
                                    return 0, "Base cannot be 1, 0 or a negative number"
                                if tokens[i+3] <= 0:
                                    return 0, "Value cannot be 0 or a negative number"
                                
                                temp = sp.log(tokens[i+3], tokens[i+1])
                                del tokens[i:i+5]

                            tokens.insert(i, temp)
                            break

                        case "sin":
                            if tokens[i+1] == "[":
                                radians_value = sp.rad(tokens[i+2])
                                temp = sp.sin(radians_value).n()
                                del tokens[i:i+4]
                            else:
                                radians_value = round(math.radians(tokens[i+3]), 1)
                                temp = sp.sin(radians_value).n() ** tokens[i+1]
                                del tokens[i:i+5]
                            
                            tokens.insert(i, temp)
                            break

                        case "cos":
                            if tokens[i+1] == "[":
                                radians_value = sp.rad(tokens[i+2])
                                temp = sp.cos(radians_value).n()
                                del tokens[i:i+4]
                            else:
                                radians_value = sp.rad(tokens[i+3])
                                temp = sp.cos(radians_value).n() ** tokens[i+1]
                                del tokens[i:i+5]
                            
                            tokens.insert(i, temp)
                            break

                        case "tng":
                            if tokens[i+1] == "[":
                                radians_value = sp.rad(tokens[i+2])
                                temp = sp.tan(radians_value).n()
                                del tokens[i:i+4]
                            else:
                                radians_value = sp.rad(tokens[i+3])
                                temp = sp.tan(radians_value).n() ** tokens[i+1]
                                del tokens[i:i+5]
                            
                            tokens.insert(i, temp)
                            break

                        case "ctg":
                            if tokens[i+1] == "[":
                                radians_value = sp.rad(tokens[i+2])
                                temp = ctg(radians_value).n()
                                del tokens[i:i+4]
                            else:
                                radians_value = sp.rad(tokens[i+3])
                                temp = ctg(radians_value).n() ** tokens[i+1]
                                del tokens[i:i+5]

                            tokens.insert(i, temp)
                            break
            if emergency_break:
                emergency_break = False
                continue

            # 3. Multiplication and division
            while "*" in tokens or "/" in tokens:
                for i in range(len(tokens)):
                    if tokens[i] == "*":
                        temp = tokens[i-1] * tokens[i+1]
                        del tokens[i-1:i+2]
                        tokens.insert(i-1, temp)
                        break

                    elif tokens[i] == "/":
                        if tokens[i+1] == 0:
                            return 0, "Cannot divide by 0"
                        temp = tokens[i-1] / tokens[i+1]
                        del tokens[i-1:i+2]
                        tokens.insert(i-1, temp)
                        break

            # 4. + or -
            while "+" in tokens or "-" in tokens:
                for i in range(len(tokens)):
                    if tokens[i] == "+":
                        temp = tokens[i-1] + tokens[i+1]
                        del tokens[i-1:i+2]
                        tokens.insert(i-1, temp)
                        break

                    elif tokens[i] == "-":
                        tokens[i-1:i+2] = tokens[i-1] - tokens[i+1]
                        break
    return tokens[0]


def evaluate(tokens: list[str]) -> float:
    tokens = [float(i) if i.isdigit() or (i[0] == "-" and i[1:].isdigit()) or "." in i else i for i in tokens]
    while len(tokens) > 1:
        while "(" in tokens:
            start, end = len(tokens) - list(reversed(tokens)).index("(") - 1, tokens.index(")")
            tokens = tokens[0:start] + [solve(tokens[start+1:end])] + tokens[end+1:]
            print("Evaluate function: ", tokens)
            break
        func_return = solve(tokens)
        if type(func_return) == tuple:
            print(func_return)
            return
        tokens = [solve(tokens)]
        break
    return tokens[0]

# Create graph points
def create_points(tokens: list[str], var: str) -> tuple[list[int], list[float]]:
    if not var:
        value = evaluate(tokens)
        return [], [value * 100]

    x = []
    for i in range(-100, 101):
        for j in range(0, 100, 10):
            x.append(i + round(float(f".{j}"), 1))


    return x, [evaluate((" ".join(tokens)).replace(var, str(i)).split()) for i in x]
    

# Open a window with graph
def create_graph(tokens: list, var: str, equation: str) -> None:
    x_points, y_points = create_points(tokens, var)

    fig, ax = plt.subplots()

    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

    ax.grid(True, linestyle="--")

    ax.relim()
    ax.autoscale_view()

    ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)
    
    if not x_points:
        plt.plot(y_points)
    else:
        plt.plot(x_points, y_points)

    plt.title(f"{equation}")
    plt.show()

    return


def main() -> None:
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
        
        create_graph(tokenized_half, func_return[2], equation)

    return

        


if __name__ == "__main__":
    main()

