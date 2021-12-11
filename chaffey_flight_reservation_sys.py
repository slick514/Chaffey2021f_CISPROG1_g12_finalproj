from abc import ABCMeta, abstractmethod
from enum import Enum
from math import ceil, floor
from os import linesep
from io import StringIO
from locale import currency, setlocale, LC_ALL

MAX_NAME_DISPLAY_LEN: int = 12
CELL_SEPARATOR: str = '|'
INNER_CELL_WIDTH: int = MAX_NAME_DISPLAY_LEN + 2
OUTER_CELL_WIDTH: int = INNER_CELL_WIDTH + 2 * len(CELL_SEPARATOR)

UNSET_INT = -1
EMPTY_STR: str = ""
SPACE: str = ' '
BAR_CHAR: str = '='
QUIT_CHAR: str = 'Q'
RETURN_TO_MAIN_CHAR: str = 'R'

DISCOUNT_LOW_AGE: int = 6
DISCOUNT_HIGH_AGE: int = 65
AGE_DISCOUNT: float = 0.2
MIN_AGE = 0
MAX_AGE = 130

SYSTEM_LOCALE = EMPTY_STR
setlocale(LC_ALL, SYSTEM_LOCALE)

WELCOME_TEXT = "Hello! Welcome to Chaffey Airlines!"
INFO_TEXT = "Our Cool Project v1.0, by Justin Gries & Christian Flores"
WELCOME_HEADER_LENGTH = 68
NUM_COACH_ROWS: int = 10
NUM_FC_ROWS: int = 4
NUM_COACH_SEATS_PER_ROW: int = 4
NUM_FC_SEATS_PER_ROW: int = 2
QUIT_GUIDANCE_TEXT: str = f"Enter '{QUIT_CHAR}' at any point to quit out of the application"
RETURN_GUIDANCE_TEXT: str = f"Enter '{RETURN_TO_MAIN_CHAR}' at any point to Return to the main menu"


def build_app_header_string(text="") -> str:
    bar = ""
    bar_len = WELCOME_HEADER_LENGTH if text == "" else int((WELCOME_HEADER_LENGTH - len(text)) / 2)

    for i in range(0, bar_len):
        bar += BAR_CHAR

    header = f'{bar} {text} {bar}' if text != "" else bar
    header_len = len(header)
    if header_len != WELCOME_HEADER_LENGTH:
        while len(header) > WELCOME_HEADER_LENGTH:
            header = header.rstrip(header[-1])
        while len(header) < WELCOME_HEADER_LENGTH:
            header += BAR_CHAR
    return header


def print_app_header():
    print(build_app_header_string())
    print(build_app_header_string(text=WELCOME_TEXT))
    print(build_app_header_string())
    print(build_app_header_string(text=INFO_TEXT))
    print(build_app_header_string())


def run_reservation_system_pos():
    print_app_header()
    model: SeatingStructure = SeatingStructure(fc_rows=NUM_FC_ROWS,
                                               coach_rows=NUM_COACH_ROWS,
                                               fc_seats=NUM_FC_SEATS_PER_ROW,
                                               coach_seats=NUM_COACH_SEATS_PER_ROW)
    controller: Controller = MainController()
    while controller is not None:
        controller = controller.do(model)


class MoneyManipulator(Enum):
    hundreds = 10000
    fifties = 5000
    twenties = 2000
    tens = 1000
    fives = 500
    dollars = 100
    quarters = 25
    dimes = 10
    nickles = 5
    pennies = 1

    @classmethod
    def make_change(cls, amount_cents: int, do_print: bool = False) -> dict:
        original_amt: int = amount_cents
        data = {}
        for member in cls:
            count: int = floor(amount_cents / member.value)
            amount_cents = amount_cents % member.value
            if count > 0:
                data[member] = count
        if do_print:
            cls.print_change(data, original_amount_cents=original_amt)
        return data

    @classmethod
    def print_change(cls, amounts: dict, original_amount_cents: int = 0):
        if len(amounts) == 0:
            print('No change necessary')
        else:
            if original_amount_cents > 0:
                print(f"Amount Returned: {cls.convert_cents_to_dollar_str(original_amount_cents)}")
            print("Change Dispensed:")
            longest_name: int = 0
            longest_amt: int = 0
            for amount in amounts.keys():
                longest_name = len(amount.get_name()) if len(amount.get_name()) > longest_name else longest_name
                longest_amt = len(str(amounts[amount])) if len(str(amounts[amount])) > longest_amt else longest_amt
            for member in cls:
                if member in amounts.keys():
                    name = member.name.capitalize()
                    value = amounts[member]
                    name_buffer: str = SPACE * (longest_name - len(name))
                    val_buffer: str = SPACE * (longest_amt - len(str(value)))
                    print(f"\t{name_buffer}{member.name.capitalize()}: {val_buffer}{amounts[member]}")

    def get_name(self) -> str:
        return self.name

    def get_value(self) -> int:
        return self.value

    @classmethod
    def convert_cents_to_dollar_str(cls, cents: int) -> str:
        return currency(cents / 100)


