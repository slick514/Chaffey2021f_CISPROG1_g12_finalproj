import abc
import os

import mainmenu

NEWLINE = os.linesep
'''
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
            NOTE: Ensure data is not corrupted, by waiting for both seats before changing anything
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

MAIN_MENU_PROMPT = "Please choose an option from the main menu:"
CHOICE_QUIT = 'Q'
CHOICE_NEW_BOOKING = 'N'
CHOICE_CHANGE_BOOKING = 'C'
CHOICE_PRINT_BOOKINGS = 'P'
CHOICE_RETURN = 'R'

FIRST_CLASS_STR = "FIRST CLASS"
FIRST_CLASS_SEAT_CHOICES = ['A', 'B']
FIRST_CLASS_ROW_SIZE = 4
COACH_STR = "COACH"
COACH_SEAT_CHOICES = ['A', 'B', 'C', 'D']
COACH_ROW_SIZE = 10
FIRST_CLASS_FARE = 500.00
COACH_FARE = 199.00
DISCOUNT_RATE = .20
DISCOUNT_LOW_AGE = 6
DISCOUNT_HIGH_AGE = 65
MAX_NAME_DISPLAY_LEN = 12
OPEN_SEAT_NAME = "OPEN"
PRINT_HEADER_TEXT = "SEATING ASSIGNMENTS"
BAR_CHAR = "="
CELL_SEPARATOR = "|"
CELL_SPACING = " "
INNER_CELL_WIDTH = MAX_NAME_DISPLAY_LEN + 2 * len(CELL_SPACING)
OUTER_CELL_WIDTH = INNER_CELL_WIDTH + 2 * len(CELL_SEPARATOR)
SUBHEADER_WIDTH = 2 * OUTER_CELL_WIDTH
HEADER_WIDTH = 4 * OUTER_CELL_WIDTH


def build_header_string(width, text=""):

    bar = ""
    bar_len = width if text == "" else int((width - len(text)) / 2)

    for i in range(0, bar_len):
        bar += BAR_CHAR

    header = f'{bar} {text} {bar}' if text != "" else bar
    header_len = len(header)
    if header_len != width:
        while len(header) > width:
            header = header.rstrip(header[-1])
        while len(header) < width:
            header += BAR_CHAR
    return header


def print_cell(name=OPEN_SEAT_NAME):
    gap = MAX_NAME_DISPLAY_LEN - len(name)
    data_str = ""
    if gap < 0:
        data_str = slice(data_str, 0, MAX_NAME_DISPLAY_LEN)
    else:
        data_str = f'{CELL_SPACING}{name}{CELL_SPACING}'
    flipflop = True
    while len(data_str) < INNER_CELL_WIDTH:
        data_str = data_str + " " if flipflop else " " + data_str
        flipflop = not flipflop
    print(f'{CELL_SEPARATOR}{data_str}{CELL_SEPARATOR}', end="")


def generate_keys(choices):
    '''
    :param choices: a list of lists is expected
    :return: will return a list comprised of the first items in each list contained in choices
    '''
    keys = []
    for choice in choices:
        keys += choice[0]
    return keys


class View(metaclass=abc.ABCMeta):
    '''
    An abstract/interface class that will enforce method implementation on child classes
    '''

    @abc.abstractmethod
    def do_view(self, text="") -> str:
        '''
        Display a view to the user
        :param text: The text to display, if it is provided
        :return: the user's input in response to the view
        '''
        pass

    @abc.abstractmethod
    def validate(self, text="") -> bool:
        '''
        :param text: The text to be validated
        :return: whether or not the text is valid for the expected view
        '''
        pass

    @abc.abstractmethod
    def print_reprompt(self, invalid_input=""):
        '''
        Prompts the user for new input
        :param invalid_input:
        :return: nothing
        '''
        pass


class Controller(metaclass=abc.ABCMeta):

    def __init__(self):
        self.__model = None

    @abc.abstractmethod
    def do(self, model):
        '''
        :param model: The model to use for this controller
        :return: the next controller that needs to be used
        '''
        self.__model = model

    def get_model(self):
        return self.__model

class Model:
    def __init__(self):
        # this will be an array of arrays in the form rows[seats[]]
        self.__reservations = self.create_empty_model()

    @staticmethod
    def create_empty_model():
        reservation_data = {FIRST_CLASS_STR: {}, COACH_STR: {}}
        for row in range(0, FIRST_CLASS_ROW_SIZE):
            reservation_data[FIRST_CLASS_STR][row] = {}
            for seat in FIRST_CLASS_SEAT_CHOICES:
                reservation_data[FIRST_CLASS_STR][row][seat] = OPEN_SEAT_NAME
        for row in range(0, COACH_ROW_SIZE):
            reservation_data[COACH_STR][row] = {}
            for seat in COACH_SEAT_CHOICES:
                reservation_data[COACH_STR][row][seat] = OPEN_SEAT_NAME
        return reservation_data

    def add_reservation(self, type, row, seat, customer_name):
        self.__reservations[type][row][seat] = customer_name
        pass

    def delete_reservation(self, type, row, seat):
        self.__reservations[type][row][seat] = OPEN_SEAT_NAME
        pass

    def get_row(self, type, row):
        return self.__reservations[type][row]

    def get_passenger(self, type, row, seat) -> str:
        return self.__reservations[type][row][seat]

    def print_grid(self):
        print(f'{build_header_string(HEADER_WIDTH, PRINT_HEADER_TEXT)}')
        self.print_grid_section(FIRST_CLASS_STR)
        print(f'{build_header_string(SUBHEADER_WIDTH)}')
        self.print_grid_section(COACH_STR)
        print(f'{build_header_string(HEADER_WIDTH)}')

    def print_grid_section(self, type):
        print(build_header_string(SUBHEADER_WIDTH, type))
        rows = self.__reservations[type]
        for row in rows.keys():
            for seat in rows[row].keys():
                print_cell(self.__reservations[type][row][seat])
            print()
        pass


class MainView(View):
    choices = [
        [CHOICE_NEW_BOOKING, "(N)ew Reservation"],
        [CHOICE_CHANGE_BOOKING, "(C)hange Reservation"],
        [CHOICE_PRINT_BOOKINGS, "(P)rint Reservation Chart"],
        [CHOICE_QUIT, "(Q)uit"]
    ]

    keys = generate_keys(choices)

    def do_view(self, text="") -> str:
        self.print_menu()
        return input()

    def print_menu(self):
        print(f'{NEWLINE}Please choose from the following options:')
        for choice in self.choices:
            print(f'\t{choice[1]}')
        print(":", end="")

    def validate(self, text="") -> bool:
        text = text.upper()
        result = text in MainView.keys
        return result

    def print_reprompt(self, invalid_input=""):
        print(f'{NEWLINE}That input "{invalid_input}" is invalid.')
        print(f'Please try again.{NEWLINE}')


class NewReservationView(View):

    def do_view(self, text="") -> str:
        # TODO:
        pass

    def validate(self, text="") -> bool:
        # TODO:
        pass

    def print_reprompt(self, invalid_input=""):
        # TODO:
        pass


class ChangeReservationView(View):

    def do_view(self, text="") -> str:
        # TODO:
        pass

    def validate(self, text="") -> bool:
        # TODO:
        pass

    def print_reprompt(self, invalid_input=""):
        # TODO:
        pass


class RowView(View):

    def do_view(self, text="") -> str:
        # TODO:
        pass

    def validate(self, text="") -> bool:
        # TODO:
        pass

    def print_reprompt(self, invalid_input=""):
        # TODO:
        pass


class NameView(View):

    def do_view(self, text="") -> str:
        # TODO:
        pass

    def validate(self, text="") -> bool:
        # TODO:
        pass

    def print_reprompt(self, invalid_input=""):
        # TODO:
        pass


class ColView(View):

    def do_view(self, text="") -> str:
        # TODO:
        pass

    def validate(self, text="") -> bool:
        # TODO:
        pass

    def print_reprompt(self, invalid_input=""):
        # TODO:
        pass


class BookingView(View):

    def do_view(self, text="") -> str:
        # TODO:
        pass

    def validate(self, text="") -> bool:
        # TODO:
        pass

    def print_reprompt(self, invalid_input=""):
        # TODO:
        pass


class BookingChangeController(Controller):
    # default constructor
    def __init__(self):
        super().__init__()
        self.view: View = BookingView()

    def do(self, model):
        super().do(model)
        print("doing booking change")
        return MainController()
        # TODO:


class PrintController(Controller):
    # default constructor
    def __init__(self):
        super().__init__()

    def do(self, model):
        super().do(model)
        super().get_model().print_grid()
        return MainController()


class NewBookingController(Controller):
    def __init__(self):
        super().__init__()
        self.row = -1
        self.col = -1
        self.name = ""

    def set_row(self, row):
        self.row = row

    def set_col(self, col):
        self.col = col

    def set_name(self, name):
        self.name = name

    def do(self, model):
        super().do(model)

        col_view: View = ColView()
        name_view: View = NameView()

        while True:
            response = col_view.do_view()
            valid = col_view.validate(response)
            if not valid:
                col_view.print_reprompt(response)
                continue
            elif response[0].upper() == CHOICE_RETURN:
                return MainController()
            else:
                self.col = int(response)
                break
        while True:
            response = name_view.do_view()
            valid = name_view.validate(response)
            if not valid:
                name_view.print_reprompt(response)
                continue
            elif response[0].upper() == CHOICE_RETURN:
                return MainController()
            else:
                self.set_name(response)
                break

        if not (self.get_row_from_user()
                and self.get_col_from_user()
                and self.get_name_from_user()):
            return MainController()
        super().get_model().add_reservation(self.row, self.col, self.name)
        return MainController()

    def get_from_user(self, view, func) -> bool:
        while True:
            response = view.do_view()
            valid = view.validate(response)
            if not valid:
                view.print_reprompt(response)
                continue
            elif response[0].upper() == CHOICE_RETURN:
                return False
            else:
                func(response)
                return True
    def get_row_from_user(self) -> bool:
        view: View = RowView()
        func = lambda val: self.set_row(val)
        return self.get_from_user(view, func)

    def get_col_from_user(self) -> bool:
        view: View = ColView()
        func = lambda val: self.set_col(val)
        return self.get_from_user(view, func)

    def get_name_from_user(self) -> bool:
        view: View = NameView()
        func = lambda val: self.set_name(val)
        return self.get_from_user(view, func)


class MainController(Controller):

    def __init__(self):
        super().__init__()

    def do(self, model):
        view: View = MainView()
        while True:
            response = ''
            while True:
                response = view.do_view().upper()[0]
                valid = view.validate(response)
                if not valid:
                    view.print_reprompt(response)
                else:
                    break
            if response == CHOICE_QUIT:
                quit()
            elif response == CHOICE_CHANGE_BOOKING:
                return BookingChangeController()
            elif response == CHOICE_PRINT_BOOKINGS:
                return PrintController()
            elif response == CHOICE_NEW_BOOKING:
                return NewBookingController()


'''
class MainMenu:
    class MainChoices():
        def handle_reservation(self):
            super().handle_reservation()

        choices = {
            'N': ["Make (N)ew Reservation", super().handle_reservation],
            'C': ["(Change Reservation", super().change_reservation],
            'P': ["(P)rint Reservations", super().print_reservations],
            'Q': [""]
        };
        make_new_reservation = ["Make (N)ew Reservation", 'N', MainMenu.handle_reservation]
        change_existing_reservation = ["(C)hange Existing Reservation", 'C', MainMenu.change_reservation]
        print = ["(P)rint Reservations", 'P', MainMenu.print_reservations]
        quit = ["(Q)uit", 'Q', quit]

        @staticmethod
        def do_choice(choice):
            for member in MainMenu.MainChoices:
                if member.value[1].lower() == choice.lower():
                    member.value[2]()
                    return
            raise ValueError(f'Choice "{choice}" not found in MainChoices')

'''
#        "Main" function of the reservation system: (See guidance file and pseudo-code for info)
'''

    @staticmethod
    def print_main_menu():
        print(f'{MAIN_MENU_PROMPT}')
        for member in MainMenu.MainChoices:
            print(f'\t{member.value[0]}')
        print("\t", end=":")

    @staticmethod
    def prompt_for_choices():
        validated_choice: str = ''
        while validated_choice == '':
            MainMenu.print_main_menu()
            choice = input()
            for member in MainMenu.MainChoices:
                if member.value[1].upper() == choice[0].upper():
                    validated_choice = member.value[1]
                    break
            if validated_choice == '':
                print(f'\nValue, \'{choice[0].upper()}\' is not a valid choice')
                print("Please Choose again\n")
        return validated_choice

    # default constructor
    def __init__(self):
        self.functionality_handler = MainFunctionality()
        while True:
            choice = MainMenu.prompt_for_choices()
            MainMenu.MainChoices.do_choice(choice)
'''
