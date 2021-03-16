import matplotlib.pyplot as plt
import csv
def read(file):
    lines = []
    chars = []
    file = open(file)
    for x in file:
        lines.append(x)
    for y in lines:
        col = []
        for z in range(len(y)):
            col.append(y[z])
        chars.append(col)
    file.close
    return chars

def pointConv(cord):
    i = len(cord)-1
    tempstring = ""
    while cord[i] == '0':
       i -= 1
    if cord[i] == '5':
        i -= 1
    cord.insert(i-2,'.')
    for i in range(len(cord)):
        tempstring += cord[i]
    cord = float(tempstring)
    return cord

def start_end(arr):
    xStart = 0
    xEnd = 0
    yStart = 0
    yEnd = 0
    for i in range(len(arr)):
        if arr[i] == 'X':
            xStart = i + 1
        if arr[i] == 'Y':
            xEnd = i - 1
            yStart = i + 2
        yEnd = -5
    return xStart,xEnd,yStart,yEnd

def bounding_box(file):
    chars = read(file)
    lines = []
    xlist = []
    ylist = []
    for x in range(len(chars)):
        if chars[x][0] == 'X':
            lines.append(chars[x])
    for x in lines:
        xcord = []
        ycord = []
        count = 1
        while x[count] != 'Y':
            xcord.append(x[count])
            count += 1
        count += 1
        while x[count] != 'D' and x[count] != 'I' and count < len(x):
            ycord.append(x[count])
            count += 1
        xcord = pointConv(xcord)
        xlist.append(xcord)
        ycord = pointConv(ycord[1:])
        ylist.append(ycord)
    minX = min(xlist)
    minY = min(ylist)
    print(minY)
    return tuple((minX,minY))

def scan(arr,zerocord):
    points = []
    minX,minY = zerocord
    for i in range(len(arr)):
        if arr[i][4] == 'P':
            check = ""
            for x in range(5):
                check += arr[i][x]
            if check == "%TO.P":
                z = 0
                while arr[i+z][0] != 'X':
                    z += 1
                part = str(arr[i][6]+arr[i][7])
                pad = arr[i][9]
                if arr[i][10] != '*':
                    pad += arr[i][10]
                xStart, xEnd, yStart, yEnd = start_end(arr[i+z])
                yEnd = -5
                xCord = arr[i+z][xStart:xEnd]
                yCord = arr[i+z][yStart:yEnd]
                xCord = pointConv(xCord)
                yCord = pointConv(yCord)
                xCord = xCord-minX
                yCord = yCord-minY
                points.append(tuple((part,pad,xCord,yCord)))
    return points


def output(arr,name):
    file = open(name,"w",newline='')
    fieldnames = ['Part','Pad','X Cord','Y Cord']
    writer = csv.DictWriter(file,fieldnames=fieldnames, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    for i in range(len(arr)):
        (part,pad,xCord,yCord) = arr[i]
        #line = ("%s %s %f %f\n"%(part,pad,xCord,yCord))
        writer.writerow({"Part" : part,"Pad" : pad,"X Cord" : xCord,"Y Cord":yCord})
    file.close()

def plot(points):
    xCords = []
    yCords = []
    for i in range(len(points)):
        (part, pad, xCord, yCord) = points[i]
        xCords.append(xCord)
        # can make y cord negative to match top left zero location
        yCords.append(yCord)
    plt.scatter(xCords,yCords)
    plt.show()

"""
Need to manage circular interpolation
http://www.helmancnc.com/circular-interpolation-concepts-programming-part-4/
https://www.artwork.com/gerber/appl2.htm
"""



if __name__ == '__main__':
    chars = read('Main-F_Cu.gbr')
    zerocord = bounding_box('Main-Edge_Cuts.gbr')
    points = scan(chars,zerocord)
    plot(points)
    output(points, "output.csv")


