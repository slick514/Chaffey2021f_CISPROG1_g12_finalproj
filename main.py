'''
Guidance found in flight_reservation_system.docx, provided
Refer to guidance for table and text formatting
TODO: User Functionality:

    Rules (CONSTANTS):
    1st class fare is $500
    Coach fare is $199
    If passenger is under 7 or 65+, 20% discount

    Establish an "exit/return" sentinel so that the attendant can back out of a menu
        if they need to
    Establish a quit sentinel so that the attendant can quit at any point.
    TODO: Design Interface:
        Print welcome & info messages
        Print main menu options
        Sanitize user input
        Option: Make a reservation
            TODO: Option to make a new first class or coach reservation
                NOTE: Only 8 seats are available in first class
                NOTE: Only 40 seats are available in coach
                TODO: If the reservation attendant picks first class or coach reservation,
                    TODO: Prompt attendant for the location of the desired seat
                        TODO: Prompt for row
                        TODO: Prompt for seat
                        TODO: If not available, it will be refused
                            TODO: Re-prompt for seat and start process again.
                    TODO: Prompt attendant for the name of the person taking the flight.
                        TODO: If seat is available:
                            TODO: Prompt attendant for sales-tax
                            TODO: Calculate cost of the ticket
                                TODO: Add base ticket price - discounts + sales tax
                            TODO: Prompt user for amount given
                            TODO: If user provides amount equal or greater than cost:
                                TODO: User is assigned a ticket
                                TODO: Change is provided, if needed.
                                    TODO: Determine optimal change
                                    TODO: Print change
                            TODO: If user provides insufficient amount:
                                TODO: Transaction is cancelled
                                TODO: fall back to options menu
        Option: change an existing reservation
            NOTE: Ensure data is not corrupted by wating for both seats before changing anything
            TODO: Prompt for the seat to change:
                TODO: Prompt for row
                TODO: Prompt for seat
                TODO: If seat is not booked:
                    TODO: re-prompt for seat
            TODO: Book previous passenger to a new seat
                TODO: If a new seat is desired:
                    TODO: Prompt for new row
                    TODO: Prompt for old row
                    TODO: If seat is taken:
                        TODO: Reprompt for new seat
            TODO: Old seat is set to open
            TODO: If a new seat was chosen
                TODO: New seat is reserved
        Option: print the listing of current seats reservations in table form
            TODO: the system will print in an orderly manner all the seats available in each compartment and the list of
                seats that are taken with the individual that has reserved the seat
            TODO: If all seats are taken a message is displayed stating, no new reservations can be made
            TODO: If the person’s name is longer than 12 characters you will only display the first 12 characters
                Note: the entire name should be in the array, you only to reduce the length of text during the print
                function for neatness.
        quit

'''
import enum

MAIN_MENU_HEADER = "MAIN MENU"
MAIN_MENU_PROMPT = "Please choose an option from the menu:"
BAR_CHAR = "="
WELCOME_TEXT = "Hello! Welcome to Chaffey Airlines!"
INFO_TEXT = "Our Cool Project v1.0, by Justin Gries & Christian Flores"
FIRST_CLASS_FARE = 500.00
COACH_FARE = 199.00
DISCOUNT_RATE = .20
DISCOUNT_LOW_AGE = 6
DISCOUNT_HIGH_AGE = 65
HEADER_LENGTH = 80
RETURN_CHOICE = 'R"'
QUIT_CHOICE = 'Q'

class MainChoices(enum.Enum):
    make_new_reservation = ["Make (N)ew Reservation", 'N']
    change_existing_reservation = ["(C)hange Existing Reservation", 'C']
    print = ["(P)rint Reservations", 'P']
    quit = ["(Q)uit", 'Q']
    
'''
    "Main" function of the reservation system: (See guidance file and pseudo-code for info)
'''


def print_main_menu():
    print(f'{MAIN_MENU_HEADER:}')
    print(f'{MAIN_MENU_PROMPT}')
    for member in MainChoices:
        print(f'{member.value[0]}')
    print(end=":")


def prompt_for_choices():
    validated_choice: str = ''
    while validated_choice == '':
        print_main_menu()
        choice = input()
        for member in MainChoices:
            if member.value[1].upper() == choice[0].upper():
                validated_choice = member.value[1]
                break;
        if validated_choice == '':
            print(f'\nValue, \'{choice}\' is not a valid choice')
            print("Please Choose again\n")
    return validated_choice


def make_bars(text=""):
    bars = ""
    str_len = HEADER_LENGTH if text == "" else int((HEADER_LENGTH - len(text)) / 2)

    for i in range(0, str_len):
        bars += BAR_CHAR
    if str_len % 2 == 0:
        bars.rstrip(bars[-1])
    return bars


def print_header():
    welcome_bars = make_bars(WELCOME_TEXT)
    info_bars = make_bars(INFO_TEXT)
    print(make_bars())
    print(f'{welcome_bars} {WELCOME_TEXT} {welcome_bars}')
    print(make_bars())
    print(f'{info_bars} {INFO_TEXT} {info_bars}')
    print(make_bars())


def run_reservation_system_pos():
    print_header()
    choice = prompt_for_choices()
    print(f'Choice was {choice}')


if __name__ == '__main__':
    print("start")
    run_reservation_system_pos()
    print("end")
