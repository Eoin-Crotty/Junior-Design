import matplotlib.pyplot as plt
import pandas
import plotly.express as px
import numpy as np
from mpldatacursor import datacursor
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

def plotgerber(canvas, fig,ax,canvas_toolbar,c_row,p_row,xCords,yCords,name,textarr):

    if p_row is not None:
        ax.plot(xCords[p_row],yCords[p_row],marker = 'o', color = 'tab:blue')
    if c_row is not None:
        ax.plot(xCords[c_row],yCords[c_row],'r*')
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

def UI(data):

    gerber_layout = [
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
        [
            sg.Table(key='table',
                     values=data.values.tolist(),
                     headings=data.columns.tolist(),
                     display_row_numbers=False,
                     auto_size_columns=False,
                     enable_events= True,
                     num_rows=min(25, len(data)))],
        [sg.In(size=(25, 1), enable_events=True, key='flag_box'),
         sg.Button('Add Flag')],
        ]


    layout = [
        [
            sg.Column(data_Layout),
            sg.VSeparator(),
            sg.Column(gerber_layout)
        ]
    ]

    window = sg.Window('Gerber View', layout,finalize=True)
    window['table'].bind('<Button-1>','+LEFT CLICK+')

    xCords = data['X Cord'].tolist()
    yCords = (data['Y Cord']*-1).tolist()
    fig, ax = plt.subplots()
    ax.scatter(xCords, yCords)
    DPI = fig.get_dpi()
    fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))

    p_row = 0
    c_row = 0
    textarr = []

    while True:
        event, values = window.read()
        print(event,values)

        if event == sg.WIN_CLOSED:
            break

        elif event == 'table+LEFT CLICK+':
            row = values['table']

            if len(row) != 0:
                c_row = values['table'][-1]
                part = data['Part'][row].item()
                pad = data['Pad'][row].item()
                name = ("%s-%s"%(part,pad))
                #remove old points to save memory
                plotgerber(window['fig_cv'].TKCanvas, fig, ax, window['tool_bar'].TKCanvas,c_row,p_row, xCords, yCords,name,textarr)
                p_row = c_row

        elif event == 'Search':
            if values['data'] != '':
                search = values['data']
                newvalues = [x for x in data.values.tolist() if search in x]
                window['table'].update(newvalues)
            elif values['data'] == '':
                window['table'].update(data.values.tolist())

        elif event == 'Add Flag':
            #todo add default flags / linkable flags
            flag = values['flag_box']
            row = values['table']
            if len(row) != 0:
                data.loc[row,'Flags'] = flag
                window['table'].update(data.values.tolist())
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
    print(df)
    UI(df)

