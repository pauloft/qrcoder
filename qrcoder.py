import validators
import qrcode
import PySimpleGUI as sg
from datetime import date
from pathlib import Path

INPUT_WIDTH = 25

layout = [
    [sg.T('Enter the URL to QR Code', s=20, justification='r'), sg.Push(),
     sg.I(k='-URL-', size=(2*INPUT_WIDTH, 1))],
    [sg.T("Output Folder:", s=20, justification='r'),
            sg.I(k='-OUTPUT_FOLDER-'), sg.FolderBrowse(initial_folder=Path.cwd())],
    [sg.Exit('Exit', s=(16,1)), sg.Push(), sg.B('Create QR Image', k='-QR-', s=(16,1))],
    [sg.HorizontalSeparator()],
    [sg.T(f"Created by Bentley Thompson for PRAC-tical purposes. Copyright \u00A9 {date.today().strftime('%Y')}")],
    [sg.Sizegrip()]
]

# create main window
window = sg.Window("QR Coder",
                   layout=layout,
                   margins=(0, 0),
                   use_custom_titlebar=True,
                   resizable=True,
                   keep_on_top=True,
                   finalize=True
                   )
window.set_min_size(window.size)

# Event loop
while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Exit'):
        break

    elif event == '-QR-':
        url = values['-URL-']
        if validators.url(url):
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=4
            )
            qr.add_data(url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            pathstr = Path(values['-OUTPUT_FOLDER-'], "myQR_image.png")
            path = sg.popup_get_file('Confirm the path to save the file', 'Save QR Code', default_path=pathstr)
            if Path(path):
                img.save(path)
        # clear the URL input
        window['-URL-'].update('') 

window.close()
