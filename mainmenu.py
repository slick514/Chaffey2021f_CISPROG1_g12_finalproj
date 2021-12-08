import abc
import os

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

MAIN_MENU_PROMPT = "Please choose an option from the main menu:"
CHOICE_QUIT = 'Q'
CHOICE_NEW_BOOKING = 'N'
CHOICE_CHANGE_BOOKING = 'C'
CHOICE_PRINT_BOOKINGS = 'P'

FIRST_CLASS_FARE = 500.00
COACH_FARE = 199.00
DISCOUNT_RATE = .20
DISCOUNT_LOW_AGE = 6
DISCOUNT_HIGH_AGE = 65


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
    def do_view(self, text=""):
        '''
        Display a view to the user
        :param text: The text to display, if it is provided
        :return: the user's input in response to the view
        '''
        pass

    @abc.abstractmethod
    def validate(self, text=""):
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

class MainView(View):
    choices = [
        [CHOICE_NEW_BOOKING, "(N)ew Reservation"],
        [CHOICE_CHANGE_BOOKING, "(C)hange Reservation"],
        [CHOICE_PRINT_BOOKINGS, "(P)rint Reservation Chart"],
        [CHOICE_QUIT, "(Q)uit"]
    ]

    keys = generate_keys(choices)

    def do_view(self, text=""):
        self.print_menu()
        return input()

    def print_menu(self):
        print(f'{NEWLINE}Please choose from the following options:')
        for choice in self.choices:
            print(f'\t{choice[1]}')
        print(":", end="")

    def validate(self, text=""):
        text = text.upper()
        result = text in MainView.keys
        return result

    def print_reprompt(self, invalid_input=""):
        print(f'{NEWLINE}That input "{invalid_input}" is invalid.')
        print(f'Please try again.{NEWLINE}')


class NewReservationView(View):
    pass


class ChangeReservationView(View):
    pass


class PrintReservationsView(View):
    pass


class Model:
    # default constructor
    def __init__(self):
        # this will be a map of maps in the form {row_number: {seat_number: passenger_name}}
        self.reservations = {}


class Controller:

    def begin(self):
        while True:
            response = self.view.do_view().upper()[0]
            valid = self.view.validate(response)
            if not valid:
                self.view.print_reprompt(response)
                continue
            if response == CHOICE_QUIT:
                quit()

    # default constructor
    def __init__(self):
        self.model = Model()
        self.view: View = MainView()
        self.begin()


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
