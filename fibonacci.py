import argparse


parser = argparse.ArgumentParser(
    description="Displays the fibonacci sequence up to a requested number.")
parser.add_argument("number", type=int)

arg = parser.parse_args()


def fibonacci(num):
    a, b = 1, 1
    print(a)
    x = 0
    while x <= num:
        print(b)
        a, b = b, a + b
        x += 1


if __name__ == "__main__":
    fibonacci(arg.number)
