import pandas
import math

def read(filename):
    Gcode = []
    for i in filename:
        i = i.strip("\n")
        Gcode.append(i)
    return Gcode

def send(Gcode):
    for i in Gcode:
        if i[4] == 'X':
            i = i.strip("G01 ")
            X,Y = i.split(" ")
            #ros send X
            #ros send y



if __name__ == '__main__':
    file = open("probegcode.gcode", "r+")
    Gcode = read(file)

