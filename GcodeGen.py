import pandas
import math

class Fake(object):
    def __init__(self, li_obj):
        self.obj = li_obj
        self.row = 0
    def getList(self):
        return self.obj
    def getRow(self):
        return self.row
    def setRow(self,input):
        self.row = input
    def setList(self,list):
        self.obj = list
    def delete(self,input):
        del self.obj[input]


def Trianglemath(X1,Y1,X2,Y2):
    if X1>X2:
        length = math.sqrt(X1*X1 + Y2*Y2)
    else:
        length = math.sqrt(X2*X2+Y1*Y1)
    return length

def anglemath(PX1,PY1,PX2,PY2,MX,MY):
    try:
        Slope1 = (PY1-MY)/(PX1-MX)
    except:
        Slope1 = 0
    try:
        Slope2 = (PY2-MY)/(PX2-MX)
    except:
        Slope2 = 0
    angle = math.atan(((Slope2-Slope1)/(1+Slope2*Slope1)))
    return angle

def getflags(data):
    listcheck = False
    dupecheck = False
    flaglist = []
    for x in range(len(data['Flags'])):
        if data['Flags'][x] == "":
            continue
        flag = data['Flags'][x]
        flag = flag.strip("P")
        flag = flag.strip("G")
        flag = flag.strip()
        for y in range(len(flag)):
            if flag[y] == ",":
                listcheck = True
        if listcheck:
            templist = flag.split(",")
            for y in templist:
                y = y.strip("P")
                y = y.strip("G")
                y = y.strip()
                for i in flaglist:
                    if y == i:
                        dupecheck = True
                if dupecheck:
                    dupecheck = False
                    continue
                else:
                    flaglist.append(y)
            listcheck = False
        else:
            for y in flaglist:
                if flag == y:
                    dupecheck = True
                    break
            if not dupecheck:
                flaglist.append(flag)
    return flaglist

def getpartpad(flag):
    pins = flag.split("<>")
    pin1 = pins[0].split("-")
    pin2 = pins[1].split("-")
    part1 = pin1[0]
    pad1 = pin1[1]
    part2 = pin2[0]
    pad2 = pin2[1]
    return part1,int(pad1),part2,int(pad2)

def generate(data):
    Zfloor = 0
    Ztop = 10
    Curangle = 0
    Nextangle = 0
    Curlength = 0
    Nextlength = 0
    file = open("probegcode.gcode", "w")
    gcode = """Still need to figure out starter gcode\n"""
    flaglist = getflags(data)
    for flag in flaglist:
        part1, pad1, part2, pad2 = getpartpad(flag)
        Xcord1 = 0
        Ycord1 = 0
        Xcord2 = 0
        Ycord2 = 0
        for y in range(len(data['Flags'])):
            if data['Part'][y] == part1:
                if data['Pad'][y] == pad1:
                    Xcord1 = float(data['X Cord'][y])
                    Ycord1 = float(data['Y Cord'][y])
            if data['Part'][y] == part2 and data['Pad'][y] == pad2:
                Xcord2 = float(data['X Cord'][y])
                Ycord2 = float(data['Y Cord'][y])

        Xmid = (Xcord1 + Xcord2) /2
        Ymid = (Ycord1 + Ycord2) /2

        tempstring = ("G01 Z%s\n" % (Ztop))
        tempstring += ("G01 X%s Y%s\n" % (Xmid,Ymid))

        Nextangle = anglemath(Xcord1,Ycord1,Xcord1,Ycord2,Xmid,Ymid)
        tempstring += ("G01 R%s\n" % (math.degrees(Nextangle-Curangle)))

        Nextlength = Trianglemath(Xcord1,Ycord1,Xcord2,Ycord2)
        tempstring += ("G01 L%s\n" % (Nextlength-Curlength))
        tempstring += ("G01 Z%s\n" % (Zfloor))
        Curangle = Nextangle
        Curlength = Nextlength
        gcode += tempstring
    file.write(gcode)
    file.close()



if __name__ == '__main__':
    df = pandas.read_pickle("Config.pkl")
    generate(df)
