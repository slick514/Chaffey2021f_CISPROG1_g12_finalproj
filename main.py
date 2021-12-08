'''
Guidance found in flight_reservation_system.docx, provided
Refer to guidance for table and text formatting
    Print Header
    Instantiate a MainMenu instance to handle main menu functionality
'''

import mainmenu
BAR_CHAR = "="
WELCOME_TEXT = "Hello! Welcome to Chaffey Airlines!"
INFO_TEXT = "Our Cool Project v1.0, by Justin Gries & Christian Flores"
HEADER_LENGTH = 80

def build_header_string(text=""):

    bar = ""
    bar_len = HEADER_LENGTH if text == "" else int((HEADER_LENGTH - len(text)) / 2)

    for i in range(0, bar_len):
        bar += BAR_CHAR

    header = f'{bar} {text} {bar}' if text != "" else bar
    header_len = len(header)
    if header_len != HEADER_LENGTH:
        while len(header) > HEADER_LENGTH:
            header = header.rstrip(header[-1])
        while len(header) < HEADER_LENGTH:
            header += BAR_CHAR
    return header


def print_header():
    print(build_header_string())
    print(build_header_string(text=WELCOME_TEXT))
    print(build_header_string())
    print(build_header_string(text=INFO_TEXT))
    print(build_header_string())


def run_reservation_system_pos():
    print_header()
    mainmenu.Controller()

if __name__ == '__main__':
    print("start")
    run_reservation_system_pos()
    print("end")