class Passenger:

    def __init__(self, name: str, age: int):

        self.__passenger_name: str = EMPTY_STR
        self.__age: int = -1
        self.__tax_rate = 0.0
        self.__set_data(name, age)

    def get_tax_rate(self) -> float:
        return self.__tax_rate

    def set_tax_rate(self, new_rate: float):
        self.__tax_rate = new_rate

    def get_name(self) -> str:
        return self.__passenger_name

    def __set_name(self, name: str):
        self.__validate_passenger_name(name)
        self.__passenger_name = name

    @staticmethod
    def __validate_passenger_name(name: str):
        if name == EMPTY_STR:
            raise Exception("Name is unspecified")
        else:
            for word in name.split(sep=SPACE):
                if not word.isalnum():
                    raise Exception(f"Name '{name}' contains invalid characters")

    def get_age(self) -> int:
        return self.__age

    def __set_age(self, age: int):
        self.__validate_age(age)
        self.__age = age

    @staticmethod
    def __validate_age(age):
        if age < MIN_AGE or age > MAX_AGE:
            raise Exception(f"Age, '{age}' is out of bounds ({MIN_AGE} to {MAX_AGE})")

    def get_discount_rate(self) -> float:
        age: int = self.get_age()
        return 0.0 if age in range(DISCOUNT_LOW_AGE, DISCOUNT_HIGH_AGE) else 0.2

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)
                and self.get_age() == other.get_age()
                and self.get_name() == other.get_name())

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        output: str = f"Passenger: Name={self.get_name()}; Age={self.get_age()}"
        return output

    def copy(self) -> 'Passenger':
        duplicate: Passenger = Passenger(name=self.get_name(), age=self.get_age())
        return duplicate

    def __set_data(self, name: str, age: int):
        errs: str = EMPTY_STR
        try:
            self.__set_name(name=name)
        except Exception as e:
            errs += f"{e}{linesep}"
        try:
            self.__set_age(age=age)
        except Exception as e:
            errs += f"{e}{linesep}"
        if errs != EMPTY_STR:
            errs = errs.rstrip(errs[-1])
            raise Exception(errs)


class Tier(Enum):
    first_class = ["First Class", 50000, 'F', "(F)irst Class"]
    coach = ["Coach", 19900, 'C', "(C)oach"]

    def get_tier_name(self) -> str:
        return self.value[0]

    def get_menu_display_text(self) -> str:
        return self.value[3]

    @classmethod
    def get_tier(cls, text: str) -> 'Tier':
        while True:
            if text != EMPTY_STR:
                text: str = text[0].upper()
                for member in cls:
                    if member.value[2] == text:
                        return member
                if text == RETURN_TO_MAIN_CHAR:
                    raise ReturnToMainMenu
                elif text == QUIT_CHAR:
                    raise QuitApplication
            raise Exception(f"'{text}' is not one of the available options")

    def get_tier_base_cost_cents(self) -> int:
        return self.value[1]


class Seat:
    NO_PASSENGER = None

    def __init__(self, seat_letter: str, row_number: int, tier: Tier):
        self.__seat_letter: str = seat_letter
        self.__row_number: int = row_number
        self.__tier: Tier = tier
        self.__passenger = self.NO_PASSENGER

    def is_taken(self) -> bool:
        return self.__passenger is not self.NO_PASSENGER

    def assign_passenger(self, passenger: Passenger):
        old_passenger: Passenger = self.get_passenger()
        if old_passenger == self.NO_PASSENGER:
            self.__passenger = passenger
        else:
            self.__raise_seat_taken_exception()

    def __raise_seat_taken_exception(self):
        name = self.__passenger.get_name()
        tier_name = self.get_tier().get_tier_name()
        row_number = self.get_row_number()
        seat_letter = self.get_seat_letter()
        msg = f"{tier_name} seat ;{row_number}-{seat_letter}; is already booked by {name}"
        raise Exception(msg)

    def remove_passenger(self):
        self.__passenger = self.NO_PASSENGER

    def get_row_number(self) -> int:
        return self.__row_number

    def get_seat_letter(self):
        return self.__seat_letter

    def get_tier(self) -> Tier:
        return self.__tier

    def get_price_dollars(self) -> float:
        return self.get_price_cents() / 100

    def get_price_cents(self, passenger=NO_PASSENGER) -> int:
        passenger: Passenger = self.get_passenger() if (passenger is self.NO_PASSENGER) else passenger
        self.__validate_passenger_existance(passenger)
        # validated_passenger: Passenger = passenger
        tier_price: int = self.get_tier().get_tier_base_cost_cents()
        discount_rate: float = passenger.get_discount_rate()
        tax_rate: float = passenger.get_tax_rate()
        passenger.set_tax_rate(tax_rate)
        total_price: int = floor((tier_price * (1 - discount_rate)) * (1 + tax_rate))
        return total_price

    def __validate_passenger_existance(self, passenger):
        if passenger == self.NO_PASSENGER:
            raise Exception("No Passenger supplied or found for price comparison")

    def compare_cost_cents(self, to_seat: 'Seat') -> int:
        self.__validate_seat_move_possible(to_seat)
        to_seat = to_seat.copy()
        to_seat_cost: int = to_seat.get_price_cents(self.get_passenger())
        return max(0, to_seat_cost - self.get_price_cents())

    def __validate_seat_move_possible(self, to_seat: 'Seat'):
        if to_seat.is_taken():
            raise Exception("That seat is already taken")
        if not self.is_taken():
            raise Exception("This seat is not presently booked")

    def copy(self) -> 'Seat':
        seat: Seat = Seat(row_number=self.get_row_number(), seat_letter=self.get_seat_letter(), tier=self.get_tier())
        seat.assign_passenger(self.get_passenger())
        return seat

    def __eq__(self, other) -> bool:
        return (type(self) == type(other)
                and self.get_seat_letter() == other.__get_letter()
                and self.get_row_number() == other.__get_number()
                and self.get_tier() == other.__get_tier())

    def get_passenger(self) -> Passenger:
        return self.__passenger

    def generate_seat_display(self) -> str:
        passenger = self.get_passenger()
        name: str = passenger.get_name()[0: MAX_NAME_DISPLAY_LEN] if (passenger is not None) else "-OPEN-"
        gap: float = (MAX_NAME_DISPLAY_LEN - len(name)) / 2
        front_gap: int = floor(gap)
        back_gap: int = ceil(gap)
        data_str = f"{front_gap * SPACE}{name}{back_gap * SPACE}"
        return f"{CELL_SEPARATOR} {data_str} {CELL_SEPARATOR}"

    def get_full_seat_description(self) -> str:
        rtn_str: str = f'Seat: {self.get_row_seat_str()}; '
        rtn_str += f'Passenger: {self.get_passenger().get_name() if self.is_taken() else "None"}; '
        rtn_str += f'Cost: {MoneyManipulator.convert_cents_to_dollar_str(self.get_price_cents())}'
        return rtn_str

    def get_row_seat_str(self) -> str:
        return f"{self.get_row_number()}-{self.get_seat_letter()}"


