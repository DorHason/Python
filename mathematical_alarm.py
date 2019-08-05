"""
A Mathematical Alarm
In order to dismiss the alarm one has to solve a random mathematical expression,
generated according to the difficulty the user has entered when setting the alarm
!!! VLC PLAYER MUST BE INSTALLED ON THE COMPUTER !!!
"""
import time
import easygui
import vlc # vlc player must be installed
import random


class Alarm:

    def __init__(self, name, hour, min, mode, repeat=False, days=[]):
        self.name = name
        self.hour = hour
        self.min = min
        self.mode = mode
        self.repeat = repeat
        self.days = days


def set_alarm():
    """
    an interface with the user to set a new alarm
    returns an instance of Alarm
    """
    name = input("Enter the name of the Alarm: ")
    hour = int(input("Enter the hour: "))
    min = int(input("Enter the minutes: "))
    mode = input("Choose a mode for dismissing the alarm: ('easy'/'medium'/'hard'/'expert')\n")
    # repeat = input("Do you want to repeat this alarm?: (y/n)")
    # if repeat == 'y':
    alarm = Alarm(name, hour, min, mode)
    return alarm


def generate_exp(mode):
    """
    gets a mode representing the difficulty
    and generates a random mathematical expression based on this mode
    returns the expression as a string
    """
    modes = {'easy': 2, 'medium': 3, 'hard': 4, 'expert': 5}
    ops = ['+', '-', '*']
    expression = ''
    op = ''
    answer = 0
    for i in range(modes[mode]):
        # split to cases to determine difficulty
        if mode == 'easy':
            op = ops[random.randint(0, 1)]
            number = random.randint(1, 10)
        elif mode == 'medium':
            op = ops[random.randint(0, 1)]
            number = random.randint(10, 100)
        elif mode == 'hard':
            op = ops[random.randint(0, 2)]
            number = random.randint(10, 100)
        elif mode == 'expert':
            op = ops[random.randint(0, 2)]
            number = random.randint(100, 1000)
        # mode is not valid
        else:
            return 0
        expression += str(number) + op

    # last letter is an unnecessary op
    expression = expression[:-1]
    return expression


def solution(string):
    """
    gets a mathematical expression as a string and returns its solution as an integer
    """
    expression = []
    number = 0
    for letter in string:
        # check if the letter is a number
        if '0' <= letter <= '9':
            number = number * 10 + int(letter)
        # else the letter is an operation
        else:
            expression.append(number)  # append previous number
            expression.append(letter)  # append operation
            number = 0
    expression.append(number)  # append last number

    # calculate and return solution
    solution = solution2(expression)
    return solution


def solution2(mylist):
    """
    gets a mathematical expression as a list comprised of numbers (as integers)
    and operatations (as strings), calculates and return its solution
    """
    # calculate multiplication first
    if '*' in mylist:
        index = mylist.index('*')
        return solution2(mylist[:index - 1] + [mylist[index - 1] * mylist[index + 1]] + mylist[index + 2:])
    else:
        # no multiplication - no importance for the order of the expression
        sum = mylist[0]
        for i in range(1, len(mylist) - 1, 2):
            if mylist[i] == '+':
                sum += mylist[i + 1]
            elif mylist[i] == '-':
                sum -= mylist[i + 1]
        return sum


if __name__ == '__main__':

    # set alarm
    alarm = set_alarm()

    # choose a song
    print("Please choose a song from your files,")
    print("This song will wake you up")
    file = easygui.fileopenbox()
    song = vlc.MediaPlayer(file)

    # generate expression based on the alarm mode
    expression = generate_exp(alarm.mode)

    # wait for the right time to activate the alarm
    while True:
        if time.localtime().tm_hour == alarm.hour and time.localtime().tm_min == alarm.min:
            print("Good Morning!")
            break

    # activate alarm
    song.play()

    # dismiss only when the user enters the right solution
    while True:
        print("Solve to dismiss")
        print(expression)
        answer = input()
        try:
            if int(answer) == solution(expression):
                song.stop()
                break
        except ValueError:
            pass
        print("\nWRONG ANSWER\n")
