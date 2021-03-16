import PySimpleGUI as sg
import time, random

contents = [[0, 'Temperature', 0], [1, 'Pressure', 0]]
layout = [[sg.Table(values=contents,
                    headings=['ID', 'Sensor', 'Reading'],
                    key='table',
                    enable_events=True)],
          [sg.T('Selected Row: None ', key='sr')],
          [sg.Button('Delete Row')]]

window = sg.Window('', layout=layout)

timer = 0
selected_row = None


def update_table():
    window.Element('table').Update(values=contents)
    window.Element('sr').Update('Selected Row: %s' % selected_row)

    # need something like this to keep same row selected (highlighted)
    # if selected_row:
    #     window.Element('table').Update(selected_row=selected_row)


while True:
    e, v = window.Read(timeout=100)

    if e == 'None' or e is None:
        break

    elif e == 'table':
        selected_row = v['table'][0]
        print('selected row:', selected_row)
        window.Element('sr').Update('Selected Row: %s' % selected_row)

        # Create new window with row_colors changed
        layout = [[sg.Table(values=contents,
                            headings=['ID', 'Sensor', 'Reading'],
                            key='table',
                            row_colors=((selected_row, 'light blue'),),
                            enable_events=True)],
                  [sg.T('Selected Row: None ', key='sr')],
                  [sg.Button('Delete Row')]]

        window.Close()
        window = sg.Window('', layout=layout)

    elif e == 'Delete Row':
        if selected_row is not None:
            contents.pop(selected_row)
            selected_row = None
            update_table()

    # run every 2 seconds
    if time.time() - timer >= 2:
        timer = time.time()
        for item in contents:
            item[2] = random.randint(1, 101)
        update_table()

window.Close()