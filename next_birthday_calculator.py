
import argparse
from datetime import datetime


parser = argparse.ArgumentParser(
    description="Calculates how many days the user has been alive and how many days until their next birthday.")
parser.add_argument("-y", "--year", required=True, type=int)
parser.add_argument("-m", "--month", required=True, type=int)
parser.add_argument("-d", "--day", required=True, type=int)

args = parser.parse_args()


currentDate = datetime.now()


birthday = datetime(args.year, args.month, args.day)

differenceBirthday = currentDate - birthday

differenceNextBirthday = datetime(
    currentDate.year, birthday.month, birthday.day) - currentDate


if differenceNextBirthday.days < 0:
    differenceNextBirthday = datetime(
        currentDate.year + 1, birthday.month, birthday.day) - currentDate

print("U were born {0} days ago and ur next birthday is in {1} days".format(
    differenceBirthday.days, differenceNextBirthday.days))
