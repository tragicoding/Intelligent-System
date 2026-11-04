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

response = {
    "function_name" : "add",
    "kwargs" : {"a" : 1, "b" : 10}
}

#-----------Hardcoding for specific----------
function_name = response.get("function_name")
kwargs = response.get("kwargs")

print(function_name)
print(kwargs)

#==========Hardcoding for somthing function from the loockup table
print(FN_LOOK_UP["add"](**kwargs))
