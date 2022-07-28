def show(func):
    def wrapper(*args):
        print(func(args[0]))
    return wrapper