def make_dict_keys_str(items: dict):
    return f"({', '.join(map(str, items.keys()))})"


class SeatingStructure:
    UNINITIALIZED_INT = -1
    UNICODE_BASE: int = 65
    OPEN_SEAT_NAME: str = "OPEN"
    PRINT_HEADER_TEXT: str = "SEATING ASSIGNMENTS"
    INNER_CELL_WIDTH: int = MAX_NAME_DISPLAY_LEN + 2
    OUTER_CELL_WIDTH: int = INNER_CELL_WIDTH + 2 * len(CELL_SEPARATOR)

    def __init__(self, fc_rows, fc_seats, coach_rows, coach_seats):
        self.TOP_HEADER_TEXT: str = "SEATING DISPLAY"
        self.__structure: dict = {}
        self.__seating_options: dict = {}
        self.__row_options: dict = {}
        self.__header_width: int = coach_seats * self.OUTER_CELL_WIDTH
        self.__subheader_width: int = fc_seats * self.OUTER_CELL_WIDTH
        self.__side_marker_len: int = len(str(coach_rows)) + 1
        self.__title_bar_header: str = EMPTY_STR
        self.__tier_headers: dict = {}
        self.__seat_headers: dict = {}

        self.__populate_row_options(tier=Tier.coach, num_rows=coach_rows, num_seats=coach_seats)
        self.__populate_row_options(tier=Tier.first_class, num_rows=fc_rows, num_seats=fc_seats)
        for tier in Tier:
            self.__populate_section(tier)

    def __populate_row_options(self, tier: Tier, num_rows: int, num_seats: int):
        self.__row_options[tier] = list(range(1, num_rows + 1))
        self.__seating_options[tier] = list(map(chr, range(self.UNICODE_BASE, self.UNICODE_BASE + num_seats)))

    def set_seat(self, new_seat: Seat):
        self.__validate_seat_existence(new_seat)
        tier: Tier = new_seat.get_tier()
        row_number: int = new_seat.get_row_number()
        seat_letter: str = new_seat.get_seat_letter()
        self.__get_structure()[tier][row_number][seat_letter] = new_seat

    def __validate_seat_existence(self, new_seat):
        errs = EMPTY_STR
        tier: Tier = new_seat.get_tier()
        row_number = new_seat.get_row_number()
        seat_letter = new_seat.get_seat_letter()
        if row_number not in self.get_row_options(tier):
            range_first = self.get_row_options(tier)[0]
            range_last = self.get_row_options(tier)[-1]
            errs += f"Row number '{row_number}'-{tier.get_tier_name()} does not exist on this flight.{linesep}"
            errs += f"Rows in {tier.get_tier_name()} range from {range_first} to {range_last}.{linesep}"
        if seat_letter not in self.get_seat_options(tier):
            range_first = self.get_seat_options(tier)[0]
            range_last = self.get_seat_options(tier)[-1]
            errs += f"Seat letter '{seat_letter}'-({tier.get_tier_name()}) does not exist on this flight.{linesep}"
            errs += f"Seats in {tier.get_tier_name()} range from {range_first} to {range_last}.{linesep}"
        if errs != EMPTY_STR:
            errs = errs.rstrip(errs[-1])  # strip off linesep
            raise Exception(errs)

    def get_seat(self, tier: Tier, row_number: int, seat_letter: str) -> Seat:
        return self.__get_structure()[tier][row_number][seat_letter]

    def generate_chart(self) -> str:
        return self.__generate_printout()

    def get_row_options(self, tier: Tier) -> list:
        return self.__row_options[tier]

    def get_seat_options(self, tier: Tier) -> list:
        return self.__seating_options[tier]

    def __generate_printout(self) -> str:
        builder: StringIO = StringIO()
        builder.write(f"{self.__generate_top_bar_header()}{linesep}")
        for tier in Tier:
            builder.write(f"{self.__generate_tier_display(tier=tier)}{linesep}")
        builder.write(self.__generate_bottom_line())
        return builder.getvalue()

    def __generate_top_bar_header(self) -> str:
        return self.__generate_bar_header(width=self.__header_width,
                                          text=self.TOP_HEADER_TEXT,
                                          front_buffer_width=self.__side_marker_len)

    @classmethod
    def __generate_bar_header(cls,
                              width: int,
                              text: str = EMPTY_STR,
                              rear_buffer_width: int = 0,
                              front_buffer_width: int = 0) -> str:
        if text != EMPTY_STR:
            text = f"{SPACE}{text}{SPACE}"
        if len(text) > width:
            raise Exception(f"Cannot fit the text '{text}' within a header of length {width}")
        side_width: float = (width - len(text)) / 2
        first_bar_width: int = floor(side_width)
        last_bar_width: int = ceil(side_width)
        first_bar: str = first_bar_width * BAR_CHAR
        last_bar: str = last_bar_width * BAR_CHAR
        return f"{SPACE * front_buffer_width}{first_bar}{text}{last_bar}{SPACE * rear_buffer_width}"

    def __generate_tier_header(self, tier: Tier) -> str:
        width: int = len(self.get_seat_options(tier)) * OUTER_CELL_WIDTH
        return self.__generate_bar_header(width=width, text=tier.get_tier_name().upper())

    def __get_structure(self) -> dict:
        return self.__structure

    def __generate_tier_display(self, tier: Tier) -> str:
        builder: StringIO = StringIO()

        builder.write(f"{self.__generate_row_marker()}{self.__generate_tier_header(tier)}{linesep}")
        row_options: list = self.get_row_options(tier=tier)
        seat_options: list = self.get_seat_options(tier=tier)
        builder.write(f"{self.__generate_seat_headers(options=self.get_seat_options(tier=tier))}{linesep}")
        for row_number in row_options:
            builder.write(self.__generate_row_marker(row_number))
            for seat_letter in seat_options:
                seat: Seat = self.get_seat(tier=tier,
                                           row_number=row_number,
                                           seat_letter=seat_letter)
                builder.write(seat.generate_seat_display())
            if row_number != row_options[-1]:
                builder.write(linesep)
        return builder.getvalue()

    def __generate_row_marker(self, row_number: int = UNSET_INT) -> str:
        marker_len: int = self.__side_marker_len
        number_len: int = len(str(row_number))
        diff: int = marker_len if row_number == UNSET_INT else marker_len - number_len
        if diff < 0:
            raise Exception(f"Row-marker '{row_number}' does not fit into a {marker_len}-character string")
        if row_number == UNSET_INT:
            return SPACE * marker_len
        else:
            return f"{SPACE * (diff - 1)}{row_number} "

    def __generate_bottom_line(self) -> str:
        return self.__generate_bar_header(width=self.__header_width,
                                          front_buffer_width=self.__side_marker_len)

    def __populate_section(self, tier: Tier):
        structure: dict = self.__get_structure()
        tier_data: dict = {}
        structure[tier] = tier_data
        for row_number in self.get_row_options(tier):
            new_row: dict = {}
            structure[tier][row_number] = new_row
            for seat_letter in self.get_seat_options(tier):
                seat: Seat = Seat(row_number=row_number, seat_letter=seat_letter, tier=tier)
                new_row[seat_letter] = seat

    def __generate_seat_headers(self, options: list) -> str:
        builder: StringIO = StringIO()
        builder.write(self.__generate_row_marker())

        for item in options:
            builder.write(CELL_SEPARATOR)
            builder.write(self.__generate_bar_header(width=INNER_CELL_WIDTH, text=item))
            builder.write(CELL_SEPARATOR)
        return builder.getvalue()

    def print_occupied_seats(self, tier: Tier, row_number: int):
        print(f"\tOccupied Seats for {tier.get_tier_name()}: "
              f"row-{row_number}: {make_dict_keys_str(self.get_occupied_seats(tier=tier, row_number=row_number))}")

    def print_available_seats(self, tier: Tier, row_number: int):
        print(f"\tAvailable Seats for {tier.get_tier_name()}: row-{row_number}: "
              f"{make_dict_keys_str(self.get_available_seats(tier=tier, row_number=row_number))}")

    def print_occupied_rows(self, tier: Tier):
        print(f"\tOccupied Rows for {tier.get_tier_name()}: "
              f"{make_dict_keys_str(items=self.get_occupied_rows(tier=tier))}")

    def print_available_rows(self, tier: Tier):
        print(f"\tAvailable Rows for {tier.get_tier_name()}: "
              f"{make_dict_keys_str(self.get_available_rows(tier=tier))}")

    def is_seat_booked(self, tier: Tier, row_number: int, seat_letter: str) -> bool:
        return self.__get_structure()[tier][row_number][seat_letter].is_taken()

    def get_occupied_seats(self, tier: Tier, row_number) -> dict:
        rtn_dict: dict = {}
        seat_keys: list = self.__get_structure()[tier][row_number].keys()
        seats: dict = self.__get_structure()[tier][row_number]
        for seat_key in seat_keys:
            seat: Seat = seats[seat_key]
            if seat.is_taken():
                rtn_dict[seat_key] = seat
        return rtn_dict

    def get_available_seats(self, tier: Tier, row_number) -> dict:
        rtn_dict: dict = {}
        seat_keys: list = self.__get_structure()[tier][row_number].keys()
        seats: dict = self.__get_structure()[tier][row_number]
        for seat_key in seat_keys:
            seat: Seat = seats[seat_key]
            if not seat.is_taken():
                rtn_dict[seat_key] = seat
        return rtn_dict

    def get_occupied_rows(self, tier) -> dict:
        rtn_dict: dict = {}
        row_keys: list = self.__get_structure()[tier].keys()
        rows: dict = self.__get_structure()[tier]
        for row_key in row_keys:
            occupied: bool = False
            seat_keys: list = rows[row_key].keys()
            row: dict = rows[row_key]
            for seat_key in seat_keys:
                seat: Seat = row[seat_key]
                if seat.is_taken():
                    occupied = True
                    break
            if occupied:
                rtn_dict[row_key] = rows[row_key]
        return rtn_dict

    def get_available_rows(self, tier) -> dict:
        rtn_dict: dict = {}
        row_keys: list = self.__get_structure()[tier].keys()
        rows: dict = self.__get_structure()[tier]
        for row_key in row_keys:
            available: bool = False
            seat_keys: list = rows[row_key].keys()
            row: dict = rows[row_key]
            for seat_key in seat_keys:
                seat: Seat = row[seat_key]
                if not seat.is_taken():
                    available = True
                    break
            if available:
                rtn_dict[row_key] = rows[row_key]
        return rtn_dict

    def get_full_rows(self, tier: Tier) -> dict:
        rtn_dict: dict = {}
        row_keys: list = self.__get_structure()[tier].keys()
        rows: dict = self.__get_structure()[tier]
        for row_key in row_keys:
            full: bool = True
            seat_keys: list = rows[row_key].keys()
            row: dict = rows[row_key]
            for seat_key in seat_keys:
                seat: Seat = row[seat_key]
                if not seat.is_taken():
                    full = False
                    break
            if full:
                rtn_dict[row_key] = rows[row_key]
        return rtn_dict

    def get_empty_rows(self, tier: Tier) -> dict:
        rtn_dict: dict = {}
        row_keys: list = self.__get_structure()[tier].keys()
        rows: dict = self.__get_structure()[tier]
        for row_key in row_keys:
            empty: bool = True
            seat_keys: list = rows[row_key].keys()
            row: dict = rows[row_key]
            for seat_key in seat_keys:
                seat: Seat = row[seat_key]
                if seat.is_taken():
                    empty = False
                    break
            if empty:
                rtn_dict[row_key] = rows[row_key]
        return rtn_dict

    def is_full(self):
        full: bool = True
        for tier in Tier:
            if len(self.get_available_rows(tier=tier)) > 0:
                full = False
                break
        return full

    def is_empty(self):
        empty: bool = True
        for tier in Tier:
            if len(self.get_occupied_rows(tier=tier)) > 0:
                empty = False
                break
        return empty


