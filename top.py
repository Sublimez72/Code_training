
import argparse
import json

parser = argparse.ArgumentParser(
    description='Show top lines from a file.', prog="Top")
parser.add_argument('filename')
parser.add_argument('-l', '--lines', type=int, default=10)
parser.add_argument('-t', '--text', action="store_true",
                    help="Show the top lines from a text file.")
parser.add_argument('-j', '--json',  action="store_true",
                    help="Show the top line from a JSON file.")

args = parser.parse_args()


if args.text == True:
    with open(args.filename, "r", encoding="utf-8") as f:
        counter = 0
        for line in f:
            if counter < args.lines:
                print(line, "")
                counter += 1

elif args.json == True:
    with open(args.filename, "r", encoding="utf-8") as f:
        file = json.load(f)
        counter = 0
        for line in file:
            if counter < args.lines:
                print(line)
                counter += 1
else:
    print("You need to specify if the file is a text file or JSON file! ")
