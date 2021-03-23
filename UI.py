import matplotlib.pyplot as plt
import pandas
import plotly.express as px
import numpy as np
from mpldatacursor import datacursor
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

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


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

def plotgerber(canvas, fig,ax,canvas_toolbar,c_row,p_row,xCords,yCords,name,textarr,color):

    if p_row is not None:
        ax.plot(xCords[p_row],yCords[p_row],marker = 'o', color = 'tab:blue')
    if c_row is not None:
        ax.plot(xCords[c_row],yCords[c_row],color)
        textvar = ax.annotate(name, (xCords[c_row], yCords[c_row]))
        #kinda gross but seems needed
        #deletes old text
        if len(textarr) > 0:
            textarr[-1].remove()
            textarr.pop(-1)
        textarr.append(textvar)
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()

    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

def makeEditor(data,row1,row2):
    pin1 = data['Flags Data'][row1[0]].getList()
    pin2 = data['Flags Data'][row2[0]].getList()
    tstring1 = ("Table 1: %s-%s"%(data['Part'][row1[0]],data['Pad'][row1[0]]))
    tstring2 = ("Table 2: %s-%s"%(data['Part'][row2[0]],data['Pad'][row2[0]]))
    layout = [
        [sg.Text(tstring1,size=(25,1)),sg.Text(tstring2)],
        [
            sg.Table(key='P1table',
                     values=pin1,
                     # Dont want to show flag data class so only show up to flags column
                     headings=["link","Power/Ground"],
                     display_row_numbers=False,
                     auto_size_columns=False,
                     enable_events=True,
                     num_rows=min(5, len(pin1))),
            sg.Table(key='P2table',
                     values=pin2,
                     # Dont want to show flag data class so only show up to flags column
                     headings=["link","Power/Ground"],
                     display_row_numbers=False,
                     auto_size_columns=False,
                     enable_events=True,
                     num_rows=min(5, len(pin2)))],
        [sg.Button("Table 1 Delete"),sg.Button("Table 2 Delete")]
    ]
    P1Class = data['Flags Data'][row1[0]]
    P2Class = data['Flags Data'][row2[0]]
    return sg.Window('Flag Editor', layout,finalize=True),P1Class,P2Class


