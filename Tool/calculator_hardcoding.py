SYSTEM_PROMPT = {...}

def add(a,b):
    return a+b
def subtract(a,b):
    return a-b
def multiply(a,b):
    return a*b
def divide(a,b):
    if b==0:
        raise ValueError
    else:
        return a/b

FN_LOOK_UP = {
    "add" : add,
    "subtract" : subtract,
    "multiply" : multiply,
    "divide": divide
}

#Example
print(FN_LOOK_UP["add"](10,1))