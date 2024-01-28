import PySimpleGUI as sg
# import your script
# import your_script
from PyClime import PyClime # import backend

# defines our global instance of PyClime class
pyclime = PyClime()
pyclime.set_env_com()
pyclime.set_ps_com()
# Define the window's contents
layout = [[sg.Text("Low Voltage Control")], 
          [sg.Button('Lov Voltage ON', key='-BTN1-', enable_events=True)], 
          [sg.Button('Low Voltage Off', key='-BTN2-', enable_events=True)]]

# Create the window
window = sg.Window('Toggle Buttons', layout, size=(300, 100),finalize=True)

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-BTN1-':
        # Call function from your script when Button 1 is clicked
        # your_script.function_for_button1()
        window['-BTN2-'].update(disabled=False)
        window['-BTN1-'].update(disabled=True)
        pyclime.lv_on(True)
    elif event == '-BTN2-':
        # Call function from your script when Button 2 is clicked
        # your_script.function_for_button2()
        window['-BTN1-'].update(disabled=False)
        window['-BTN2-'].update(disabled=True)
        pyclime.lv_on(False)

# Finish up by removing from the screen
window.close()