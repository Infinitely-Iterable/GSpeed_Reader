import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv('.env'), override=True)

MY_ENV_VAR = os.getenv("MY_ENV_VAR")


class terminalColors:
    # ANSI color codes
    RED="\033[31m"
    BLUE="\033[36m"
    ENDCOLOR="\033[0m]"
        

colors = terminalColors()


print(f"{colors.RED}HELLO GRANT!{colors.BLUE} DAN HAS SMALL BALLS! OH NO!{colors.ENDCOLOR}")


class Person():
    def __init__(self, first_name, last_name, age=0):
        self.name = first_name + " " + last_name
        self.age = int(age)
        self.whatever = "Whatever"

    def get_retirement_age(self):
        return 65 - self.age


    def print_whatever(self):
        print(self.whatever)
    



dan = Person(first_name="Dan", last_name="Simon", age=28)
austin = Person(first_name="Austin", last_name="ONeil", age=28)
grant = Person(first_name="Grant", last_name="Ligma", age=10)
# print(dan.get_retirement_age())




def xyz(x):
    if x > 5:
        return "Greater than 5"
    return "Not greater than 5"


def abc(x):
    if x > 5:
        return True, "Greater than 5"
    return False, "Not greater than 5"

a = xyz(6)
print(a)

print(xyz(6))

h,f = abc(6)
print(h)
print(f)