class Controller(metaclass=ABCMeta):

    @abstractmethod
    def do(self, model: SeatingStructure) -> 'Controller':
        """
        :param model: The model to use for this controller
        :return: the next controller that needs to be used, or None if the program is to quit
        """


class QuitController(Controller):

    def do(self, model: SeatingStructure):
        return None


def prompt_user_for_tier() -> Tier:
    while True:
        print(f"\tWhat is the tier of the seat?")
        for tier in Tier:
            print(f"\t{tier.get_menu_display_text()}")
        text = input("\t:")
        try:
            check_for_quit_or_return(text)
            tier = Tier.get_tier(text)
            print(f"You chose '{tier.get_tier_name()}'{linesep}")
            return tier
        except QuitApplication:
            raise QuitApplication
        except ReturnToMainMenu:
            raise ReturnToMainMenu
        except Exception as e:
            print(e)


class ReturnToMainMenu(Exception):
    pass


class QuitApplication(Exception):
    pass


class NoMoreBookings(Exception):
    pass


class NoBookingsExist(Exception):
    pass


def prompt_user_for_row_number(tier: Tier, model: SeatingStructure, change_booking: bool) -> int:
    while True:
        if change_booking:
            model.print_occupied_rows(tier)
        else:
            model.print_available_rows(tier)
        print(f"\tPlease select a row number{linesep}\t: ", end=EMPTY_STR)
        row_str: str = input()
        try:
            check_for_quit_or_return(row_str)
            row: int = int(row_str)
            if change_booking:
                if row in model.get_empty_rows(tier):
                    raise Exception(f"No seats have been booked yet for row {row} in {tier.get_tier_name()} ")
            else:
                if row in model.get_full_rows(tier):
                    raise Exception(f"Row {row} in {tier.get_tier_name()} is full for this flight.")
            print(f"Row {row} in {tier.get_tier_name()} has been selected{linesep}")
            return row
        except QuitApplication:
            raise QuitApplication
        except ReturnToMainMenu:
            raise ReturnToMainMenu
        except ValueError:
            print(f'Entry "{row_str}" could not be evaluated as an integer.')
        except Exception as e:
            print(e)