def UI(data):

    gerber_Layout = [
        [sg.Canvas(key='tool_bar')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='fig_cv',size=(400 * 2, 400))]
                # it's important that you set this size
                ],
            background_color='#DAE0E6',
            pad=(0, 0)
        )]
        ]

    data_Layout = [
        [sg.In(size=(25, 1), enable_events=True, key='data'),
         sg.Button('Search')],
        [sg.Text('Power',size=(58,1)),sg.Text('Ground')],
        [
            sg.Table(key='Ftable1',
                           values=data.values.tolist(),
                           # Dont want to show flag data class so only show up to flags column
                           headings=data.columns[:5].tolist(),
                           display_row_numbers=False,
                           auto_size_columns=False,
                           enable_events=True,
                           num_rows=min(25, len(data))),
            sg.Table(key='Ftable2',
                     values=data.values.tolist(),
                     # Dont want to show flag data class so only show up to flags column
                     headings=data.columns[:5].tolist(),
                     display_row_numbers=False,
                     auto_size_columns=False,
                     enable_events=True,
                     num_rows=min(25, len(data)))]
        ,
        [sg.Button('Link'), sg.Button('Edit Flags')],
        ]


    layout = [
        [
            sg.Column(data_Layout),
            sg.VSeparator(),
            sg.Column(gerber_Layout)
        ]
    ]
    flagEditor = None
    window1 = sg.Window('Gerber View', layout,finalize=True)
    window1['Ftable1'].bind('<Button-1>','+LEFT CLICK+')
    window1['Ftable2'].bind('<Button-1>', '+LEFT CLICK+')

    xCords = data['X Cord'].tolist()
    yCords = (data['Y Cord']*-1).tolist()
    fig, ax = plt.subplots()
    ax.scatter(xCords, yCords)
    DPI = fig.get_dpi()
    fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

    tempstring = ""
    p_row1 = 0
    c_row1 = 0
    p_row2 = 0
    c_row2 = 0
    textarr1 = []
    textarr2 = []
    newvalues = []
    P1Class = Fake([0,0])
    P2Class = Fake([0,0])


    while True:
        window, event, values = sg.read_all_windows()
        print(event, values)

        if event == sg.WIN_CLOSED or event == 'Exit':
            window.close()
            if window == flagEditor:  # if closing win 2, mark as closed
                flagEditor = None
            elif window == window1:  # if closing win 1, exit program
                break

        elif event == 'Ftable1+LEFT CLICK+':
            row = values['Ftable1']
            color = 'r*'
            if len(row) != 0:
                part = data['Part'][row].item()
                pad = data['Pad'][row].item()
                # checks is search has been run
                if len(newvalues) > 0:
                    # takes info from seach data
                    part = newvalues[row[0]][0]
                    pad = newvalues[row[0]][1]
                    # searches for matching data in main dataset and returns the proper row number
                    for i in range(len(data.values.tolist())):
                        if part == data['Part'][i] and pad == data['Pad'][i]:
                            part = data['Part'][i]
                            pad = data['Pad'][i]
                            c_row1 = i
                else:
                    c_row1 = values['Ftable1'][-1]
                name = ("%s-%s"%(part,pad))
                #remove old points to save memory
                plotgerber(window1['fig_cv'].TKCanvas, fig, ax, window1['tool_bar'].TKCanvas,c_row1,p_row1, xCords, yCords,name,textarr1,color)
                p_row1 = c_row1

        elif event == 'Ftable2+LEFT CLICK+':
            row = values['Ftable2']
            color = 'k*'
            if len(row) != 0:
                part = data['Part'][row].item()
                pad = data['Pad'][row].item()
                print(part)
                #checks is search has been run
                if len(newvalues) > 0:
                    # takes info from seach data
                    part = newvalues[row[0]][0]
                    pad = newvalues[row[0]][1]
                    # searches for matching data in main dataset and returns the proper row number
                    for i in range(len(data.values.tolist())):
                        if part == data['Part'][i] and pad == data['Pad'][i]:
                            part = data['Part'][i]
                            pad = data['Pad'][i]
                            c_row2 = i
                else:
                    c_row2 = values['Ftable2'][-1]
                name = ("%s-%s"%(part,pad))
                #remove old points to save memory
                plotgerber(window1['fig_cv'].TKCanvas, fig, ax, window1['tool_bar'].TKCanvas,c_row2,p_row2, xCords, yCords,name,textarr2,color)
                p_row2 = c_row2

        elif event == 'Search':
            if values['data'] != '':
                search = values['data']
                newvalues = [x for x in data.values.tolist() if search in x]
                print(newvalues)
                window1['Ftable1'].update(newvalues)
                window1['Ftable2'].update(newvalues)
            elif values['data'] == '':
                newvalues = []
                window1['Ftable1'].update(data.values.tolist())
                window1['Ftable2'].update(data.values.tolist())

        elif event == 'Link':
            row1 = values['Ftable1']
            row2 = values['Ftable2']
            flagarr1 = []
            flagarr2 = []
            if len(row1) != 0 and len(row2) != 0:
                part1 = data['Part'][row1[0]]
                pad1 = data['Pad'][row1[0]]
                part2 = data['Part'][row2[0]]
                pad2 = data['Pad'][row2[0]]
                if len(newvalues) > 0:
                    # takes info from seach data
                    part1 = newvalues[row1[0]][0]
                    pad1 = newvalues[row1[0]][1]
                    part2 = newvalues[row2[0]][0]
                    pad2 = newvalues[row2[0]][1]
                    # searches for matching data in main dataset and returns the proper row number
                    for i in range(len(data.values.tolist())):
                        if part1 == data['Part'][i] and pad1 == data['Pad'][i]:
                            part1 = data['Part'][i]
                            pad1 = data['Pad'][i]
                            row1 = i
                    for i in range(len(data.values.tolist())):
                        if part2 == data['Part'][i] and pad2 == data['Pad'][i]:
                            part2 = data['Part'][i]
                            pad2 = data['Pad'][i]
                            row2 = i

                name1 = ("%s-%s<>%s-%s P" % (part1, pad1,part2,pad2))
                name2 = ("%s-%s<>%s-%s G" % (part1, pad1,part2,pad2))

                if data['Flags'][row1[0]] != "":
                    flagarr1 += data['Flags Data'][row1[0]].getList()

                if data['Flags'][row2[0]] != "":
                    flagarr1 += data['Flags Data'][row2[0]].getList()

                flagarr1.append(name1)
                flagarr2.append(name2)

                for i in range(len(flagarr1)):
                    if tempstring == "":
                        tempstring = flagarr1[i]
                    else:
                        tempstring = tempstring + "," + flagarr1[i]

                data.loc[row1, 'Flags'] = tempstring
                tempstring = ""

                for i in range(len(flagarr2)):
                    tempstring += flagarr2[i]
                data.loc[row2, 'Flags'] = tempstring
                tempstring = ""

                data.loc[row1, 'Flags Data'] = Fake(flagarr1)
                data.loc[row2, 'Flags Data'] = Fake(flagarr2)

                #todo fix search function so it doesnt reset when applying a flag
                window1['Ftable1'].update(data.values.tolist())
                window1['Ftable2'].update(data.values.tolist())
        elif event == 'Edit Flags' and not flagEditor:
            row1 = values['Ftable1']
            row2 = values['Ftable2']
            if len(row1) != 0 and len(row2) != 0 and data['Flags'][row2[0]] != "" and data['Flags'][row1[0]] != "":
                flagEditor,P1Class,P2Class = makeEditor(data,row1,row2)
                P1Class.setRow(row1)
                P2Class.setRow(row2)

        elif event == 'Table 1 Delete':
            row1 = values['P1table']
            P1Class.delete(row1[0])
            data.loc[P1Class.getRow(), 'Flags Data'] = P1Class
            for i in range(len(P1Class.getList())):
                if tempstring == "":
                    tempstring = P1Class.getList()[i]
                else:
                    tempstring = tempstring + "," + P1Class.getList()[i]
            data.loc[P1Class.getRow(), 'Flags'] = tempstring
            tempstring = ""
            flagEditor['P1table'].update(P1Class.getList())
            window1['Ftable1'].update(data.values.tolist())
            window1['Ftable2'].update(data.values.tolist())

        elif event == 'Table 2 Delete':
            row2 = values['P2table']
            P2Class.delete(row2[0])
            data.loc[P2Class.getRow(), 'Flags Data'] = P2Class
            for i in range(len(P2Class.getList())):
                if tempstring == "":
                    tempstring = P2Class.getList()[i]
                else:
                    tempstring = tempstring + "," + P2Class.getList()[i]
            data.loc[P2Class.getRow(), 'Flags'] = tempstring
            tempstring = ""
            flagEditor['P2table'].update(P2Class.getList())
            window1['Ftable1'].update(data.values.tolist())
            window1['Ftable2'].update(data.values.tolist())

            """                                    
            The Plan:
            1) create new window / expand old one
            2) duplicate lists
            3) select two points to create probe point? / link?
            4) create way to specify power and ground point
            4b) maybe create do not touch pins???? might not need to since machine will only probe selected points????
            5) Original window should be able to specify ground and power pins
            6) may need to create a test all??? maybe operator needs to specify pins to test? or is provided a general config file
            7) create a way to output / load a config file should be easy as it will just re-read the pandas db
            """


if __name__ == '__main__':
    df = pandas.read_csv("output.csv")
    df.insert(4,"Flags","")
    df.insert(5,"Flags Data","")
    print(df)
    UI(df)

