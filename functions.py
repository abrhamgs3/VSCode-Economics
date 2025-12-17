def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

name = input("Enter your name: ")

print(greet(name))

a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("The sum is:", add(a, b))