def check_for_quit_or_return(row_str):
    if row_str.upper() == QUIT_CHAR:
        raise QuitApplication
    if row_str.upper() == RETURN_TO_MAIN_CHAR:
        raise ReturnToMainMenu


def prompt_user_for_seat_letter(tier: Tier, row_number: int, model: SeatingStructure, change_booking: bool) -> str:
    while True:
        if change_booking:
            model.print_occupied_seats(tier=tier, row_number=row_number)
        else:
            model.print_available_seats(tier=tier, row_number=row_number)
        print(f"\tPlease select a seat letter{linesep}\t: ", end=EMPTY_STR)
        seat_str: str = input().upper()
        try:
            check_for_quit_or_return(seat_str)
            if seat_str == EMPTY_STR:
                raise Exception("No entry detected")
            if seat_str not in model.get_seat_options(tier=tier):
                raise_invalid_option_exception(seat_str)
            if change_booking:
                if not model.is_seat_booked(tier=tier, row_number=row_number, seat_letter=seat_str):
                    raise Exception(
                        f"{tier.get_tier_name()} seat '{row_number}-{seat_str}' does not have a passenger assigned to "
                        f"it.")
            else:
                if model.is_seat_booked(tier=tier, row_number=row_number, seat_letter=seat_str):
                    raise Exception(
                        f"{tier.get_tier_name()} seat '{row_number}-{seat_str}' is not available.")
            print(f"You chose seat-letter '{seat_str}'")
            return seat_str
        except QuitApplication:
            raise QuitApplication
        except ReturnToMainMenu:
            raise ReturnToMainMenu
        except Exception as e:
            print(e)


