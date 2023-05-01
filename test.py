def print_red(text):
    red = "\033[31m"
    reset = "\033[0m"
    print(f"{red}{text}{reset}",end='')

print_red("hello")