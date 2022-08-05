import csv

word = ""
month = "file.csv"
money = 0.0

with open(month, newline="") as csv_file:
    reader = csv.reader(csv_file, delimiter=";")
    for row in reader:
        if row[1] == "Belopp":
            continue
        if word in row[5].lower():
            amount = row[1]
            amount = amount.replace(",", ".")
            print(amount)
            money += float(amount)

    print(money)