def prompt_user_for_passenger_name() -> str:
    while True:
        print(f"\tWhat is the passenger's name?{linesep}\t:", end=EMPTY_STR)
        try:
            name_str: str = input()
            check_for_quit_or_return(name_str)
            rtn_name: str = EMPTY_STR
            words: list = name_str.split()
            if len(words) == 0:
                raise Exception("No name supplied.")
            for word in words:
                word = word.capitalize()
                if not word.isalpha():
                    raise Exception(f'"{word}" contains invalid characters.')
                rtn_name += f"{word} "
            rtn_name = rtn_name.rstrip(rtn_name[-1])
            return rtn_name
        except QuitApplication:
            raise QuitApplication
        except ReturnToMainMenu:
            raise ReturnToMainMenu
        except Exception as e:
            print(e)


def print_exiting_guidance():
    print(f"\t{QUIT_GUIDANCE_TEXT}")
    print(f"\t{RETURN_GUIDANCE_TEXT}{linesep}")


def prompt_user_for_passenger_age() -> int:
    while True:
        print(f"\tWhat is the passenger's age? ({MIN_AGE} to {MAX_AGE}){linesep}\t:", end=EMPTY_STR)
        age_str: str = input()
        try:
            check_for_quit_or_return(age_str)
            age: int = int(age_str)
            if age < MIN_AGE or age > MAX_AGE:
                raise Exception(f"Age '{age} is not within valid bounds ({MIN_AGE} to {MAX_AGE})")
            return age
        except QuitApplication:
            raise QuitApplication
        except ReturnToMainMenu:
            raise ReturnToMainMenu
        except ValueError:
            print(f'Entry "{age_str}" could not be evaluated as an integer.')
        except Exception as e:
            print(e)


def obtain_passenger_from_attendant() -> Passenger:
    name: str = prompt_user_for_passenger_name()
    age: int = prompt_user_for_passenger_age()
    passenger: Passenger = Passenger(name=name, age=age)
    print(f'Passenger "{passenger}" (age {age}) has been created')
    return passenger


def obtain_seat_from_attendant(model: SeatingStructure, change_booking: bool) -> Seat:
    tier: Tier = prompt_user_for_tier()
    row_number = prompt_user_for_row_number(tier=tier, model=model, change_booking=change_booking)
    seat_letter = prompt_user_for_seat_letter(tier=tier, row_number=row_number, model=model,
                                              change_booking=change_booking)
    seat: Seat = Seat(tier=tier, row_number=row_number, seat_letter=seat_letter)
    print(f"{tier.get_tier_name()} seat {row_number}-{seat_letter} has been selected")
    return seat


def prompt_user_for_tax_rate() -> float:
    while True:
        print(f'{linesep}\tPlease enter the tax rate for this transaction.')
        rate_str = input(f'\tRates are entered in decimal form. ("0.8" = 8.0%){linesep}\t:')
        try:
            check_for_quit_or_return(rate_str)
            rate_f: float = float(rate_str)
            r: int = floor(rate_f * 1000)
            rate_f: float = r / 1000
            rate_str = f'{rate_f * 100}%'
            print(f"Rate Entered is {rate_str}")
            return rate_f
        except ReturnToMainMenu:
            raise ReturnToMainMenu()
        except QuitApplication:
            raise QuitApplication()
        except ():
            print(f'Value ({rate_str}) is not interpretable as a tax-rate')
            print(f'Please only enter numerical values, and a decimal place if appropriate')
        except Exception as e:
            print(e)


def handle_money_transfer(to_seat: Seat, from_seat: Seat = None):
    owed_cents: int = to_seat.get_price_cents() if from_seat is None else from_seat.compare_cost_cents(to_seat)
    while True:
        print(f"{linesep}Amount owed is {MoneyManipulator.convert_cents_to_dollar_str(owed_cents)}")
        print(f'\tPlease enter amount paid by customer{linesep}\t:', end=EMPTY_STR)
        amt_str = input()
        try:
            check_for_quit_or_return(amt_str)
            amt: float = float(amt_str)
            amt_cents: int = floor(amt * 100)
            diff = amt_cents - owed_cents
            if diff < 0:
                owed_str: str = MoneyManipulator.convert_cents_to_dollar_str(abs(diff))
                owed_cents -= amt_cents
                raise Exception(f"{owed_str} is insufficient to cover the cost of this booking")
            else:
                MoneyManipulator.make_change(amount_cents=diff, do_print=True)
                break
        except ReturnToMainMenu:
            raise ReturnToMainMenu()
        except QuitApplication:
            raise QuitApplication()
        except ValueError:
            print(f'Value ({amt_str}) could not be converted to a dollar amount')
            print(f'Please only enter numerical values, and a decimal place if appropriate')
        except Exception as e:
            print(e)


def check_model_full(model: SeatingStructure):
    if model.is_full():
        raise NoMoreBookings()


def check_model_empty(model: SeatingStructure):
    if model.is_empty():
        raise NoBookingsExist()


class NewBookingController(Controller):

    def do(self, model: SeatingStructure) -> Controller:
        try:
            check_model_full(model)
            print(f"{linesep}Create A New Booking:")
            print_exiting_guidance()
            seat: Seat = obtain_seat_from_attendant(model=model, change_booking=False)
            passenger: Passenger = obtain_passenger_from_attendant()
            seat.assign_passenger(passenger)
            tax_rate: float = prompt_user_for_tax_rate()
            passenger.set_tax_rate(tax_rate)
            handle_money_transfer(seat)
            model.set_seat(seat)
            print(f"Booked: {seat.get_full_seat_description()}")
        except NoMoreBookings:
            print("This is a full flight; no more bookings can be made unless there is a cancellation.")
        except ReturnToMainMenu:
            pass
        except QuitApplication:
            return QuitController()
        return MainController()


def move_passenger(to_seat: Seat, from_seat: Seat, model: SeatingStructure):
    to_seat.assign_passenger(from_seat.get_passenger())
    from_seat.remove_passenger()
    model.set_seat(to_seat)
    model.set_seat(from_seat)


class DeleteBookingController(Controller):

    def do(self, model: SeatingStructure) -> Controller:
        print(f"{linesep}Delete An Existing Booking:")
        print_exiting_guidance()
        try:
            check_model_empty(model=model)
            seat: Seat = obtain_seat_from_attendant(model=model, change_booking=True)
            seat.remove_passenger()
            print(f'Seat {seat.get_row_seat_str()} booking removed')
        except NoBookingsExist:
            print("There are no bookings to delete.")
        except ReturnToMainMenu:
            pass
        except QuitApplication:
            return QuitController()
        return MainController()


class ChangeBookingController(Controller):

    def do(self, model: SeatingStructure) -> Controller:
        print(f"{linesep}Change An Existing Booking:")
        print_exiting_guidance()
        try:
            check_model_full(model)
            check_model_empty(model)
            print("Please provide the information for the existing booking:")
            from_seat: Seat = obtain_seat_from_attendant(model=model, change_booking=True)
            print("Please provide the information that for the seat that is desired:")
            to_seat: Seat = obtain_seat_from_attendant(model=model, change_booking=False)
            row_number: int = from_seat.get_row_number()
            seat_letter: str = from_seat.get_seat_letter()
            tier: Tier = from_seat.get_tier()
            from_seat = model.get_seat(row_number=row_number, seat_letter=seat_letter, tier=tier)
            diff: int = from_seat.compare_cost_cents(to_seat=to_seat)
            handle_money_transfer(to_seat=to_seat, from_seat=from_seat)
            move_passenger(from_seat=from_seat, model=model, to_seat=to_seat)
            print(f'Passenger "{to_seat.get_passenger().get_name()}" '
                  f'moved from {from_seat.get_row_seat_str()} to {to_seat.get_row_seat_str()} ', end=EMPTY_STR)

            if diff == 0:
                print(f' at no charge."')
            else:
                print(f" for an additional cost of {MoneyManipulator.convert_cents_to_dollar_str(diff)}")
        except NoMoreBookings:
            print("This is a full flight; There are no seats to move to.")
        except NoBookingsExist:
            print("No bookings exist to change.")
        except ReturnToMainMenu:
            pass
        except QuitApplication:
            return QuitController()
        except Exception as e:
            print(e)
        return MainController()


class PrintBookingController(Controller):
    def do(self, model: SeatingStructure) -> Controller:
        print(f"{linesep}\tBookings Chart:")
        print(f"{linesep}{model.generate_chart()}")
        return MainController()


def raise_invalid_option_exception(text: str):
    raise Exception(f"Entry '{text}' is not a valid option")


class MainMenuChoices(Enum):
    new_booking = ["(N)ew Booking", 'N', NewBookingController]
    change_booking = ["(C)hange Booking", 'C', ChangeBookingController]
    delete_booking = ["(D)elete Booking", 'D', DeleteBookingController]
    print_bookings = ["(P)rint Bookings Chart", 'P', PrintBookingController]
    quit = ["(Q)uit", 'Q', QuitController]

    def get_controller(self) -> Controller:
        return self.value[2]()

    @classmethod
    def get_by_letter(cls, text: str) -> 'MainMenuChoices':
        if text != EMPTY_STR:
            text = text[0].upper()
            for member in cls:
                if text == member.value[1]:
                    return member
        raise_invalid_option_exception(text)

    def get_menu_text(self):
        return self.value[0]


class MainController(Controller):

    def __init__(self):
        super().__init__()

    def do(self, model: SeatingStructure) -> Controller:
        print(f"{linesep}Main Menu")
        return self.prompt_for_choice()

    @staticmethod
    def prompt_for_choice() -> Controller:
        choice: MainMenuChoices
        while True:
            print(f"\tOptions:")
            for member in MainMenuChoices:
                print(f"\t{member.get_menu_text()}")
            text: str = input("\t: ")
            try:
                choice = MainMenuChoices.get_by_letter(text=text)
                return choice.get_controller()
            except Exception as e:
                print(e)


'''
    Rules:
    First-Class basefare is $500
    Coach base fare is $199
    If passenger is under 7 or 65+, 20% discount
    No refunds
    
    Establish an "exit/return" option so that the attendant can back out of a menu if they need to
    Establish a "quit" option so that the attendant can quit at any point.
    Design Interface:
        Print welcome & info messages
        Prompt for (Receive/Validate) main menu options
            * Make New Booking
            * Change Existing Booking
            * Print Booking Chart
            * Quit
            
            If "Make New Booking":
                Generate Seat
                    Prompt (Receive/Validate) for reservation tier (first class or coach)
                    Prompt (Receive/Validate) for row-number
                        Display available rows in tier
                        Check row exists in tier
                        Check if bookings are available in that row and tier
                    Prompt (Receive/Validate) for seat-letter
                        Display available seats in tier/row
                        Check seat exists/available in tier/row-number/seat-letter
                    Create Seat with tier, row-number, and seat-letter provided
                
                Generate Passenger:
                    Prompt (Receive/Validate) for the name of the person taking the flight.
                        Verify that this is comprised of alphabetical characters
                        Prompt (Receive/Validate) attendant for age of person taking the flight
                            Age range limited to realistic values
                        Create Passenger with name and age
                
                Assign Passenger to Seat (not added to data structure yet)
                Handle payment
                    Get cost of ticket for seat
                        Calculate using base ticket price, age-discount, & sales tax
                    Prompt user for amount paid
                    If user provides insufficient amount:
                        Prompt for more money
                    Once user provides amount equal or greater than cost:
                        User is assigned a ticket
                        Any change is provided:
                            Determine optimal change
                            Print out denominations returned
                            
                Assign Seat to Flight
                
                User can exit from any options by entering designated return char ('R')
                User can exit from any options by entering designated return char ('Q')
            
            If "Change Existing Booking"
                Find Existing Seat/Booking
                    Prompt (Receive/Validate) for reservation tier (first class or coach)
                    Prompt (Receive/Validate) for row-number
                        Display rows where bookings exist
                        Check row exists in tier
                        Check if any reservations exist in that tier
                    Prompt (Receive/Validate) for seat-letter
                        Display seats in where bookings exist
                        Check seat exists in tier and row
                        Check if seat is presently booked
                    Create/Find Seat with tier, row-number, and seat-letter provided
                
                Find new seat
                    Prompt (Receive/Validate) for reservation tier (first class or coach)
                    Prompt (Receive/Validate) for row-number
                        Display free rows for tier
                        Check row exists in tier
                        Check if any open seats exist in that tier
                    Prompt (Receive/Validate) for seat-letter
                        Display free seats in tier/row
                        Check seat exists in tier and row
                        Check if seat is currently booked
                
                If upgrading from coach to first-class
                    Handle payment
                        Get cost for change of ticket
                        Prompt user for amount paid
                        If user provides insufficient amount:
                            Prompt for more money
                        Once user provides amount equal or greater than cost:
                            Any change is provided:
                                Determine optimal change
                                Print out denominations returned
                
                Assign passenger to new seat
                Remove passenger from old seat
                
                User can exit from any options by entering designated return char ('R')
                User can exit from any options by entering designated return char ('Q')
                
            If "Print Booking Chart"
                Display all the bookings in a readable chart (See guidance document)
                    If the person’s name is longer than 12 characters:
                        Only display the first 12 name-characters
                If all seats are taken:
                    Display a message is displayed stating that no new reservations can be made
            
            If "Quit":
                Quit
'''
